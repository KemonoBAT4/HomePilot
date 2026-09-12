import hashlib

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import PC, Profile

router = APIRouter(prefix="/agent", tags=["agent"])

def _hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
# # #enddef _hash

def get_current_pc(authorization: str = Header(None), db: Session = Depends(get_db)) -> PC:

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token mancante")
    # #endif

    token = authorization.removeprefix("Bearer ").strip()
    pc = db.query(PC).filter(PC.token_hash == _hash(token), PC.paired == True).first()

    if not pc:
        raise HTTPException(status_code=401, detail="Token non valido")
    # #endif

    return pc
# #enddef get_current_pc

@router.get("/checkin")
def checkin(pc: PC = Depends(get_current_pc), db: Session = Depends(get_db)):

    if not pc.pending_profile_id:
        return {"profile": None}
    # #endif

    profile = db.query(Profile).filter(Profile.id == pc.pending_profile_id).first()
    pc.pending_profile_id = None
    db.commit()

    if not profile:
        return {"profile": None}
    # #endif

    return {
        "profile": {
            "id": profile.id,
            "name": profile.name,
            "lock_after_launch": profile.lock_after_launch,
            "apps": [
                {"command": a.command, "args": a.args, "delay_seconds": a.delay_seconds}
                for a in sorted(profile.apps, key=lambda a: a.launch_order)
            ],
        }
    }
# #enddef checkin
