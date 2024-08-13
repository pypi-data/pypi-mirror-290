"""Basic CLI to describe the output shape of an AWS API operation, and optionally find the path to a key in the shape tree."""

import argparse
import logging
from dataclasses import dataclass

from botoplier._shapes import operation_output_shape, path_to_key, shape_tree
from botoplier.util.treeutils import first_branching_node

logger = logging.getLogger(__name__)

# Ensure we have a handler to print to stdout
if not logger.handlers:
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)


@dataclass
class OutputShapeArgs:
    api_name: str
    operation_name: str
    key_pathfinding: list[str]
    interactive: bool


def output_shape(args: OutputShapeArgs) -> None:
    """Prints the output shape of an AWS API operation."""
    shape = operation_output_shape(args.api_name, args.operation_name)
    tree = shape_tree(shape)
    thing = tree.show(stdout=False)
    print(thing)  # noqa: T201

    logger.info(f"Tree size: {tree.size()}")
    logger.info(f"First branching node: {first_branching_node(tree).identifier}")

    for key in args.key_pathfinding:
        path = path_to_key(tree, key)
        if path:
            logger.info(f"Key {key} lookup path: {path}")

    if args.interactive:
        breakpoint()  # noqa: T100


def main() -> None:
    main_parser = argparse.ArgumentParser(
        description="Prints an AWS API operation output shape and optionally starts a REPL for experimentation."
        "Useful to find the right subtree key for unnesting."
    )
    subparsers = main_parser.add_subparsers(help="commands", dest="command")

    # Setting up a subparser for the 'botoplier' command
    output_shape_parser = subparsers.add_parser(
        "output-shape",
        help="""Prints the output shape of an AWS API operation. Optionally, it can also print the path to a key in the shape tree.

    Example usage:
    ```
    python -m botoplier describe-shape ec2 describe_instances VirtualizationType
    ```

    This is useful to know the shape of `smart_query` results.""",
    )
    output_shape_parser.add_argument("api_name", type=str, help='The name of the AWS API (e.g., "ec2", "s3", "ecr")')
    output_shape_parser.add_argument("operation_name", type=str, help='The name of the operation within the API (e.g., "describe_instances", "list_buckets")')
    output_shape_parser.add_argument(
        "key_pathfinding",
        nargs="*",
        type=str,
        help="A key to find in the shape tree. If provided, the path to the key will be printed."
        'E.g. "Reservations", "Buckets", etc. Useful to determine your `smart_query`\'s `subtree` argument.',
    )
    output_shape_parser.add_argument("-i", "--interactive", action="store_true", help="Start a REPL for experimentation")

    args = main_parser.parse_args()

    if args.command == "output-shape":
        typed_args = OutputShapeArgs(
            api_name=args.api_name, operation_name=args.operation_name, key_pathfinding=args.key_pathfinding, interactive=args.interactive
        )
        output_shape(typed_args)
    else:
        main_parser.print_help()


if __name__ == "__main__":
    main()
