from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric_logicmonitor import IPFabric

from dataclasses import dataclass, field
from ipfabric_logicmonitor.tools import add_attributes, extra_checks, lm_pager
from ipfabric_logicmonitor.models import LMDevice
import logicmonitor_sdk
from typing import Dict, Set

import logging
import re


logger = logging.getLogger(__name__)
FQDN_RE = re.compile(
    r"(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}\.?$)"
)


@dataclass
class LogicMonitor:
    snapshot_id: str
    _sdk: logicmonitor_sdk.LMApi = None
    _all_devs_by_id: Dict[int, LMDevice] = field(default_factory=dict)
    _unmatched: Set[LMDevice] = field(default_factory=set)
    _matched: Dict[str, LMDevice] = field(default_factory=dict)
    _check: Dict[str, LMDevice] = field(default_factory=dict)

    @property
    def sdk(self) -> logicmonitor_sdk.LMApi:
        return self._sdk

    @property
    def all_devs_by_id(self) -> Dict[int, LMDevice]:
        return self._all_devs_by_id

    @property
    def unmatched(self) -> Set[LMDevice]:
        return self._unmatched

    @property
    def matched(self) -> Dict[str, LMDevice]:
        return self._matched

    @property
    def check(self) -> Dict[str, LMDevice]:
        return self._check

    @property
    def unmatched_by_id(self) -> Dict[int, LMDevice]:
        return {d.id: d for d in self.unmatched}

    def configure(self, lm_resource: dict):
        cfg = logicmonitor_sdk.Configuration()
        cfg.company = lm_resource["company"]
        cfg.access_id = lm_resource["access_id"]
        cfg.access_key = lm_resource["access_key"]
        self._sdk = logicmonitor_sdk.LMApi(logicmonitor_sdk.ApiClient(cfg))
        self._load_lm_devices()

    def _load_lm_devices(self):
        for dev in [
            LMDevice(**d.to_dict())
            for d in lm_pager(self.sdk.get_device_list_with_http_info)
        ]:
            self.all_devs_by_id[dev.id] = dev
            if dev.ipf_properties.sn:
                self.check.update({dev.ipf_properties.sn: dev})
            elif dev.ipf_properties.sns:
                for sn in dev.ipf_properties.sns.split(","):
                    self.check.update({sn: dev})
            else:
                self.unmatched.add(dev)

    def initial_attribute_matching(self, ipf: IPFabric):
        """Step 1: Initial matching to check if LM devices assigned an IPF sn has a device in IPF Snapshot"""
        for sn, dev in self.check.copy().items():
            if sn in ipf.check or (
                sn in ipf.unmatched and extra_checks(dev, ipf.unmatched[sn], ipf)
            ):
                ipf_dev = (
                    ipf.check.pop(sn) if sn in ipf.check else ipf.unmatched.pop(sn)
                )
                self.matched[sn], ipf.matched[sn] = self.check.pop(sn), ipf_dev
                add_attributes(dev, ipf_dev, ipf.snapshot_meta)
                logger.debug(
                    f"Matched LM Device '{dev.display_name}/{dev.id}' to IPF Device '{ipf_dev.hostname}/{sn}'."
                )
            else:
                # TODO Report this device not discovered in IPF
                logger.warning(
                    f"LM Device '{dev.display_name}/{dev.id}' with IPF SN '{dev.ipf_properties.sn}'"
                    f" not found in IPF Snapshot '{self.snapshot_id}'."
                )
