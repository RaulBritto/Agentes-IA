from dotenv import load_dotenv
from model import PersonalAssistant
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import web_search_tool, wiki_tool
import os
from pprint import pprint

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
parser = PydanticOutputParser(pydantic_object=PersonalAssistant)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are my personal assistant that will help generate to know more about topics that I don't have domain.
            Answer the user query with details and use necessary tools. 
            Generate the output in the format specified and be sucient in your answer.\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [web_search_tool, wiki_tool]

agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

query = input("How can I help you? ")
raw_response = agent_executor.invoke({"query": query})
structured_response = parser.parse(raw_response.get("output"))
pprint(structured_response.model_dump(), sort_dicts=False)
