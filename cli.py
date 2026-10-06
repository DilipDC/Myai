from __future__ import annotations

import argparse

from app import agent


def main() -> None:
    parser = argparse.ArgumentParser(description="JARVIS CLI")
    parser.add_argument("message", nargs="*", help="message to JARVIS")
    args = parser.parse_args()
    message = " ".join(args.message).strip()

    if not message:
        print("JARVIS CLI. Type a message:")
        while True:
            try:
                message = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if not message:
                continue
    result = agent.handle(message)
    print(result["reply"])


if __name__ == "__main__":
    main()
