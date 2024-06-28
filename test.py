import pytest
import argparse


def main():
    parser = argparse.ArgumentParser(description="Run pytest with a specified marker.")
    parser.add_argument(
        "marker",
        help="Specify the pytest marker to run",
        default="all",
        choices=["integration", "unit", "all"],
    )
    args = parser.parse_args()

    # Run pytest with the specified marker
    if args.marker == "integration":
        pytest.main(["-m", "integration"])
    elif args.marker == "unit":
        pytest.main(["-m", "not integration"])
    elif args.marker == "all":
        print("All test is disabled currently!")


if __name__ == "__main__":
    main()
