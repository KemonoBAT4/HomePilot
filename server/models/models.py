
from .base import *
from ._common import *

class PC(BaseModel):
    __tablename__ = "pcs"

    device_id     : str        = Column(String , nullable = False, unique  = True  )  # generato dall'agente al primo avvio
    name          : str        = Column(String , nullable = False, unique  = False )
    mac_address   : str        = Column(String , nullable = True , unique  = False )
    last_known_ip : str        = Column(String , nullable = True , unique  = False )
    os_type       : OsTypeEnum = Column(Enum   , nullable = True , unique  = False )
    token_hash    : str        = Column(String , nullable = True , unique  = False )
    paired        : bool       = Column(Boolean, nullable = False, default = False )

    profiles = relationship("Profile", back_populates="pc", cascade="all, delete-orphan")

    pending_profile_id : str = Column      (String   , ForeignKey("profiles.id"), nullable=True)
    peding_profile           = relationship("Profile", foreign_keys=[pending_profile_id])
# #endclass PC

class Profile(BaseModel):
    __tablename__ = "profiles"

    pc_id            : str  = Column(String, ForeignKey("pcs.id"), nullable=False)
    name             : str  = Column(String, nullable=False)
    lock_after_launch: bool = Column(Boolean, default=True)

    pc   = relationship("PC"        , back_populates="profiles")
    apps = relationship("ProfileApp", back_populates="profile", cascade="all, delete-orphan", order_by="ProfileApp.launch_order")
# #endclass Profile

class ProfileApp(BaseModel):
    __tablename__ = "profile_apps"

    profile_id    : str  = Column(String, ForeignKey("profiles.id"), nullable=False)
    command       : str  = Column(String, nullable=False)  # percorso eseguibile o comando
    args          : list = Column(JSON, default=list)
    launch_order  : int  = Column(Integer, default=0)
    delay_seconds : int  = Column(Integer, default=0)

    profile = relationship("Profile", back_populates="apps")
# #endclass ProfileApp
