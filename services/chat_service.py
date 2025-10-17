from google import genai
from google.genai import types
from config.prompt import CHATBOT_PROMPT

from agents import OpenAIChatCompletionsModel, function_tool
from openai import AsyncOpenAI
from tavily import TavilyClient


from config.load_env import GEMINI_API_KEY, GEMINI_MODEL, TAVILY_API_KEY
client = genai.Client(api_key=GEMINI_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


async def create_gemini_model() -> OpenAIChatCompletionsModel:
    """Create and configure the Gemini model."""
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
    MODEL_NAME = GEMINI_MODEL
    
    api_key = GEMINI_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    
    client = AsyncOpenAI(base_url=BASE_URL, api_key=api_key)
    return OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client)



@function_tool
def tavily_search(query: str) -> str:
    """
    Perform a web search using Tavily and return a summarized result.
    """
    response = tavily_client.search(query,search_depth='advanced',max_results='5')
    results = response.get("results", [])
    return results or "No results found."