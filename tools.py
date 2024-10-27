from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import AgentType, Tool, initialize_agent

search_tool = Tool(
    name="Web Search",
    func=DuckDuckGoSearchRun().run,
    description="Tool for searching the internet for general topics."
)

wikipedia_tool = Tool(
    name="Wikipedia",
    func=WikipediaAPIWrapper().run,
    description="Tool for finding information from Wikipedia on various topics."
)

tools=[search_tool, wikipedia_tool]