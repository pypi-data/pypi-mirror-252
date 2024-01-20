# Copyright (c) 2021, 2022, 2023, Panagiotis Tsirigotis

# This file is part of linuxnet-iptables.
#
# linuxnet-iptables is free software: you can redistribute it and/or
# modify it under the terms of version 3 of the GNU Affero General Public
# License as published by the Free Software Foundation.
#
# linuxnet-iptables is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General
# Public License along with linuxnet-iptables. If not, see
# <https://www.gnu.org/licenses/>.

"""
This module provides the SnatTarget and DnatTarget classes which
provide access to the SNAT and DNAT iptables targets respectively.
"""

from ipaddress import IPv4Address
from typing import List, Optional, Tuple

from ..deps import get_logger
from ..exceptions import IptablesError, IptablesParsingError

from .target import Target, TargetParser

_logger = get_logger("linuxnet.iptables.target.nattarget")


class _NatTarget(Target):
    """This class provides access to the ``SNAT/DNAT`` targets.
    """
    def __init__(self, *, nat_target: str, nat_option: str,
                        addr: Optional[IPv4Address],
                        port: Optional[int], last_port: Optional[int],
                        is_random: bool, is_persistent: bool):
        super().__init__(nat_target, terminates=True)
        self.__nat_option = nat_option
        self.__addr = addr
        self.__port = port
        self.__last_port = last_port
        self.__is_random = is_random
        self.__is_persistent = is_persistent

    def get_address(self) -> Optional[IPv4Address]:
        """Returns the address used as the new
        source address (in the case of ``SNAT``) or destination
        address (in the case ``DNAT``).
        """
        return self.__addr

    def set_address(self, addr: IPv4Address) -> None:
        """Set the address
        """
        self.__addr = addr

    def get_ports(self) -> Tuple[Optional[int], Optional[int]]:
        """Returns the port range used for NATing.
        """
        return (self.__port, self.__last_port)

    def set_port(self, port: int) -> None:
        """Set the port
        """
        self.__port = port

    def set_port_range(self, port: int, last_port: int) -> None:
        """Set the port range
        """
        self.__port = port
        self.__last_port = last_port

    def is_persistent(self) -> bool:
        """Returns ``True`` when persistent port mapping is enabled
        """
        return self.__is_persistent

    def is_random(self) -> bool:
        """Returns ``True`` when random port mapping is enabled
        """
        return self.__is_random

    def set_persistent(self) -> None:
        """Enable persistent port mapping
        """
        self.__is_persistent = True

    def set_random(self) -> None:
        """Enable randomized port mapping
        """
        self.__is_random = True

    def to_iptables_args(self) -> List[str]:
        """Returns a list of **iptables(8)** arguments
        """
        if self.__addr is None and self.__port is None:
            raise IptablesError('addr/port both None')
        retval = super().to_iptables_args()
        dest_spec = ''
        if self.__addr is not None:
            dest_spec += str(self.__addr)
        if self.__port is not None:
            dest_spec += f':{self.__port:d}'
            if self.__last_port is not None:
                dest_spec += f'-{self.__last_port:d}'
        retval += [self.__nat_option, dest_spec]
        if self.__is_random:
            retval.append('--random')
        if self.__is_persistent:
            retval.append('--persistent')
        return retval

    @staticmethod
    def _parse_nat(target_name: str, field_iter):
        """Parse the [SD]NAT target options
        Returns a kwargs dictionary
        """
        # pylint: disable=too-many-branches
        # The iterator moved just past the 'to:' field; retrieve that field.
        val = field_iter.rewind().next_field()
        if not val:
            return None
        kwargs = {}
        try:
            values = val.split(':')
            if len(values) == 2:
                addr_spec = values[1]
                port_spec = None
            elif len(values) == 3:
                addr_spec = values[1]
                port_spec = values[2]
            else:
                raise IptablesParsingError(f'bad DNAT dest spec: {val}')
            if '-' in addr_spec:
                raise IptablesParsingError("IP address range not supported")
            if addr_spec:
                kwargs['addr'] = IPv4Address(addr_spec)
            if port_spec is not None:
                if '-' in port_spec:
                    port_str, last_port_str = port_spec.split('-', 1)
                    kwargs['port'] = int(port_str)
                    kwargs['last_port'] = int(last_port_str)
                elif port_spec:
                    kwargs['port'] = int(port_spec)
        except Exception as ex:
            raise IptablesParsingError(
                        f'bad {target_name} dest spec: {val}') from ex
        for val in field_iter:
            if val == 'random':
                kwargs['is_random'] = True
            elif val == 'persistent':
                kwargs['is_persistent'] = True
            else:
                raise IptablesParsingError(
                        f'unknown {target_name} argument: {val}')
        return kwargs
        # pylint: enable=too-many-branches


class SnatTarget(_NatTarget):
    """This class provides access to the ``SNAT`` target
    """
    def __init__(self, *, addr: Optional[IPv4Address] =None,
                    port: Optional[int] =None, last_port: Optional[int] =None,
                    is_random=False, is_persistent=False):
        """
        :param addr: an :class:`IPv4Address` object
        :param port: port number (integer)
        :param last_port: port number (integer) used when defining
            a port range
        :param is_random: if ``True``, use the **iptables(8)**
            ``--random`` option
        :param is_persistent: if ``True``, use the **iptables(8)**
            ``--persistent`` option
        """
        super().__init__(nat_target='SNAT', nat_option='--to-source',
                        addr=addr, port=port, last_port=last_port,
                        is_random=is_random, is_persistent=is_persistent)

    @classmethod
    def parse(cls, field_iter) -> Target:
        """Parse the ``SNAT`` target options

        :meta private:
        """
        kwargs = cls._parse_nat('SNAT', field_iter)
        if kwargs is None:
            return None
        return SnatTarget(**kwargs)


class DnatTarget(_NatTarget):
    """This class provides access to the ``DNAT`` target
    """
    def __init__(self, *, addr=None, port=None, last_port=None,
                        is_random=False, is_persistent=False):
        """
        :param addr: an :class:`IPv4Address` object
        :param port: port number (integer)
        :param last_port: port number (integer) used when defining
            a port range
        :param is_random: if ``True``, use the **iptables(8)**
            ``--random`` option
        :param is_persistent: if ``True``, use the **iptables(8)**
            ``--persistent`` option
        """
        super().__init__(nat_target='DNAT', nat_option='--to-destination',
                        addr=addr, port=port, last_port=last_port,
                        is_random=is_random, is_persistent=is_persistent)

    @classmethod
    def parse(cls, field_iter) -> Target:
        """Parse the ``DNAT`` target options

        :meta private:
        """
        kwargs = cls._parse_nat('DNAT', field_iter)
        if kwargs is None:
            return None
        return DnatTarget(**kwargs)


TargetParser.register_target('SNAT', SnatTarget, 'to:', prefix_match=True)
TargetParser.register_target('DNAT', DnatTarget, 'to:', prefix_match=True)
