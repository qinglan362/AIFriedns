import os
from typing import TypedDict, Annotated, Sequence

import lancedb
from django.utils.timezone import localtime, now
from langchain_community.vectorstores import LanceDB

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode

from web.documents.utils.custom_embeddings import CustomEmbeddings


class ChatGraph:
    @staticmethod
    def create_app():
        @tool
        def get_time() -> str:
           """当需要查询精确时间时,可以调用这个工具函数 返回格式 [年-月-日 时:分:秒]"""
           return localtime(now()).strftime('%Y-%m-%d %H:%M:%S')

        @tool
        def search_knowledge_base(query: str) -> str:
            """当用户需要查询阿里云百炼平台相关的知识时,调用这个工具函数。输入为要查询的问题，输出为查询结果"""
            db = lancedb.connect('./web/documents/lancedb_storage')
            embeddings = CustomEmbeddings()
            vector_db = LanceDB(
                connection=db,
                embedding=embeddings,
                table_name='my_knowledge_base',
            )
            docs = vector_db.similarity_search(query, k=3)
            context = '\n\n'.join([f'内容片段：{i+1}\n{doc.page_content}'for i ,doc in enumerate(docs)])
            return f'这是从知识库中的查询结果：\n\n{context}\n'

        tools = [get_time,search_knowledge_base]

        llm = ChatOpenAI(
            model='deepseek-v4-flash',
            openai_api_key=os.getenv('API_KEY'),
            openai_api_base=os.getenv('API_BASE'),
            streaming=True,
            model_kwargs={
                "stream_options": {
                    "include_usage": True,  # 输出token消耗数量
                }
            }
            # temperature=0.7,
            # max_tokens=2048,
            # enable_thinking=True,
        ).bind_tools(tools)

        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]

        def model_call(state: AgentState) -> AgentState:
            res = llm.invoke(state['messages'])
            return {'messages': [res]}

        def should_continue(state: AgentState) -> str:
            # 这里可以根据state的内容来判断是否继续执行后续的节点
            # 例如当模型输出满足某些条件时才继续执行后续的工具调用等
            last_message = state['messages'][-1]
            if last_message.tool_calls:
               return "tools"
            return "end"

        tool_node = ToolNode(tools)

        graph = StateGraph(AgentState)
        graph.add_node('agent', model_call)
        graph.add_node('tools', tool_node)

        graph.add_edge(START, 'agent')
        graph.add_conditional_edges(
            'agent',
            should_continue,
             {
                 'tools': 'tools',
                 'end': END,
             }
        )

        graph.add_edge('tools', 'agent')

        return graph.compile()

