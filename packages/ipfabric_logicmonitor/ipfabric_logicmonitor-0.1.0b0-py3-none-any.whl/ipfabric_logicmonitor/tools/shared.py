from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric_logicmonitor.models import LMDevice, IPFDevice
    from ipfabric_logicmonitor import IPFabric

import logging

logger = logging.getLogger(__name__)


def add_attributes(lm_dev: LMDevice, ipf_dev: IPFDevice, snap_meta: dict):
    lm_dev.ipf_properties.load_ipf_data(**ipf_dev.model_dump(), **snap_meta)
    ipf_dev.lm_attributes.load_lm_data(
        device_id=lm_dev.id,
        host_status=lm_dev.host_status,
        name=lm_dev.name,
        displayname=lm_dev.display_name,
    )


def extra_checks(lm_dev: LMDevice, ipf_dev: IPFDevice, ipf: IPFabric) -> bool:
    """Perform some extra checks that a LM host matches IPF host based on name or an IP Address."""
    lm_names, lm_ips = lm_dev.lm_names_ips
    if lm_names.intersection(ipf_dev.ipf_names):
        logger.debug(
            f"Matched LM Device to IPF Device by hostname(s) '{lm_names.intersection(ipf_dev.ipf_names)}'."
        )
        return True

    ipf_dev_ips = {i.ip for i in ipf.managed_ips.by_sn[ipf_dev.sn]}
    if lm_ips.intersection(ipf_dev_ips):
        logger.debug(
            f"Matched LM Device to IPF Device by IP(s) '{lm_ips.intersection(ipf_dev_ips)}'."
        )
        return True
    return False
