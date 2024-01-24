from ipaddress import IPv4Address, AddressValueError
from typing import Optional
from typing import Union, Tuple, Set

from logicmonitor_sdk.models.device import Device
from pydantic import Field, ConfigDict, field_validator
from pydantic.dataclasses import dataclass


@dataclass(config=ConfigDict(extra="ignore"))
class AutoProperties:
    network_address: Optional[str] = ""
    network_mac_address: Optional[str] = ""
    network_names: Optional[Union[str, set]] = None
    system_name: Optional[str] = ""
    endpoint_serial_number: Optional[str] = ""
    entphysical_serialnum: Optional[str] = ""

    @field_validator("network_names")
    @classmethod
    def split_network_names(cls, v) -> set:
        if not v or isinstance(v, set):
            return v
        return set(v.split(","))


@dataclass(config=ConfigDict(extra="ignore"))
class SystemProperties:
    groups: set = Field(default_factory=set)
    version: Optional[str] = ""
    sysname: Optional[str] = ""
    hostname: Optional[str] = ""


@dataclass(config=ConfigDict(extra="ignore"))
class IPFProperties:
    sn: Optional[str] = None
    sns: Optional[str] = None
    sn_hw: Optional[str] = None
    hostname: Optional[str] = None
    hostnames: Optional[str] = None
    family: Optional[str] = None
    platform: Optional[str] = None
    model: Optional[str] = None
    site_name: Optional[str] = None
    version: Optional[str] = None
    last_snapshot_id: Optional[str] = None
    last_snapshot_timestamp: Optional[str] = None
    first_snapshot_id: Optional[str] = None
    first_snapshot_timestamp: Optional[str] = None
    _updates: dict = Field(default_factory=dict)

    @property
    def updates(self):
        return self._updates

    def load_ipf_data(self, **kwargs):
        if "hostnames" in kwargs:
            self.hostnames = ",".join(kwargs.pop("hostnames"))
        if "sns" in kwargs:
            self.hostnames = ",".join(kwargs.pop("sns"))
        for k, v in kwargs.items():
            if k in self.__dict__ and self.__getattribute__(k) != v:
                self.__setattr__(k, v)
                self._updates.update({k: v})
        if not self.first_snapshot_id and self.last_snapshot_id:
            self.first_snapshot_id = self.last_snapshot_id
            self.first_snapshot_timestamp = self.last_snapshot_timestamp
            self._updates.update(
                {
                    "first_snapshot_id": self.first_snapshot_id,
                    "first_snapshot_timestamp": self.first_snapshot_timestamp,
                }
            )


class LMDevice(Device):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ipf_properties: IPFProperties = self.load_ipf_properties()
        self.auto: AutoProperties = AutoProperties(
            **{
                p["name"].split(".", 1)[1].replace(".", "_"): p["value"]
                for p in self.auto_properties
            }
        )
        self.sys: SystemProperties = self.load_sys_properties()

    def load_ipf_properties(self) -> IPFProperties:
        props = IPFProperties()
        for prop in self.custom_properties:
            name = prop["name"].split(".")
            if name[0] == "ipfabric":
                props.__setattr__(name[1], prop["value"])
        return props

    def load_sys_properties(self) -> SystemProperties:
        props = SystemProperties()
        for prop in self.system_properties:
            name = prop["name"].split(".", 1)[1].replace(".", "_")
            if name == "groups":
                props.groups = set(prop["value"].split(","))
            elif name in props.__dict__:
                setattr(props, name, prop["value"])
        return props

    @staticmethod
    def _parse_lm_names(
        obj, names: list, lm_names: set, lm_ips: set
    ) -> Tuple[Set[str], Set[str]]:
        def check_ip(v):
            try:
                IPv4Address(v)
                lm_ips.add(v)
            except AddressValueError:
                lm_names.add(v.lower())

        for name in names:
            value = getattr(obj, name)
            if not value:
                continue
            if isinstance(value, str):
                check_ip(value)
            if isinstance(value, (list, set)):
                [check_ip(i) for i in value]
        return lm_names, lm_ips

    @property
    def lm_names_ips(self):
        lm_names, lm_ips = self._parse_lm_names(
            self.sys, ["hostname", "sysname"], set(), set()
        )
        lm_names, lm_ips = self._parse_lm_names(
            self.auto, ["system_name", "network_names"], lm_names, lm_ips
        )
        lm_names, lm_ips = self._parse_lm_names(
            self, ["name", "display_name"], lm_names, lm_ips
        )
        if self.auto.network_address:
            lm_ips.add(self.auto.network_address)
        return lm_names, lm_ips

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other if isinstance(other, int) else other.id

    def __repr__(self):
        return self.display_name
