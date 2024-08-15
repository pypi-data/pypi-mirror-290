from .argument_parser import ArgumentParser


def subparsers(parser: ArgumentParser) -> None:
    subparser = parser.add_subparsers()

    compile_ = subparser.add_parser("compile")
    compile_.set_defaults(compile=False)
    compile_.add_argument("-y", action="store_true")

    list_ = subparser.add_parser("list")
    list_.set_defaults(list=False)

    ls = subparser.add_parser("ls")
    ls.set_defaults(ls=False)
