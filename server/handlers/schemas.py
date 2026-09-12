
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class ProfileAppBase(BaseModel):
    command       : str
    args          : List[str] = []
    launch_order  : int       = 0
    delay_seconds : int       = 0
# #endclass ProfileAppBase

class ProfileAppCreate(ProfileAppBase):
    pass
# #endclass ProfileAppCreate

class ProfileAppOut(ProfileAppBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
# #endclass ProfileAppOut

class ProfileBase(BaseModel):
    name: str
    lock_after_launch: bool = True
# #endclass ProfileBase

class ProfileCreate(ProfileBase):
    apps: List[ProfileAppCreate] = []
# #endclass ProfileCreate

class ProfileOut(ProfileBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    apps: List[ProfileAppOut] = []
# #endclass ProfileOut

class PCOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    device_id: str
    name: str
    mac_address: Optional[str] = None
    last_known_ip: Optional[str] = None
    os_type: Optional[str] = None
    paired: bool
    profiles: List[ProfileOut] = []
# #endclass PCOut

class DiscoveredDevice(BaseModel):
    device_id: str
    hostname: str
    os_type: Optional[str] = None
    mac: Optional[str] = None
    ip: Optional[str] = None
    port: int
# #endclass DiscoveredDevice

class PairApproveRequest(BaseModel):
    name: str
# #endclass PairApproveRequest