import streamlit as st
from dotenv import load_dotenv
from model import PersonalAssistant
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import web_search_tool, wiki_tool
import os

# Load environment variables
load_dotenv()

# Get API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

if not openai_api_key and not google_api_key:
    st.error(
        "Missing API keys. Set OPENAI_API_KEY or GOOGLE_API_KEY in your .env file."
    )
    st.stop()

# Initialize AI models
llm_openai = (
    ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key) if openai_api_key else None
)
llm_gemini = (
    ChatGoogleGenerativeAI(
        model="gemini-2.5-pro-exp-03-25", temperature=0.1, max_retries=2
    )
    if google_api_key
    else None
)

# Create LangChain prompt
parser = PydanticOutputParser(pydantic_object=PersonalAssistant)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are my personal assistant that helps me learn about new topics.
            Answer the user's query in detail and use necessary tools.
            Generate the output in the format specified and be sufficient in your answer.\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [web_search_tool, wiki_tool]

# Streamlit UI
st.title("🧠 AI Personal Agent")

# Model selection
available_models = {}
if llm_openai:
    available_models["GPT-4o-mini"] = llm_openai
if llm_gemini:
    available_models["Gemini 2.5 Pro"] = llm_gemini

model_choice = st.selectbox("Select AI Model", list(available_models.keys()))

# Initialize selected agent
llm = available_models[model_choice]
agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# User input
query = st.text_input("How can I help you?", "")

if st.button("Submit") and query:
    with st.spinner(f"Thinking with {model_choice}... 🤔"):
        raw_response = agent_executor.invoke({"query": query})
        structured_response = parser.parse(raw_response.get("output"))

    # Display response in a readable format
    st.subheader("📌 Topic")
    st.write(structured_response.topic)

    st.subheader("📝 Answer")
    st.write(structured_response.answer)

    st.subheader("🔗 Sources")
    for source in structured_response.sources:
        st.markdown(f"- [{source}]({source})")

    st.subheader("🛠 Tools Used")
    st.write(", ".join(structured_response.tools_used))
