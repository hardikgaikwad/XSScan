import httpx
import time

DEFAULT_HEADERS = {
    "User-Agent": "XSScan/1.0"
}

async def fetch(
    url,
    method="GET",
    params=None,
    data=None,
    headers=None,
    timeout=10
):
    request_headers = DEFAULT_HEADERS.copy()
    if headers:
        request_headers.update(headers)
        
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(
            headers=request_headers,
            follow_redirects=True,
            timeout=timeout
        ) as client:
            
            response = await client.request(
                method=method,
                url=url,
                params=params,
                data=data
            )
            
            elapsed = round(time.time() - start_time, 2)
            
            return {
                "url" : str(response.url),
                "method" : method,
                "status" : response.status_code,
                "headers" : dict(response.headers),
                "body" : response.text,
                "elapsed" : elapsed
            }
    
    except httpx.RequestError as e:
        return {
            "url" : url,
            "method" : method,
            "error" : str(e)
        }