import pytest
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Run pytest with a specified marker.")
    parser.add_argument(
        "-m",
        "--marker",
        default="not generation",
        help="Specify the marker expression for pytest.",
    )
    args = parser.parse_args()

    pytest.main(["-m", args.marker])


if __name__ == "__main__":
    main()
