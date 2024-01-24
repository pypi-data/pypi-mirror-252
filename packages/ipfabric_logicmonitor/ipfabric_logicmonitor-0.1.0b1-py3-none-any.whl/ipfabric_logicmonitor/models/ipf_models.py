from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric_logicmonitor.ipf import IPFabric

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from collections import defaultdict
from typing import Optional, Any, Dict, List, Set, Union

from ipfabric.models import Device
from macaddress import MAC
from pydantic import Field, BaseModel, ConfigDict, StringConstraints
from pydantic.dataclasses import dataclass

LowerConstraint = Annotated[str, StringConstraints(to_lower=True)]


@dataclass
class ManagedIP:
    sn: str
    hostname: str
    ip: str
    mac: Optional[str] = None
    dns_name: Optional[str] = Field(None, alias="dnsName")

    def __repr__(self):
        return self.ip

    def __hash__(self):
        return hash(self.ip)

    def __eq__(self, other):
        return self.ip == other if isinstance(other, str) else other.ip


@dataclass
class ManagedIPs:
    ips: Optional[List[Union[dict, ManagedIP]]] = Field(default_factory=list)

    def __post_init__(self):
        self.ips = [ManagedIP(**i) for i in self.ips]

    @property
    def by_fqdn(self) -> Dict[str, List[ManagedIP]]:
        ips = defaultdict(list)
        for i in self.ips:
            ips[i.dns_name.lower() if i.dns_name else None].append(i)
        return ips

    @property
    def by_mac(self) -> Dict[str, List[ManagedIP]]:
        ips = defaultdict(list)
        for i in self.ips:
            ips[str(MAC(i.mac)).lower().replace("-", ":") if i.mac else None].append(i)
        return ips

    @property
    def by_sn(self) -> Dict[str, List[ManagedIP]]:
        ips = defaultdict(list)
        for i in self.ips:
            ips[i.sn].append(i)
        return ips


@dataclass
class LMAttributes:
    device_id: Optional[str] = None
    host_status: Optional[str] = None
    name: Optional[str] = None
    displayname: Optional[str] = None
    url: Optional[
        str
    ] = None  # https://ipfabricnfr.logicmonitor.com/santaba/uiv3/device/index.jsp#tree/-17-d-5
    _updates: dict = Field(default_factory=dict)

    @property
    def updates(self):
        return self._updates

    def load_lm_data(self, **kwargs):
        for k, v in kwargs.items():
            v = str(v)
            if k in self.__dict__ and self.__getattribute__(k) != v:
                self.__setattr__(k, v)
                self._updates.update({k: v})


class IPFDevice(Device, BaseModel):
    lm_attributes: Optional[LMAttributes] = Field(default_factory=LMAttributes)

    def model_post_init(self, __context: Any) -> None:
        for k, v in self.global_attributes.items():
            if (
                "LogicMonitor_" in k
                and k.replace("LogicMonitor_", "") in self.lm_attributes.__dict__
            ):
                setattr(self.lm_attributes, k.replace("LogicMonitor_", ""), v)

    @property
    def ipf_names(self) -> Set[str]:
        names = {self.hostname.lower()}
        if self.fqdn:
            names.add(self.fqdn.lower())
        if self.hostname_original:
            names.add(self.hostname_original.lower())
        return names

    def __repr__(self):
        return self.hostname

    def __hash__(self):
        return hash(self.sn)

    def __eq__(self, other):
        return self.sn == other if isinstance(other, str) else other.sn


@dataclass(config=ConfigDict(extra="ignore"))
class PhysicalDevice:
    name: str
    devices: List[IPFDevice]
    sns: Optional[Set[str]] = Field(default_factory=set)
    sn_hw: Optional[str] = None
    hostnames: Optional[Set[str]] = Field(default_factory=set)
    family: Optional[str] = None
    platform: Optional[str] = None
    model: Optional[str] = None
    site: Optional[str] = None
    version: Optional[str] = None

    def __repr__(self):
        return self.hostnames

    def __hash__(self):
        return hash(sorted(self.sns))

    def __post_init__(self):
        self.sns = {d.sn for d in self.devices}
        self.hostnames = {d.hostname for d in self.devices}
        for attr in ["sn_hw", "family", "platform", "model", "site", "version"]:
            if len({getattr(d, attr) for d in self.devices}) == 1:
                setattr(self, attr, getattr(self.devices[0], attr))
            else:
                setattr(self, attr, "Multiple")


@dataclass(config=ConfigDict(extra="ignore"))
class LogicalDevice:
    sn: Optional[str] = ""
    hostname: Optional[str] = ""
    context_name: Optional[str] = Field("", alias="contextName")
    context_id: Optional[int] = Field(None, alias="contextId")
    context_type: Optional[str] = Field("", alias="contextType")

    @property
    def name(self) -> str:
        return (
            self.hostname.replace(f"/{self.context_name}", "")
            if f"/{self.context_name}" in self.hostname
            else self.hostname
        )

    def __repr__(self):
        return self.hostname

    def __hash__(self):
        return hash(self.sn)

    def __eq__(self, other):
        return self.sn == other if isinstance(other, str) else other.sn


@dataclass
class LogicalDevices:
    devices: List[LogicalDevice]
    physical_devices: Optional[Dict[str, PhysicalDevice]] = Field(default_factory=dict)

    def create_physical_devices(self, ipf: IPFabric):
        for name in self.by_name:
            dev_sns = {d.sn for d in self.by_name[name]}
            devices = [ipf.unmatched[sn] for sn in dev_sns if sn in ipf.unmatched]
            devices.extend([ipf.matched[sn] for sn in dev_sns if sn in ipf.matched])
            devices.extend([ipf.check[sn] for sn in dev_sns if sn in ipf.check])
            device = PhysicalDevice(name=name, devices=devices)
            self.physical_devices.update({name: device})

    def _map_logical_devs(self, attr) -> Dict[str, Set[LogicalDevice]]:
        tmp = defaultdict(set)
        for d in self.devices:
            tmp[getattr(d, attr)].add(d)
        return tmp

    @property
    def by_name(self) -> Dict[str, Set[LogicalDevice]]:
        return self._map_logical_devs("name")

    @property
    def by_hostname(self) -> Dict[str, Set[LogicalDevice]]:
        return self._map_logical_devs("hostname")

    @property
    def by_sn(self) -> Dict[str, LogicalDevice]:
        return {d["sn"]: d for d in self.devices}


@dataclass
class SNMPSummary:
    sn: str
    hostname: str
    communities: int = Field(alias="communitiesCount")
    users: int = Field(alias="usersCount")
    ordered_config: Optional[List[Union[dict, ConfiguredSNMPUser]]] = Field(
        default_factory=list
    )


@dataclass(config=ConfigDict(extra="ignore"))
class SNMPUser:
    user: str
    auth: Optional[LowerConstraint] = None
    priv: Optional[LowerConstraint] = None

    def __str__(self):
        return f"{self.user}:{self.auth}:{self.priv}"

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))


@dataclass
class ConfiguredSNMPUser(SNMPUser):
    auth_token: Optional[str] = None
    priv_token: Optional[str] = None
