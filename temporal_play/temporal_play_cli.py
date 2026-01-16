"""
CLI for temporal_play
"""

from argparse import ArgumentParser
import asyncio
from dotenv import load_dotenv
from temporal_play.workers.worker_1 import main as worker_1


load_dotenv()


def cli_argument_parser() -> ArgumentParser:
    """Function to create the argument parser

    :rtype: ArgumentParser
    :returns: The argument parser
    """
    arg_parser = ArgumentParser(description="temporal-play-cli")
    subparsers = arg_parser.add_subparsers(
        title="commands",
        description="Valid commands: a single command is required",
        help="CLI Help",
        dest="a single command please see the -h option",
    )
    subparsers.required = True

    # This is the sub parser to start worker
    arg_parser_hello = subparsers.add_parser("worker", help="Start Worker")
    arg_parser_hello.set_defaults(which_sub="worker")
    arg_parser_hello.add_argument("-a", "--address", required=True, help="The Temporal IP address")
    arg_parser_hello.add_argument("-p", "--port", required=True, help="The Temporal Port Number")
    arg_parser_hello.add_argument("-t", "--task-queue", required=True, help="The Temporal Task Queue Name")

    return arg_parser


def cli() -> None:
    """Function to run the command line
    :rtype: None
    :returns: Nothing it is the CLI
    """
    arg_parser = None

    try:
        arg_parser = cli_argument_parser()
        args = arg_parser.parse_args()

        if args.which_sub == "worker":
            asyncio.run(worker_1(host=args.address, port=args.port, task_queue=args.task_queue))

    except AttributeError as error:
        print(f"\n !!! {error} !!! \n")
        arg_parser.print_help()

    except FileNotFoundError as error:
        print(f"\n !!! {error} !!! \n")
        arg_parser.print_help()

    except FileExistsError as error:
        print(f"\n !!! {error} !!! \n")
        arg_parser.print_help()

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"\n !!! {error} !!! \n")
        arg_parser.print_help()
