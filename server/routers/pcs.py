from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import *
from handlers.schemas import *

from database import get_db
from handlers import send_magic_packet

router = APIRouter(prefix="/pcs", tags=["pcs"])

@router.get("", response_model=list[PCOut])
def list_pcs(db: Session = Depends(get_db)):
    return db.query(PC).filter(PC.paired == True).all()
# #enddef list_pcs

@router.get("/{pc_id}", response_model=PCOut)
def get_pc(pc_id: str, db: Session = Depends(get_db)):
    pc = db.query(PC).filter(PC.id == pc_id).first()

    if not pc:
        raise HTTPException(status_code=404, detail="PC non trovato")
    # #endif

    return pc
# #enddef get_pc

@router.delete("/{pc_id}", status_code=204)
def delete_pc(pc_id: str, db: Session = Depends(get_db)):
    pc = db.query(PC).filter(PC.id == pc_id).first()

    if not pc:
        raise HTTPException(status_code=404, detail="PC non trovato")
    # #endif

    db.delete(pc)
    db.commit()
# #enddef delete_pc

@router.post("/{pc_id}/wake", status_code=202)
def wake_pc(pc_id: str, db: Session = Depends(get_db)):
    pc = db.query(PC).filter(PC.id == pc_id).first()

    if not pc:
        raise HTTPException(status_code=404, detail="PC non trovato")
    # #endif

    if not pc.mac_address:
        raise HTTPException(status_code=400, detail="MAC address non impostato per questo PC")
    # #endif

    send_magic_packet(pc.mac_address)
    return {"status": "wol_sent"}
# #enddef wake_pc