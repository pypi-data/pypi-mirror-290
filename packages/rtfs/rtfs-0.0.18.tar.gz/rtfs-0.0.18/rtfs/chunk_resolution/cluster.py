import networkx as nx
from infomap import Infomap
import yaml
from dataclasses import dataclass
from typing import Dict, List

from rtfs.graph import DictMixin
from rtfs.models import OpenAIModel

from logging import getLogger

logger = getLogger(__name__)


def cluster_infomap(digraph: nx.DiGraph) -> Dict[int, List]:
    # Initialize Infomap
    infomap = Infomap("--seed 42", silent=True)

    # Create a mapping from NetworkX node IDs to integer IDs
    node_id_map = {node: idx for idx, node in enumerate(digraph.nodes())}
    reverse_node_id_map = {idx: node for node, idx in node_id_map.items()}

    # Add nodes and edges to Infomap using integer IDs
    for edge in digraph.edges():
        infomap.addLink(node_id_map[edge[0]], node_id_map[edge[1]])

    infomap.run()
    # Run Infomap clustering

    cluster_dict: Dict[int, List] = {}
    # node_id, path
    # 1 (1, 2, 2)
    for node, levels in infomap.get_multilevel_modules().items():
        node_id = reverse_node_id_map[node]
        cluster_dict[node_id] = [lvl for lvl in levels]

    # replace leaf nodes with their original id

    return cluster_dict


class LLMException(Exception):
    pass


@dataclass
class SummarizedChunk(DictMixin):
    title: str
    summary: str
    key_variables: List[str]


def summarize_chunk_text(cluster, model: OpenAIModel) -> SummarizedChunk:
    prompt = """
The following chunks of code are grouped into the same feature.
I want you to respond with a yaml object that contains the following fields: 
- first come up with a descriptive title that best captures the role that these chunks of code
play in the overall codebase. 
- next, write a single paragraph summary of the chunks of code
- finally, take a list of key variables/functions/classes from the code

Your yaml should take the following format:

title: str
summary: str
key_variables: List[str]

Here is the code:
{code}
    """

    async def query_model(cluster):
        # Retry logic for yaml parsing
        for attempt in range(3):
            try:
                response = await model.query(prompt.format(code=cluster))
                yaml_content = response.split("```yaml")[1].split("```")[0].strip()

                return SummarizedChunk(**yaml.safe_load(yaml_content))
            # TODO: check if this fails 3 times only or not at all
            except Exception as e:
                if attempt < 2:
                    print(f"{attempt + 1} summarizing attempt failed, retrying...")
                else:
                    raise LLMException("Failed to parse YAML after 3 attempts") from e

    return query_model(cluster)
