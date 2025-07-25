import os
import traceback
from dotenv import load_dotenv
load_dotenv()

try:
    from crewai import Crew, Task, Agent, LLM
    from crewai.knowledge import StringKnowledgeSource, EmbedderConfig
    from crewai.knowledge.embedders import GoogleGeminiEmbeddingFunction

    print("Initializing Gemini LLM...")
    gemini_llm = LLM(model='gemini/gemini-2.0-flash')

    print("Configuring embedder...")
    embedder_config = EmbedderConfig(
        embedder=GoogleGeminiEmbeddingFunction(
            model='gemini-embedding-001',
            api_key=os.getenv('GEMINI_API_KEY')
        )
    )

    print("Creating knowledge base...")
    kb = StringKnowledgeSource(
        name='FAQ',
        content='''Q: How long is the refund window?
A: 30 days from purchase date, provided the item is unused.''',
        embedder_config=embedder_config
    )

    print("Setting up agent...")
    agent = Agent(
        role='Support Bot',
        goal='Answer refund questions',
        backstory='Expert in company policies.',
        llm=gemini_llm,
        knowledge=[kb]
    )

    print("Creating task...")
    task = Task(
        description='Customer asks: "Can I still get a refund after 25 days?"',
        expected_output='Short, friendly answer with policy citation.',
        agent=agent
    )

    print("Running crew...")
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    print("Result:", result)

except Exception as e:
    print(f'\nERROR: {str(e)}')
    print('\nTRACEBACK:')
    print(traceback.format_exc())

