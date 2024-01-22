import argparse
import os

def start_cli():
    parser = argparse.ArgumentParser(description="B-Tocs Container SDK - Manage Tools")
    subparsers = parser.add_subparsers(
        help="", dest="command", required=True, title="Command List"
    )

    keys_parser = subparsers.add_parser("keys", help="Manage API keys database")

    keys_subparser = keys_parser.add_subparsers(
        help="", dest="sub_command", title="Command List"
    )

    keys_add_parser = keys_subparser.add_parser("add", help="Add API keys to database")
    keys_add_parser.add_argument(
        "req_limit", type=int, help="Request Limits (per minute)"
    )
    keys_add_parser.add_argument(
        "--key", type=str, default="auto", required=False, help="API Key"
    )

    keys_remove_parser = keys_subparser.add_parser(
        "remove", help="Remove API keys to database"
    )
    keys_remove_parser.add_argument("key", type=str, help="API Key")

    args = parser.parse_args()

    if args.command == "keys":
        print("key not implemented yet")
    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    start_cli()
