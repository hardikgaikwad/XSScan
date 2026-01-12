from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from core.http import fetch
from plugins.payloads import PAYLOADS, XSS_MARKER

async def test_xss(url):
    findings = []
    
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    
    # nothing to test if no query parameters found
    if not query_params:
        return findings
    
    for param in query_params:
        original_params = query_params.copy()
        
        for context, payload_list in PAYLOADS.items():
            for payload_entry in payload_list:
                payload = payload_entry["payload"]
                
                mutated_params = original_params.copy()
                mutated_params[param] = [payload]
        
                new_query = urlencode(mutated_params, doseq=True)
                
                mutated_url = urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    new_query,
                    parsed.fragment
                ))
                
                response = await fetch(mutated_url)
                
                if "error" in response:
                    continue
                
                body = response.get("body", "")
                if not body:
                    continue
                
                if XSS_MARKER in body or payload.lower() in body.lower():
                    
                    findings.append({
                        "type": "Reflected XSS",
                        "url": mutated_url,
                        "parameter": param,
                        "payload_name": payload_entry["name"],
                        "payload": payload,
                        "declared_context": context,
                        "severity": "High"
                    })
                    
    return findings