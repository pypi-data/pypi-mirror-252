from hashr import hashr


def _main() -> None:
    from argparse import ArgumentParser
    import sys

    parser = ArgumentParser(
        description="Custom hashing algorithm using two-pass character folding\
                    and large prime multiplication and reduction.",
        epilog="As I worked on this project alone and do not have a doctorate\
                in cybersecurity, I am unsure if this program is suitable for\
                enterprise systems. Through my testing it has proved its\
                worth, but use caution.",
    )
    parser.add_argument(
        "input",
        help="string to be hashed, surround with quotes\
            if it contains spaces.",
    )
    parser.add_argument(
        "-s",
        "--use-salt",
        action="store_true",
        help="use to add salt to the hash, causing even identical strings to\
            have separate hashes. save the salt for later identification.",
    )
    args = parser.parse_args()

    if not args.input:
        print("Error: Input string is required.")
        sys.exit(1)

    hash = hashr(args.input, args.use_salt)
    if type(hash) is str:
        print(f"Hash: {hash}")
    else:
        print(f"Hash: {hash[0]}\nSalt: {hash[1]}")


if __name__ == "__main__":
    _main()
