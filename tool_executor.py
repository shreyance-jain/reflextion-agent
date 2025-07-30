from dotenv import load_dotenv

from schemas import AnswerQuestion, ReviseAnswer

load_dotenv()

from langchain_tavily import TavilySearch
from langchain_core.tools import StructuredTool ## allows to convert python function to tools which can then be used by llms
from langgraph.prebuilt import ToolNode ## node in lang graph that we can invoke check the last message in Messages key and then see if there is tool call in the lst last message and if there is it will execute it for us

tavily_tool = TavilySearch(max_results=5)

## make 2 functions one for the initial search and one for the revision search
def run_queries(search_queries: list[str], **kwargs):
    """Run the generated queries."""
    return tavily_tool.batch([{"query": query} for query in search_queries])

execute_tools = ToolNode(
    [
        StructuredTool.from_function(run_queries, name=AnswerQuestion.__name__),
        StructuredTool.from_function(run_queries, name=ReviseAnswer.__name__)
    ]
)