"""Class used for mounting iso images."""
import crypt
import hashlib
import logging
import shlex
import shutil
import subprocess

from dataclasses import dataclass
from ipaddress import IPv4Interface, IPv4Address
from pathlib import Path
from typing import Optional

from isobuilder.constants import (
    AUTHORIZED_KEYS,
    ISOLINUX_CFG,
    TXT_CFG,
    GRUB,
    PRESEED,
    LATE_COMMAND,
)


class IsoBuilderError(Exception):
    """Raise by the IsoBuilder class."""


@dataclass
class IsoBuilderHost:
    """Dataclass to hold config data for the host

    Arguments:
        fddn: the host fqdn
        ipaddress: the host ip address
        netmask: the host netmask
        gateway: the host default gateway
        ipv4_primary: the host ipv4 primary interface
        ipv6_primary: the host ipv6 primary interface
    """
    fqdn: str
    ipaddress: IPv4Interface
    gateway: IPv4Address
    ipv4_primary: str
    ipv6_primary: Optional[str] = None


@dataclass
class IsoBuilderDirs:
    """Data class to hole the directories for the IsoBuilder

    Arguments:
        source_iso: Path to the source iso image
        source_mount: The location to mount the source iso image
        build_dir: directory used for building the custom image
        output_dir: The location to store the resulting iso

    """
    source_iso: Path
    source_mount: Path
    build_dir: Path
    output_dir: Path


class IsoBuilder:
    """Class for building imrs ISOs."""

    def __init__(
        self,
        host: IsoBuilderHost,
        drac_password: str,
        dirs: IsoBuilderDirs,
    ):
        """Main init class

        Arguments:
            host: Object containing the configuration for the host
            drac_password: the drac password is used as a seed for the root password
            dirs: dataclass holding all the dirs we need

        """
        self.logger = logging.getLogger(__name__)
        self.host = host
        self._drac_password = drac_password
        self._dirs = dirs
        self.output_iso = dirs.output_dir / f"{host.fqdn}.iso"

    def _run_command(
        self, command: str, capture_output: bool = False
    ) -> subprocess.CompletedProcess:
        """Run a cli command.

        Arguments:
            command: the command to run

        """
        self.logger.debug("%s: running command: %s", self.host.fqdn, command)
        try:
            # use capture_output=capture_output when using python3.7
            return subprocess.run(
                shlex.split(command), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as error:
            raise IsoBuilderError(f"{command}: failed to execute: {error}") from error

    def mount_iso(self) -> None:
        """Mount the iso image"""
        self._dirs.source_mount.mkdir(parents=True, exist_ok=True)
        self._run_command(f"fusermount -u {self._dirs.source_mount}")
        self._run_command(f"fuseiso {self._dirs.source_iso} {self._dirs.source_mount}")

    def sync_build_dir(self) -> None:
        """Sync the source iso image into a build directory."""
        # TODO: no need to cast on 3.7 when python3.7
        shutil.rmtree(str(self._dirs.build_dir), ignore_errors=True)
        self._dirs.build_dir.mkdir(parents=True, exist_ok=True)
        self._run_command(f"rsync -a {self._dirs.source_mount}/ {self._dirs.build_dir}")

    def write_custom_files(self) -> None:
        """Update the build dir with custom files."""
        (self._dirs.build_dir / "dns0ps").mkdir(parents=True, exist_ok=True)
        root_password = hashlib.md5(f"{self.host.fqdn}:{self._drac_password}".encode()).hexdigest()
        root_password_hash = crypt.crypt(
            root_password, crypt.mksalt(crypt.METHOD_SHA512)
        )
        hostname, domain = self.host.fqdn.split(".", 1)
        late_command = LATE_COMMAND.format(
            hostname=hostname, ipv6_primary=self.host.ipv6_primary
        )
        preeseed = PRESEED.format(
            hostname=hostname,
            domain=domain,
            password=root_password_hash,
            late_command=late_command,
        )
        (self._dirs.build_dir / "preseed" / "dnsops.seed").write_text(preeseed)
        (self._dirs.build_dir / "dns0ps" / "authorized_keys").write_text(AUTHORIZED_KEYS)
        (self._dirs.build_dir / "dns0ps" / "grub").write_text(GRUB)

    def write_ioslinux_files(self) -> None:
        """ "Write the files required for iso linux"""
        txt_cfg = TXT_CFG.format(
            interface=self.host.ipv4_primary,
            ipaddress=self.host.ipaddress.ip,
            netmask=self.host.ipaddress.netmask,
            gateway=self.host.gateway,
        )
        shutil.copy(
            "/usr/lib/syslinux/modules/bios/menu.c32",
            str(self._dirs.build_dir / "isolinux"),
        )
        (self._dirs.build_dir / "isolinux" / "isolinux.cfg").write_text(ISOLINUX_CFG)
        (self._dirs.build_dir / "isolinux" / "txt.cfg").write_text(txt_cfg)

    def mkiso(self) -> None:
        """Make the iso image."""
        try:
            self.output_iso.unlink()
        except FileNotFoundError:
            # TODO: on python3.7 us missing_ok=True
            pass
        command = """mkisofs -r -V "DNSEng Media" -cache-inodes, -J -l -b \
                isolinux/is  olinux.bin -c isolinux/boot.cat \
                -no-emul-boot -boot-load-size 4 -boot-info-table -o \
                {self.output_iso} {self._dirs.build_dir}"""
        self._run_command(command)

    def build(self) -> None:
        """Run all the bits to generate the iso."""
        self.mount_iso()
        self.sync_build_dir()
        self.write_custom_files()
        self.write_ioslinux_files()
        self.mkiso()
        print(f"{self.host.fqdn}: ISO has been generated and avalible at: {self.output_iso}")
