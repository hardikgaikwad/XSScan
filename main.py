import asyncio
import argparse
from core.scanner import Scanner

parser = argparse.ArgumentParser(
    description="Context-aware reflected XSS scanner"
)

parser.add_argument(
    "--url",
    required=True,
    help="Target URL to scan"
)

parser.add_argument(
    "--depth",
    type=int,
    default=0,
    help="Crawl depth (default: 0)"
)

args = parser.parse_args()


async def main():
    scanner = Scanner(args.url, max_depth=args.depth)
    await scanner.run()
    
if __name__ == "__main__":
    asyncio.run(main())