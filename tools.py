from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool


search_engine = DuckDuckGoSearchRun()
web_search_tool = Tool(
    name="search",
    func=search_engine.run,
    description="Web search the for information",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
