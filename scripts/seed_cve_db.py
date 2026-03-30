"""Seed the CVE knowledge base from NVD JSON feeds."""

import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Seed CVE knowledge base")
    parser.add_argument("--feed", type=str, help="Path to NVD JSON feed file")
    parser.add_argument("--year", type=int, help="NVD feed year to download")
    args = parser.parse_args()

    if args.feed:
        feed_path = Path(args.feed)
        if not feed_path.exists():
            print(f"Feed file not found: {feed_path}", file=sys.stderr)
            sys.exit(1)
        with open(feed_path) as f:
            data = json.load(f)
        cve_count = len(data.get("CVE_Items", []))
        print(f"Loaded {cve_count} CVEs from {feed_path}")
        # TODO: Embed and store in vector DB
    else:
        print("Usage: python seed_cve_db.py --feed <path-to-nvd-json>")


if __name__ == "__main__":
    main()
