from dotenv import load_dotenv
load_dotenv()



from crew import LLM
llm = LLM(
    model = "gemini/gemini-2.0-flash",
    temperature = 0.1

)


llm.call("Who Invented Transcendental Meditation.")



