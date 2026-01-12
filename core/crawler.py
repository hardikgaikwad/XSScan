from core.http import fetch
from urllib.parse import urljoin, urlparse, parse_qsl, urlencode
from bs4 import BeautifulSoup
from collections import deque

TRACKING_PARAMS = ("utm_",)

def normalize_url(base_url, raw_url):
        
    absolute = urljoin(base_url, raw_url)
    
    parsed = urlparse(absolute)
    
    scheme = parsed.scheme
    netloc = parsed.netloc
    path = parsed.path.rstrip("/")
    
    query_params = parse_qsl(parsed.query)
    
    cleaned_params = []
    for key, value in query_params:
        if not key.startswith(TRACKING_PARAMS):
            cleaned_params.append((key, value))
            
    
    cleaned_params.sort()
    
    query = urlencode(cleaned_params)
    
    
    normalized = f"{scheme}://{netloc}{path}"
    if query:
        normalized += f"?{query}"
        
    return normalized
            

async def crawl(start_url, max_depth=3):
    
    queue = deque()
    visited = set()
    
    queue.append((start_url, 0))

    while queue:
        current_url, depth = queue.popleft()
        
        normalized = normalize_url(start_url, current_url)
        
        if normalized in visited:
            continue
        
        visited.add(normalized)
        
        if depth >= max_depth:
            continue
        
        response = await fetch(current_url)
        
        if "error" in response:
            continue
        
        body = response.get("body")
        if not body:
            continue
        
        soup = BeautifulSoup(body, "html.parser")
        links = soup.find_all("a", href=True)

        for link in links:
            absolute_url = normalize_url(current_url, link["href"])
            queue.append((absolute_url, depth+1))
        
    return visited 