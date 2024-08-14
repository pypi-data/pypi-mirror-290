import argparse
from simple_poetry_package.hello_world import HelloWorld


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True, help="Pass your name")
    args = parser.parse_args()
    hw = HelloWorld(args.name)
    hw.print_name()


if __name__ == "__main__":
    cli()
