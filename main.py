import argparse


def main():
    parser = argparse.ArgumentParser(
        description="File Compression System", add_help=False
    )
    subparsers = parser.add_subparsers(dest="command")

    compress_parser = subparsers.add_parser("compress", help="Compress files")
    compress_parser.add_argument(
        "-a", "--algorithm", choices=["zip", "gzip", "lzma"], required=True
    )
    compress_parser.add_argument("-f", "--files", nargs="+", required=True)
    compress_parser.add_argument("-o", "--output", required=True)
    compress_parser.add_argument("-p", "--password")

    decompress_parser = subparsers.add_parser("decompress", help="Decompress archive")
    decompress_parser.add_argument("-f", "--file", required=True)
    decompress_parser.add_argument("-o", "--output", required=True)
    decompress_parser.add_argument("-p", "--password")

    args = parser.parse_args()

    if args.command is None:
        from compression.gui_compressor import GuiCompressor

        app = GuiCompressor()
        app.run()
    elif args.command == "compress":
        from compression.cli_compressor import CliCompressor

        app = CliCompressor(
            files=args.files,
            algorithm=args.algorithm,
            output=args.output,
            password=args.password,
            direction="compress",
        )
        app.run()
    elif args.command == "decompress":
        from compression.cli_compressor import CliCompressor

        app = CliCompressor(
            files=[args.file],
            output=args.output,
            password=args.password,
            direction="decompress",
        )
        app.run()


if __name__ == "__main__":
    main()
