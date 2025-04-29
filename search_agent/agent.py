from datetime import datetime
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from . import utils

load_dotenv()

def get_current_time() -> dict:
    """Returns the current time.
    
    Returns:
        dict: status and result or error msg.
    """
    return {"status": "success", "current_time": str(datetime.now())}
    
def search(query: str) -> dict:
    """Returns a search result for the given query.
    
    Args:
        query (str): The search query.
    
    Returns:
        dict: status and result or error msg.
    """
    return utils.search(query)

def get_page(url: str) -> dict:
    """Returns the content of a web page.
    
    Args:
        url (str): The URL of the web page.
    
    Returns:
        dict: status and result or error msg.
    """
    # Simulate a page retrieval operation
    return utils.get_page(url)

current_time_agent = None
try:
    current_time_agent = Agent(
        model=LiteLlm("gemini/gemini-2.0-flash"),
        name="current_time_agent",
        instruction="You are the Current Time Agent. Your ONLY task is to provide a current time using the 'get_current_time' tool. Do nothing else.",
        description="Handles current time using the 'get_current_time' tool.",
        tools=[get_current_time],
    )
    print(f"✅ Sub-Agent '{current_time_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Could not redefine Greeting agent. Check Model/API Key ({current_time_agent.model}). Error: {e}")

search_agent = None
try:
    search_agent = Agent(
        model=LiteLlm("gemini/gemini-2.0-flash"),
        name="search_agent",
        instruction="You are the Search Agent. Your ONLY task is to provide a search result using the 'search' tool. Do nothing else.",
        description="Handles search using the 'search' tool.",
        tools=[search],
    )
    print(f"✅ Sub-Agent '{search_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Could not redefine Search agent. Check Model/API Key ({search_agent.model}). Error: {e}")

get_page_agent = None
try:
    get_page_agent = Agent(
        model=LiteLlm("gemini/gemini-2.0-flash"),
        name="get_page_agent",
        instruction="You are the Get Page Agent. Your ONLY task is to provide a page using the 'get_page' tool. Do nothing else.",
        description="Handles page using the 'get_page' tool.",
        tools=[get_page],
    )
    print(f"✅ Sub-Agent '{get_page_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Could not redefine Get Page agent. Check Model/API Key ({get_page_agent.model}). Error: {e}")

try:
    root_agent = Agent(
        name="weather_time_agent",
        model=LiteLlm("gemini/gemini-2.0-flash"),
        description=(
            "Agent to answer questions about anything."
        ),
        instruction=(
            "You are a helpful agent who can answer user questions."
        ),
        sub_agents=[current_time_agent, search_agent, get_page_agent],
    )
except Exception as e:
    print(f"Counld not create Agent. Error: {e}")