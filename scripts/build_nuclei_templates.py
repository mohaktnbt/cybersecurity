"""Build custom Nuclei templates for HexStrike-specific checks."""

import argparse


def main():
    parser = argparse.ArgumentParser(description="Build custom Nuclei templates")
    parser.add_argument("--output-dir", type=str, default="./templates")
    args = parser.parse_args()
    print(f"Building custom Nuclei templates in {args.output_dir}")
    # TODO: Generate custom templates for auth bypass, IDOR, etc.


if __name__ == "__main__":
    main()
