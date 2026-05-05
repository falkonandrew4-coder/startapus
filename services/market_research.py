from duckduckgo_search import DDGS
import httpx
import os

# Програмний продукт розроблено Соколом Андрієм - Falkon AI

async def research_market_duckduckgo(query: str):
    """Пошук реальних кейсів успіху/провалу через DuckDuckGo з підтримкою проксі"""
    try:
        # Звичайний запит
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(f"{query} success failure cases why failed startup", max_results=5)]
        return results
    except Exception as e:
        print(f"DuckDuckGo error, attempting proxy fallback: {e}")
        try:
            proxy_url = os.environ.get("PROXY_URL")
            if proxy_url:
                # Вмикаємо проксі лише у разі помилки (капча/блок)
                with DDGS(proxies={"http": proxy_url, "https": proxy_url}) as ddgs:
                    results = [r for r in ddgs.text(f"{query} success failure cases why failed startup", max_results=5)]
                return results
            else:
                return []
        except Exception as proxy_error:
            print(f"Proxy fallback failed: {proxy_error}")
            return []

async def research_producthunt(query: str):
    """Пошук конкурентів та трендів на ProductHunt через GraphQL"""
    client_id = os.environ.get("PRODUCTHUNT_CLIENT_ID")
    client_secret = os.environ.get("PRODUCTHUNT_CLIENT_SECRET")
    
    url = "https://api.producthunt.com/v2/api/graphql"
    
    # GraphQL запит для пошуку постів за ключовим словом
    query_graphql = """
    query ($term: String) {
      posts(topic: $term, first: 5) {
        edges {
          node {
            name
            tagline
            votesCount
            website
          }
        }
      }
    }
    """
    
    # Тут буде логіка отримання токену та виконання запиту
    # Поки що повертаємо порожній список для подальшої реалізації
    return []

async def research_github(query: str):
    """Пошук репозиторіїв на GitHub для аналізу технологій та популярності"""
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=5"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                results = []
                for repo in data.get("items", []):
                    results.append({
                        "full_name": repo["full_name"],
                        "stars": repo["stargazers_count"],
                        "updated_at": repo["updated_at"],
                        "description": repo["description"],
                        "url": repo["html_url"]
                    })
                return results
            return []
        except Exception as e:
            print(f"GitHub Search Error: {e}")
            return []

async def research_libraries(query: str):
    """Аналіз популярних бібліотек та фреймворків через libraries.io"""
    api_key = os.environ.get("LIBRARIES_IO_API_KEY")
    if not api_key:
        return []
    
    url = f"https://libraries.io/api/search?q={query}&api_key={api_key}&per_page=5"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return [{
                    "name": lib["name"],
                    "stars": lib["stars"],
                    "language": lib["language"],
                    "latest_release": lib["latest_release_number"]
                } for lib in data]
            return []
        except Exception as e:
            print(f"Libraries.io Search Error: {e}")
            return []

