from core.crawler import crawl
from core.http import fetch
from plugins.xss import test_xss

class Scanner:
    def __init__(self, target, max_depth=3):
        self.target = target
        self.max_depth = max_depth
        self.findings = []
        
    async def run(self):
        print(f"[+] Starting crawl on {self.target}")
        
        urls = await crawl(self.target, self.max_depth)
        
        print(f"[+] Discovered {len(urls)} URLs")
        
        for url in urls:
            response = await fetch(url)
            
            if "error" in response:
                print(f"[-] Error fetching {url}: {response['error']}")
                continue
                
            print(f"[+] Testing {url}")
            print("\n\n")
            
            xss_results = await test_xss(url)
            
            if xss_results:
                for finding in xss_results:
                    self.findings.append(finding)
                    print(f"[!!!] Reflected XSS Found \nURL: <{finding['url']}> \nParameter: <{finding['parameter']}> \nPayload: <{finding['payload']}> \nTested context: <{finding['declared_context']}>")
                    print("----------------------------------------------------------------------------------------")
                    
                    
        print("\n[+] Scan complete")
        print(f"[+] Total findings: {len(self.findings)}")