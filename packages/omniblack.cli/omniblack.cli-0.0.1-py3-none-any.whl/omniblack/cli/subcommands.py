from importlib.metadata import entry_points, metadata, version, EntryPoint
from types import ModuleType
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from omniblack.cli import add_field
from omniblack.entry import entry
from omniblack.model import Model


class Temp:
    def __init__(self, *args):
        self.args = args

    def __getattr__(self, name):
        return Temp(*self.args, name)

    def __call__(self):
        eps = entry_points()
        subcommands = eps.select(group='omniblack.cli')
        full_package = '.'.join(self.args)

        models = eps.select(group='omniblack.model', name='main')

        model, *_ = (
            model_entry
            for model_entry in models
            if model_entry.module.startswith(full_package)
        )

        subcommands = {
            subcommand.name: self._subcommand_from_entry(subcommand, model)
            for subcommand in subcommands
            if subcommand.module.startswith(full_package)
        }

        meta = metadata(full_package)
        ver = version(full_package)

        parser = self.create_parser(meta, ver, subcommands, model)
        args = parser.parse_args()
        subcommand_name = args.subcommand
        del args.subcommand
        subcommand = subcommands[subcommand_name]

        return subcommand.func(**vars(args))

    def create_parser(self, meta, ver, subcommands, model):
        parser = ArgumentParser(
            description=meta['Summary'],
            epilog=meta['Description'],
        )

        parser.add_argument(
            '--version',
            action='version',
            version=ver,
        )

        subcommand_help = ', '.join(subcommands)

        sub_parsers = parser.add_subparsers(
            dest='subcommand',
            metavar='subcommand',
            help='{' + subcommand_help + '}',
        )

        for name, subcommand in subcommands.items():
            sub_parser = sub_parsers.add_parser(
                name,
                formatter_class=RawDescriptionHelpFormatter,
                description=subcommand.short_desc,
                epilog=subcommand.long_desc,
            )

            for field in subcommand.fields:
                add_field(sub_parser, field)

        return parser

    def _subcommand_from_entry(self, entry_obj: EntryPoint, model: Model):
        func = entry_obj.load()

        if isinstance(func, ModuleType):
            func = func.__main__

        return entry(model, func)


def __getattr__(name):
    return Temp(name)
