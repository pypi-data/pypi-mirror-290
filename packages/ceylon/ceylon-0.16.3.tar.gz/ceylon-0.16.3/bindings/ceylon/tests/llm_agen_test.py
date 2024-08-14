import asyncio

from duckduckgo_search import DDGS
from langchain_community.chat_models import ChatOllama, ChatOpenAI
from langchain_core.tools import StructuredTool

from ceylon import AgentRunner
from ceylon.llm.llm_agent import LLMAgent
from ceylon.tools.file_publisher_tool import FilePublisherTool
from ceylon.tools.search_tool import SearchTool


async def main():
    runner = AgentRunner(workspace_name="ceylon-ai")
    llm_lib = ChatOllama(model="llama3:instruct")
    # llm_lib = ChatOpenAI(model="gpt-4o")
    runner.register_agent(LLMAgent(
        name="writer",
        position="Assistant Writer",
        llm=llm_lib,
        responsibilities=["Create high-quality, original content that matches the audience's tone and style."],
        instructions=[
            "Ensure clarity, accuracy, and proper formatting while respecting ethical guidelines and privacy."]
    ))
    runner.register_agent(LLMAgent(
        name="name_chooser",
        position="Select File name",
        llm=llm_lib,
        responsibilities=["Create high-quality, SEO friendly file name."],
        instructions=[
            "Easy to read and understand."
        ]
    ))

    runner.register_agent(LLMAgent(
        name="researcher",
        position="Content Researcher",
        llm=llm_lib,
        responsibilities=[
            "Conducting thorough and accurate research to support content creation.",
            "summarize with source references"

        ],
        instructions=[
            "Must only Find the most relevant 2 or 3 sources."
            "Find credible sources, verify information, and provide comprehensive and relevant "
            "data while ensuring ethical "
            "standards and privacy are maintained.",
            "Must  summarize output with source references."
        ],
        tools=[
            SearchTool()
        ]
    ))
    #
    runner.register_agent(LLMAgent(
        name="editor",
        position="Content Editor",
        llm=llm_lib,
        responsibilities=[
            "Review and refine content to ensure it meets quality standards and aligns with the editorial guidelines.",
            "Write content in a clear and concise manner.",
            "Ensure the content is appropriate for the target audience.",
            "Ensure the content is engaging and maintains the intended tone and style.",
            "Include source references when appropriate."
        ],
        instructions=[
            "Check for grammatical errors, clarity, and coherence.",
            "Ensure the content is engaging and maintains the intended tone and style.",
            "Provide constructive feedback to the writer."
        ]
    ))
    #
    runner.register_agent(LLMAgent(
        name="publisher",
        position="Content Publisher",
        llm=llm_lib,
        responsibilities=[
            "Publish the finalized content using the publishing tools and platforms specified by the writer.",
        ],
        instructions=[
            "Publish it as finalized and polished content",
        ],
        tools=[
            FilePublisherTool()
        ]
    ))

    await runner.run(
        {
            "request": "I want to create a blog post",
            "title": "How to use AI for Machine Learning",
            "tone": "informal",
            "length": "large",
            "style": "creative"
        },
        network={
            "name_chooser": [],
            "researcher": [],
            "writer": ["researcher"],
            "editor": ["writer"],
            "publisher": ["editor", "name_chooser"]
        }
    )


if __name__ == '__main__':
    asyncio.run(main())
