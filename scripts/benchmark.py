"""Performance benchmarking for HexStrike scan engine."""

import argparse
import time


def main():
    parser = argparse.ArgumentParser(description="Benchmark scan performance")
    parser.add_argument("--target", type=str, help="Target to benchmark against")
    parser.add_argument("--iterations", type=int, default=3)
    args = parser.parse_args()

    print(f"Benchmarking against {args.target} ({args.iterations} iterations)")
    # TODO: Run scans and measure timing
    start = time.monotonic()
    # placeholder
    elapsed = time.monotonic() - start
    print(f"Completed in {elapsed:.2f}s")


if __name__ == "__main__":
    main()
