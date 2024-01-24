from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric_logicmonitor import IPFabric, LogicMonitor

from dataclasses import dataclass

from ipfabric_logicmonitor.models import LMDevice

import logging
import re
from ipfabric_logicmonitor.tools import add_attributes, extra_checks


logger = logging.getLogger(__name__)
FQDN_RE = re.compile(
    r"(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}\.?$)"
)


@dataclass
class DeviceMatching:
    lm: LogicMonitor
    ipf: IPFabric

    def match_devices(self):
        self.lm.initial_attribute_matching(self.ipf)
        self.ipf.initial_attribute_matching(self.lm)
        self.serial_number_lookup()
        self.ip_mac_lookup()
        self.hostname_lookup()

    def serial_number_lookup(self):
        """Lookup device in IP Fabric based on a Serial Number if one configured on the device."""
        for dev in self.lm.unmatched.copy():
            for lm_sn_name in ["endpoint_serial_number", "entphysical_serialnum"]:
                lm_sn = getattr(dev.auto, lm_sn_name).lower()

                if lm_sn and lm_sn in self.ipf.hw_sn:
                    if len(self.ipf.hw_sn[lm_sn]) == 1:
                        ipf_sn = self.ipf.hw_sn[lm_sn].copy().pop()
                        if ipf_sn in self.ipf.unmatched:
                            ipf_dev = self.ipf.unmatched[ipf_sn]
                            if extra_checks(dev, ipf_dev, self.ipf):
                                self.lm.unmatched.remove(dev)
                                (
                                    self.lm.matched[ipf_sn],
                                    self.ipf.matched[ipf_sn],
                                ) = dev, self.ipf.unmatched.pop(ipf_sn)
                                add_attributes(dev, ipf_dev, self.ipf.snapshot_meta)
                                logger.debug(
                                    f"Matched LM Device '{dev.display_name}/{dev.id}' to "
                                    f"IPF Device '{ipf_dev.hostname}/{ipf_sn}'."
                                )
                                break
                            else:
                                logger.warning(
                                    f"LM Device '{dev.display_name}/{dev.id}' with HW SN '{lm_sn}' matches "
                                    f"IPF Device '{ipf_sn}' but does not match hostname or ip."
                                )
                    else:
                        # TODO multiple ipf devs with same hw sn
                        logger.warning(
                            f"LM Device '{dev.display_name}/{dev.id}' with HW SN '{lm_sn}' matches multiple "
                            f"IPF devices in IPF Snapshot '{self.lm.snapshot_id}'."
                        )
                elif lm_sn:
                    logger.warning(
                        f"LM Device '{dev.display_name}/{dev.id}' with HW SN '{lm_sn}' has no matches in "
                        f"IPF Snapshot '{self.lm.snapshot_id}'."
                    )

    def _matched(self, dev: LMDevice, ipf_sn: str):
        self.lm.unmatched.remove(dev)
        self.lm.matched[ipf_sn], self.ipf.matched[ipf_sn] = dev, self.ipf.unmatched.pop(
            ipf_sn
        )
        add_attributes(dev, self.ipf.matched[ipf_sn], self.ipf.snapshot_meta)
        logger.debug(
            f"Matched LM Device '{dev.display_name}/{dev.id}' to "
            f"IPF Device '{self.ipf.matched[ipf_sn].hostname}/{ipf_sn}'."
        )

    def ip_mac_lookup(self):
        """Lookup device in IP Fabric based on MAC and IP."""
        for dev in self.lm.unmatched.copy():
            if not dev.auto.network_address or not dev.auto.network_mac_address:
                continue

            ip, mac = dev.auto.network_address, dev.auto.network_mac_address
            if mac not in self.ipf.managed_ips.by_mac:
                logger.warning(
                    f"LM Device '{dev.display_name}/{dev.id}' with MAC '{mac}' has no matches in "
                    f"IPF Snapshot '{self.lm.snapshot_id}'."
                )
                continue

            ipf_sn = {i.sn for i in self.ipf.managed_ips.by_mac[mac] if i.ip == ip}
            if len(ipf_sn) > 1:
                logger.warning(
                    f"LM Device '{dev.display_name}/{dev.id}' with MAC '{mac}' and IP '{ip}' has multiple matches in "
                    f"IPF Snapshot '{self.lm.snapshot_id}'."
                )
                continue
            if len(ipf_sn) == 0:
                logger.warning(
                    f"LM Device '{dev.display_name}/{dev.id}' with MAC '{mac}' and IP '{ip}' has no matches in "
                    f"IPF Snapshot '{self.lm.snapshot_id}'."
                )
                continue
            ipf_sn = ipf_sn.pop()
            if extra_checks(dev, self.ipf.unmatched[ipf_sn], self.ipf):
                self._matched(dev, ipf_sn)
            else:
                logger.warning(
                    f"LM Device '{dev.display_name}/{dev.id}' with MAC '{mac}' and IP '{ip}' matches "
                    f"IPF Device '{ipf_sn}' but does not match hostname or ip."
                )

    def _search_name(
        self, dev: LMDevice, name: str, obj: object, attribute: str
    ) -> bool:
        """Verifies that hostname/fqdn only belongs to a single SN in IP Fabric."""
        ipf_sn = {d.sn for d in getattr(obj, attribute)[name]}
        if len(ipf_sn) > 1:
            logger.warning(
                f"LM Device '{dev.display_name}/{dev.id}' with FQDN '{name}' has multiple matches in "
                f"IPF Snapshot '{self.lm.snapshot_id}'."
            )
            return False
        ipf_sn = ipf_sn.pop()
        self._matched(dev, ipf_sn)
        return True

    def _search_by_fqdn(self, lm_fqdns: set, dev: LMDevice) -> bool:
        """First we search by FQDN before any other name matching."""
        for name in lm_fqdns:
            if name in self.ipf.sdk.devices.by_fqdn:
                if self._search_name(dev, name, self.ipf.sdk.devices, "by_fqdn"):
                    return True
            if name in self.ipf.managed_ips.by_fqdn:
                if self._search_name(dev, name, self.ipf.managed_ips, "by_fqdn"):
                    return True
        return False

    def hostname_lookup(self):
        """Lookup device in IP Fabric based on Hostname."""
        for dev in self.lm.unmatched.copy():
            lm_names, _ = dev.lm_names_ips

            if self._search_by_fqdn(
                {name for name in lm_names if FQDN_RE.match(name)}, dev
            ):
                continue

            for name in lm_names:
                if name in self.ipf.sdk.devices.by_hostname:
                    if self._search_name(
                        dev, name, self.ipf.sdk.devices, "by_hostname"
                    ):
                        break
                elif name in self.ipf.sdk.devices.by_hostname_original:
                    if self._search_name(
                        dev, name, self.ipf.sdk.devices, "by_hostname_original"
                    ):
                        break
                elif True:
                    ...  # TODO logical device checking or do this after ip lookup?
