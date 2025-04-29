import requests
from dotenv import load_dotenv
import os

load_dotenv()

def search(query: str) -> dict:
    API_KEY = os.getenv("BRAVE_API_KEY")
    url = "https://api.search.brave.com/res/v1/web/search"

    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": API_KEY
    }

    params = {
        "q": query,
        "count": 10,  # 取得件数（最大50）
        "safesearch": "off"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        results = response.json()
        print(results)
        for idx, item in enumerate(results.get("web", {}).get("results", []), start=1):
            print(f"{idx}. {item['title']}")
            print(f"URL: {item['url']}")
            print(f"Snippet: {item['description']}\n")
        return {"status": "success", "result": results}
    else:
        print("Error:", response.status_code, response.text)
        return {"status": "error", "error": response.text}
    
def get_page(url: str) -> dict:
    """Returns the content of a web page.
    
    Args:
        url (str): The URL of the web page.
    
    Returns:
        dict: status and result or error msg.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return {"status": "success", "result": response.text}
    else:
        return {"status": "error", "error": response.text}