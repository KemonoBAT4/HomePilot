from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import *
from handlers import *
from database import get_db

router = APIRouter(prefix="/pcs/{pc_id}/profiles", tags=["profiles"])

# pcs/{pc_id}/profiles
@router.get("", response_model=list[ProfileOut])
def list_profiles(pc_id: str, db: Session = Depends(get_db)):
    return db.query(Profile).filter(Profile.pc_id == pc_id).all()
# #enddef list_profiles

# pcs/{pc_id}/profiles
@router.post("", response_model=ProfileOut, status_code=201)
def create_profile(pc_id: str, payload: ProfileCreate, db: Session = Depends(get_db)):
    pc = db.query(PC).filter(PC.id == pc_id).first()

    if not pc:
        raise HTTPException(status_code=404, detail="PC non trovato")
    # #endif

    profile: Profile = Profile(pc_id=pc_id, name=payload.name, lock_after_launch=payload.lock_after_launch)
    profile.apps     = [ProfileApp(**app.model_dump()) for app in payload.apps]

    db.add(profile)
    db.commit()

    db.refresh(profile)

    return profile
# #enddef create_profile

@router.delete("/{profile_id}", status_code=204)
def delete_profile(pc_id: str, profile_id: str, db: Session = Depends(get_db)):

    profile = (
        db.query(
            Profile
        ).filter(
            Profile.id == profile_id,
            Profile.pc_id == pc_id
        ).first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Profilo non trovato")
    # #endif

    db.delete(profile)
    db.commit()
# #enddef delete_profile

@router.post("/{profile_id}/launch", status_code=202)
def launch_profile(pc_id: str, profile_id: str, db: Session = Depends(get_db)):
    pc: PC | None = db.query(PC).filter(PC.id == pc_id).first()

    if (pc is None):
        raise HTTPException(status_code=404, detail="PC non trovato")
    # #endif

    profile: Profile | None = db.query(Profile).filter(Profile.id == profile_id, Profile.pc_id == pc_id).first()

    if (profile is None):
        raise HTTPException(status_code=404, detail="Profilo non trovato")
    # #endif

    pc.pending_profile_id = profile.id
    db.commit()

    if (pc.mac_address is not None):
        send_magic_packet(pc.mac_address)
    # #endif

    return {"status": "queued"}
# #enddef launch_profile
