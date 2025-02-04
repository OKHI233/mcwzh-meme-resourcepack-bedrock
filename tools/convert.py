from json import load, dump


def json_to_lang(source, dest):
    content = load(source)
    dest.writelines(f'{k}={v}\t#\n' for k, v in content.items())


def lang_to_json(source, dest):
    content = dict(line[:line.find('#') - 1].strip().split("=", 1)
                   for line in source if line.strip() != '' and not line.startswith('#'))
    dump(content, dest, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType
    import sys

    def generate_parser():
        parser = ArgumentParser(
            description='A tool for converting .lang from/to .json.')
        parser.add_argument(
            "type", help="Specify conversion destination file type. Must be 'lang' or 'json'.", choices=['lang', 'json'])
        parser.add_argument("input", type=FileType(
            mode='r', encoding='utf8'), help="Path to source file.")
        parser.add_argument("-o", "--output", nargs='?', default=sys.stdout,
                            type=FileType(mode='w', encoding='utf8'), help="Path to destination file. If omitted, will write to stdout.")
        return parser
    args = generate_parser().parse_args()
    if args.type == 'lang':
        json_to_lang(args.input, args.output)
    elif args.type == 'json':
        lang_to_json(args.input, args.output)
