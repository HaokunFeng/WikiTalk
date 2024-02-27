import os
import openai
import streamlit as st
from pathlib import Path
import requests

from llama_index import(
    VectorStoreIndex,
    SummaryIndex,
    SimpleDirectoryReader,
    ServiceContext,
)
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms import OpenAI
from llama_index.agent import OpenAIAgent
from llama_index import load_index_from_storage, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.objects import ObjectIndex, SimpleToolNodeMapping
from dotenv import load_dotenv


load_dotenv()
llm = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OEPNAI_API_BASE"),
    model="gpt-3.5-turbo",
    temperature=0.0,
    menu_items=None,
)
service_context = ServiceContext.from_defaults(llm=llm)


wiki_titles = [
    "Serie A",
    "Premier League",
    "Bundesliga",
    "La Liga",
    "Ligue 1"
]


for title in wiki_titles:
    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "extracts",
            "explaintext": True,
        },
    ).json()
    page = next(iter(response["query"]["pages"].values()))
    wiki_text = page["extract"]

    data_path = Path("data")
    if not data_path.exists():
        Path.mkdir(data_path)
    
    with open(data_path / f"{title}.txt", "w") as fp:
        fp.write(wiki_text)


leagues_docs = {}
for wiki_title in wiki_titles:
    leagues_docs[wiki_title] = SimpleDirectoryReader(
        input_files=[f"data/{wiki_title}.txt"]
    ).load_data()



node_parser = SentenceSplitter()

#Build agents dictionary
agents = {}
query_engines = {}
all_nodes = []

for idx, wiki_title in enumerate(wiki_titles):
    nodes = node_parser.get_nodes_from_documents(leagues_docs[wiki_title])
    all_nodes.extend(nodes)

    if not os.path.exists(f"./data/{wiki_title}"):
        #build vector index
        vector_index = VectorStoreIndex(nodes, service_context=service_context)
        vector_index.storage_context.persist(
            persist_dir=f"./data/{wiki_title}"
        )
    else:
        vector_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=f"./data/{wiki_title}"),
            service_context=service_context,
        )
    
    # build summary index
    summary_index = SummaryIndex(
        nodes,
        service_context=service_context,
    )
    # define query engine
    vector_query_engine = vector_index.as_query_engine()
    summary_query_engine = summary_index.as_query_engine()

    # define tools
    query_engine_tools = [
        QueryEngineTool(
            query_engine=vector_query_engine,
            metdata=ToolMetadata(
                name="vector_tool",
                description=(
                    "Useful for questions related to specific aspects of"
                    f" {wiki_title} (e.g. the history, teams and performance in EU, or more)."
                ),
            ),
        ),
        QueryEngineTool(
            query_engine=summary_query_engine,
            metdata=ToolMetadata(
                name="summary_tool",
                description=(
                    "Useful for any requests that require a holistic summary"
                    f" of EVERYTHING about {wiki_title}. For questions about more specific sections, please use the vertor_tool."
                ),
            ),
        ),
    ]

    # define agents
    function_llm = OpenAI(model="gpt-4")
    agent = OpenAIAgent.from_tools(
        query_engine_tools,
        llm=function_llm,
        verbose=True,
        system_prompt=f"""\
        Your are a specialist in answering questions about {wiki_title}.
        You must ALWAYS use at least one of the tools provided when answering a question; DO NOT RELY ON PRIOR KNOWLEDGE.\
        """,
    )
    agents[wiki_title] = agent
    query_engines[wiki_title] = vector_index.as_query_engine(
        similarity_top_k=2
    )


# define tool for each document agent
all_tools = []
for wiki_title in wiki_titles:
    wiki_summary = (
        f"This content contains Wikipedia artiles about {wiki_title}. Use"
        f" this tool if you want to answer any questions about {wiki_title}.\n"
    )
    doc_tool = QueryEngineTool(
        query_engine=agents[wiki_title],
        metadata=ToolMetadata(
            name=f"tool_{wiki_title.replace(' ', '_')}",
            description=wiki_summary,
        ),
    )
    all_tools.append(doc_tool)


# define an "object" index and retriever over these tools

