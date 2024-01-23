# /usr/bin/env python3
"""CLi too for building ISOs"""
import logging

from argparse import ArgumentParser, Namespace
from ipaddress import IPv4Interface, IPv4Address
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from isobuilder import IsoBuilder, IsoBuilderDirs, IsoBuilderHost, IsoBuilderError

logger = logging.getLogger(__name__)


def get_args(args: Optional[List] = None) -> Namespace:
    """Parse and return the arguments.

    Returns:
        Namespace: The parsed argument namespace
    """
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-P', '--drac-password', default='calvin')
    parser.add_argument('--source-mount', default='/tmp/cdrom/', type=Path)
    parser.add_argument('--build-dir', default='/tmp/build/', type=Path)
    parser.add_argument('-d', '--nodes-dir', type=Path, default='/etc/hieradata/nodes')
    parser.add_argument(
        '-i',
        '--source-iso',
        default='/etc/puppetlabs/installer/remote/default.iso',
        type=Path,
    )
    parser.add_argument(
        '-o', '--output-dir', default='/etc/puppetlabs/installer/remote/', type=Path
    )
    parser.add_argument('node')
    if args is None:  # pragma: no cover
        return parser.parse_args()
    return parser.parse_args(args)


def get_log_level(args_level: int) -> int:
    """Convert an integer to a logging log level.

    Arguments:
        args_level (int): The log level as an integer

    Returns:
        int: the logging loglevel
    """
    return {
        0: logging.ERROR,
        1: logging.WARN,
        2: logging.INFO,
        3: logging.DEBUG,
    }.get(args_level, logging.DEBUG)


def get_primary_int(network_data: Dict, address_family: int) -> Optional[str]:
    """Parse the network_data and return the primary ip interface.

    The primary interface is which ever interfaces as the default gateway

    Arguments:
        network_data: dictionary of network data
        address_family: the address family either 4 or 6

    Returns:
        the primary interface.

    """
    for interface, config in network_data.items():
        if f'gw{address_family}' in config:
            if config[f'gw{address_family}']:
                return interface
    return None


def main() -> int:  # pragma: no cover
    """Main program Entry point.

    Returns:
        int: the status return code
    """
    args = get_args()
    logging.basicConfig(level=get_log_level(args.verbose))
    node_path = args.nodes_dir / f"{args.node}.yaml"
    if not node_path.is_file():
        logging.error("%s: no such file. Please generate the config first", node_path)
        return 1

    yaml_data = yaml.safe_load(node_path.read_text())
    ipv4_primary = get_primary_int(yaml_data['network::interfaces'], 4)
    if ipv4_primary is None:
        logging.error("%s: unable to find ipv4 primary interface", node_path)
        return 1

    ipv6_primary = get_primary_int(yaml_data['network::interfaces'], 6)
    ipaddress = IPv4Interface(yaml_data['network::interfaces'][ipv4_primary]['addr4'])
    gateway = IPv4Address(yaml_data['network::interfaces'][ipv4_primary]['gw4'])

    iso_host = IsoBuilderHost(
        fqdn=args.node,
        ipaddress=ipaddress,
        gateway=gateway,
        ipv4_primary=ipv4_primary,
        ipv6_primary=ipv6_primary,
    )
    iso_dirs = IsoBuilderDirs(
        source_iso=args.source_iso,
        source_mount=args.source_mount,
        build_dir=args.build_dir,
        output_dir=args.output_dir,
    )
    iso_builder = IsoBuilder(
        host=iso_host,
        dirs=iso_dirs,
        drac_password=args.drac_password,
    )
    try:
        iso_builder.build()
    except IsoBuilderError as error:
        logger.error("%s: error occurred building\n%s", args.node, error)
        return 1

    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
