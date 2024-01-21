import sys
import os
from tempfile import NamedTemporaryFile
from sys import _getframe, stderr
from functools import partial
from omniblack.entry import entry
from omniblack.model import Field, Model
from abc import ABC, abstractmethod
from importlib import metadata
from argparse import (
    ArgumentParser,
    BooleanOptionalAction,
    RawDescriptionHelpFormatter,
)

from public import public


class ModelCliType:
    def __init__(self, field: Field):
        self.__field = field
        self.__model = self.__field.model

    def __repr__(self):
        return self.__field.type.name

    def __call__(self, value: str):
        return self.__model.types.from_format('string', value, self.__field)


internal_errors = (
    ImportError,
    NotImplementedError,
    NameError,
    SyntaxError,
    IndentationError,
    SystemError,
)

stderr_print = partial(print, file=stderr)


class HasExitCode(ABC):
    @abstractmethod
    def exit_code(self) -> int:
        ...


def create_parser(model: Model, entry_obj: entry) -> ArgumentParser:
    parser = ArgumentParser(
        description=entry_obj.short_desc,
        epilog=entry_obj.long_desc,
        formatter_class=RawDescriptionHelpFormatter,
    )

    for field in entry_obj.fields:
        add_field(parser, field)

    return parser


@public
class CLI:
    """
    A command-line interface application.

    :param model: The model that will be used to parse parameters.
    :type model: :type:`omniblack.model.Model`

    :param package: The package that contains the cli.
        This will be used to get the package's version,
        description and summary.
        If not provided CLI will attempt to get the package
        using :py:func:`sys._getframe(1) <sys._getframe>`.
    :type package: :type:`str`

    :param version: The version of this application.
        Will be derived using :code:`package`.
    :type version: :type:`str`
    """

    def __init__(self, model, package=None, version=None):

        self.functions = {}

        if package is None:
            frame = _getframe(1)
            if spec := frame.f_globals['__spec__']:
                package = spec.parent
            elif pkg := frame.f_globals['__package__']:
                package = pkg

        if package is not None:
            self.package = package
        else:
            raise ValueError("Could not determine package containing the cli.")

        if version is None and package is not None:
            version = metadata.version(package)

        self.version = version
        self.model = model
        self._create_root_parser()

    def _create_root_parser(self):
        meta = metadata.metadata(self.package)
        root_parser = ArgumentParser(
            description=meta.get('Summary', ''),
            epilog=meta.get('Description', ''),
        )

        if self.version:
            root_parser.add_argument(
                '--version',
                action='version',
                version=self.version,
            )

        return root_parser

    def print_all_help(self, root_parser, sub_parsers):
        blobs = []
        blobs.append(root_parser.format_help())

        for sub_parser in sub_parsers:
            blobs.append(sub_parser.format_help())

        full_text = hr().join(blobs)

        print(full_text)
        sys.exit(0)

    def __call__(self, *args):
        root_parser = self._create_root_parser()

        if len(self.functions) == 1:
            name, = tuple(self.functions)
            func_entry = self.functions[name]

            root_parser.set_defaults(entry=func_entry)

            sub_parsers = []
            for field in func_entry.fields:
                add_field(root_parser, field)
        else:
            sub_parsers = self._add_subparsers(root_parser)

        args = root_parser.parse_args()

        if getattr(args, 'help_all', False):
            self.print_all_help(root_parser, sub_parsers)

        try:
            delattr(args, 'help_all')
        except AttributeError:
            pass

        target_entry = args.entry
        del args.entry
        self.__call_entry(target_entry, args)

    def __call_entry(self, entry, args):
        try:
            ret = entry.func(**vars(args))
        except OSError as err:
            stderr_print(err.strerror, err.filename, err.filename2)
            sys.exit(err.errno)
        except EOFError as err:
            print(*err.args)
            sys.exit(os.EX_DATAERR)
        except PermissionError as err:
            stderr_print(*err.args)
            sys.exit(os.EX_NOPERM)
        except internal_errors as err:
            stderr_print('An internal error occured.')
            with NamedTemporaryFile('wx', delete=False) as file:
                stderr_print(f'See {file.name} for details')
                print(*err.args, file=file)

            sys.exit(1)
        else:
            if ret is None:
                sys.exit(os.EX_OK)
            elif isinstance(ret, int):
                sys.exit(ret)
            elif isinstance(ret, HasExitCode):
                if hasattr(ret, 'exit_message'):
                    stderr_print(ret.exit_message())

                sys.exit(ret.exit_code())

            else:
                try:
                    exit_code = int(ret)
                except Exception:
                    pass
                else:
                    sys.exit(exit_code)

    def _add_subparsers(self, root_parser):
        root_parser.add_argument(
            '--help-all',
            action='store_true',
            dest='help_all',
            help='Print help for all subcommands.',
        )

        sub_parsers = root_parser.add_subparsers(
            title='subcommand',
            description='Subcommands available in %(prog)s',
        )

        all_sub_parsers = []
        for func_name, func_entry in self.functions.items():
            sub_parser = sub_parsers.add_parser(
                func_name.replace('_', '-'),
                formatter_class=RawDescriptionHelpFormatter,
                help=func_entry.short_desc,
                description=func_entry.short_desc,
                epilog=func_entry.long_desc,
            )

            all_sub_parsers.append(sub_parser)

            sub_parser.set_defaults(entry=func_entry)

            for field in func_entry.fields:
                add_field(sub_parser, field)

        return all_sub_parsers

    def command(self, func):
        func_entry = entry(self.model, func)

        self.functions[func_entry.name] = func_entry

        return func


def add_field(parser: ArgumentParser, field: Field):
    name = field.field_def.name
    pos_name = name.replace('_', '-')

    extra_args = dict()

    required = field.field_def.required
    if not required:
        if 'assumed' in field.field_def:
            extra_args['default'] = field.field_def.assumed
        else:
            extra_args['default'] = None

    if 'desc' in field.field_def:
        extra_args['help'] = field.field_def.desc.en

    if field.field_def.list:
        extra_args['nargs'] = '*' if required else '+'

    if field.field_def.type == 'boolean':
        extra_args.setdefault('default', False)

        parser.add_argument(
            f'--{pos_name}',
            dest=name,
            **extra_args,
            action=BooleanOptionalAction,
        )
    else:
        if 'assumed' in field.field_def:
            name = f'--{pos_name}'
            extra_args['dest'] = name

        parser.add_argument(
            name,
            **extra_args,
            type=ModelCliType(field),
        )


def hr():
    columns, _rows = os.get_terminal_size(0)
    return ('-' * columns)
