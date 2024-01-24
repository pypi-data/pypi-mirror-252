from dataclasses import dataclass
from typing import Optional


@dataclass
class MergedDevice:
    ipf_hostname: Optional[str] = None
    ipf_fqdn: Optional[str] = None
    ipf_login_ip: Optional[str] = None
    ipf_site: Optional[str] = None
    ipf_vendor: Optional[str] = None
    ipf_family: Optional[str] = None
    ipf_platform: Optional[str] = None
    ipf_model: Optional[str] = None
    ipf_serial_number: Optional[str] = None
    ipf_hw_serial_number: Optional[str] = None
    ipf_version: Optional[str] = None
    ipf_device_type: Optional[str] = None
    lm_display_name: Optional[str] = None
    lm_name: Optional[str] = None
    lm_hostname: Optional[str] = None
    lm_sysname: Optional[str] = None
    lm_description: Optional[str] = None
    lm_host_status: Optional[str] = None
    lm_groups: Optional[str] = None
    lm_id: Optional[int] = None
    lm_network_address: Optional[str] = None
    lm_endpoint_serial_number: Optional[str] = None
    lm_entphysical_serialnum: Optional[str] = None
    lm_url: Optional[str] = None
