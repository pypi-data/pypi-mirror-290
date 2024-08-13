from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class Instance(BaseModel):
    model_config = ConfigDict(strict=True)

    instance_id: str
    instance_name: Optional[str]
    project_id: Optional[str]
    project_name: Optional[str]
    domain_name: Optional[str]
    private_v4_ips: Optional[list[str]]
    floating_ip: Optional[str]
    status: str
    ram: int
    vcpus: int
    created_at: str
    updated_at: str
