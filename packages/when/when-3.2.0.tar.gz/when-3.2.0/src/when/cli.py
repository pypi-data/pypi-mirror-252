#!/usr/bin/env python
import sys
import logging
import argparse

from . import core
from . import VERSION
from . import utils
from .db import make
from .config import settings, __doc__ as FORMAT_HELP

logger = logging.getLogger(__name__)


def db_main(args, db):
    value = " ".join(args.timestamp)
    if args.search:
        for row in db.search(value):
            print(", ".join(str(c) for c in row))
        return 0

    if args.alias:
        db.add_alias(value, args.alias)
        return 0

    filename = make.fetch_cities(args.size)
    admin_1 = make.fetch_admin_1()
    data = make.process_geonames_txt(filename, args.pop, admin_1)
    db.create_db(data, admin_1)
    return 0


def config_main(args):
    print(settings.write_text())
    return 0


def get_parser():
    parser = argparse.ArgumentParser(
        description="Convert times to and from time zones or cities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )

    parser.add_argument(
        "timestamp",
        default="",
        nargs="*",
        help="Timestamp to parse, defaults to local time",
    )

    parser.add_argument(
        "-h",
        "--help",
        action="store_true",
        default=False,
        help="Show helpful usage information",
    )

    parser.add_argument(
        "-s",
        "--source",
        action="append",
        help="""
            Timezone / city to convert the timestamp from, defaulting to local time
        """,
    )

    parser.add_argument(
        "-t",
        "--target",
        action="append",
        help="""
            Timezone / city to convert the timestamp to (globbing patterns allowed, can be comma
            delimited), defaulting to local time
        """,
    )

    default_format = settings["formats"]["named"]["default"]
    parser.add_argument(
        "-f",
        "--format",
        default=default_format,
        help="Output formatting. Additional formats can be shown using the -v option with -h",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        default=False,
        help="Show times in all common timezones",
    )

    parser.add_argument("--holidays", help="Show holidays for given country code.")

    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc). Use -v to show `when` extension detailed help",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=VERSION),
    )

    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output results in nicely formatted JSON",
    )

    # config options
    parser.add_argument(
        "--config",
        action="store_true",
        default=False,
        help="Toggle config mode. With no other option, dump current configuration settings",
    )

    # DB options
    parser.add_argument(
        "--db",
        action="store_true",
        default=False,
        help="Togge database mode, used with --search, --alias, --size, and --pop",
    )

    parser.add_argument(
        "--search",
        action="store_true",
        default=False,
        help="Search database for the given city (used with --db)",
    )
    parser.add_argument(
        "--alias", type=int, help="(Used with --db) Create a new alias from the city id"
    )

    parser.add_argument(
        "--size",
        default=15_000,
        type=int,
        help="(Used with --db) Geonames file size. Can be one of {}. ".format(
            ", ".join(str(i) for i in make.CITY_FILE_SIZES)
        ),
    )

    parser.add_argument(
        "--pop",
        default=10_000,
        type=int,
        help="(Used with --db) City population minimum.",
    )

    return parser


def log_config(verbosity):
    log_level = logging.WARNING
    log_format = "[%(levelname)s]: %(message)s"
    if verbosity:
        log_format = "[%(levelname)s %(name)s:%(lineno)d]: %(message)s"
        log_level = logging.DEBUG if verbosity > 1 else logging.INFO

    logging.basicConfig(level=log_level, format=log_format, force=True)
    logger.debug("Configuration files read: %s", ", ".join(settings.read_from))


def main(sys_args, when=None):
    debug = "--pdb" in sys_args
    if debug:
        sys_args.remove("--pdb")

    parser = get_parser()
    args = parser.parse_args(sys_args)

    if debug:
        try:
            import ipdb as pdb
        except ImportError:
            import pdb
        pdb.set_trace()

    log_config(args.verbosity)
    if args.help:
        parser.print_help()
        if args.verbosity:
            print(FORMAT_HELP)
        else:
            print("\nUse -v option for details\n")
        sys.exit(0)

    when = when or core.When()
    targets = utils.all_zones() if args.all else args.target

    if args.db:
        return db_main(args, when.db)
    elif args.config:
        return config_main(args)
    elif args.holidays:
        return core.holidays(args.holidays, args.timestamp[0] if args.timestamp else None)
    elif args.json:
        print(when.as_json(args.timestamp, targets, args.source, indent=2))
    else:
        formatter = core.Formatter(args.format)
        try:
            for output in when.format_results(formatter, args.timestamp, args.source, targets):
                print(output)
        except core.UnknownSourceError as e:
            print(e, file=sys.stderr)
            return 1

    return 0
