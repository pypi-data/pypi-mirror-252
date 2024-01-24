from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric_logicmonitor import LogicMonitor

from ipfabric import IPFClient
from dataclasses import dataclass, field
from ipfabric_logicmonitor.models import (
    ManagedIPs,
    IPFDevice,
    LogicalDevices,
)
from collections import defaultdict
from typing import Dict, Set
from ipfabric_logicmonitor.tools import add_attributes, extra_checks
import logging


logger = logging.getLogger(__name__)


@dataclass
class IPFabric:
    _sdk: IPFClient = None
    _unmatched: Dict[str, IPFDevice] = field(default_factory=dict)
    _matched: Dict[str, IPFDevice] = field(default_factory=dict)
    _check: Dict[str, IPFDevice] = field(default_factory=dict)
    _managed_ips: ManagedIPs = None
    _logical_devs: LogicalDevices = None
    _hw_sn: Dict[str, Set[str]] = field(default_factory=dict)

    @property
    def sdk(self) -> IPFClient:
        return self._sdk

    @property
    def unmatched(self) -> Dict[str, IPFDevice]:
        return self._unmatched

    @property
    def matched(self) -> Dict[str, IPFDevice]:
        return self._matched

    @property
    def check(self) -> Dict[str, IPFDevice]:
        return self._check

    @property
    def managed_ips(self) -> ManagedIPs:
        return self._managed_ips

    @property
    def logical_devs(self) -> LogicalDevices:
        return self._logical_devs

    @property
    def hw_sn(self) -> Dict[str, Set[str]]:
        return self._hw_sn

    def configure(self, ipf_resource: dict):
        self._sdk = IPFClient(
            base_url=ipf_resource["base_url"],
            auth=ipf_resource["auth"],
            verify=ipf_resource.get("verify", True),
            timeout=ipf_resource.get("timeout", 5.0),
        )

        self._unmatched = {
            k: IPFDevice(**v.model_dump(by_alias=True))
            for k, v in self.sdk.devices.by_sn.items()
        }
        self._check = self._has_lm_device_id()
        self._managed_ips = ManagedIPs(
            self.sdk.technology.addressing.managed_ip_ipv4.all(
                columns=["sn", "hostname", "dnsName", "ip", "mac"]
            )
        )
        self._logical_devs: LogicalDevices = LogicalDevices(
            devices=self.sdk.technology.platforms.logical_devices.all()
        )
        self.logical_devs.create_physical_devices(self)
        self._hw_sn = self._load_hw_info()

    def _has_lm_device_id(self) -> Dict[str, IPFDevice]:
        """Check IP Fabric Attributes if it was assigned to a LM Device ID"""
        check = dict()
        for k, v in self.unmatched.copy().items():
            if v.lm_attributes.device_id:
                check[k] = self.unmatched.pop(k)
        return check

    def _load_hw_info(self) -> Dict[str, Set[str]]:
        """Gets IPF Inventory > Parts data to match serial numbers to LM"""
        sn_hw = defaultdict(set)
        for part in self.sdk.inventory.pn.all(
            columns=["deviceSn", "sn"], filters={"sn": ["empty", False]}
        ):
            sn_hw[part["sn"].lower()].add(part["deviceSn"])
        return sn_hw

    @property
    def snapshot_meta(self) -> Dict[str, str]:
        return dict(
            last_snapshot_id=self.sdk.snapshot.snapshot_id,
            last_snapshot_timestamp=self.sdk.snapshot.end.isoformat(),
        )

    def initial_attribute_matching(self, lm: LogicMonitor):
        """Step 2: Initial matching to check if IPF devices assigned an LM ID has a device in LogicMonitor"""
        for sn in self.check.copy():
            ipf_dev = self.check.pop(sn)
            lm_id = int(ipf_dev.lm_attributes.device_id)
            if lm_id in lm.unmatched_by_id and extra_checks(
                lm.unmatched_by_id[lm_id], ipf_dev, self
            ):
                lm_dev = lm.unmatched_by_id[lm_id]
                lm.unmatched.remove(lm_dev)
                self.matched[sn], lm.matched[sn] = ipf_dev, lm_dev
                add_attributes(lm_dev, ipf_dev, self.snapshot_meta)
                logger.debug(
                    f"Matched IPF Device '{ipf_dev.hostname}/{sn}' to LM Device '{lm_dev.display_name}/{lm_dev.id}'."
                )
            else:
                self.unmatched[sn] = ipf_dev
                logger.warning(
                    f"IPF Device '{ipf_dev.hostname}/{sn}' not found in LogicMonitor will try to add."
                )
