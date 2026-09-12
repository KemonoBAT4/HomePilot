import hashlib
import secrets

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from handlers import mdns, schemas
from models import *
from database import *

import os
SERVER_PUBLIC_URL = os.getenv("SERVER_PUBLIC_URL", "http://localhost:8000")

router = APIRouter(prefix="/pairing", tags=["pairing"])

@router.get("/discovered", response_model=list[schemas.DiscoveredDevice])
def list_discovered(db: Session = Depends(get_db)):
    """PC visti in LAN via mDNS ma non ancora accoppiati con il server."""

    already_paired: dict = {
        pc.device_id for pc in db.query(PC).filter(PC.paired == True).all()
    }

    return [d for d in mdns.discovered_devices.values() if d["device_id"] not in already_paired]
# #enddef list_discovered

@router.post("/{device_id}/approve", response_model=schemas.PCOut)
def approve_pairing(device_id: str, payload: schemas.PairApproveRequest, db: Session = Depends(get_db)):
    device = mdns.discovered_devices.get(device_id)

    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo non trovato in LAN")
    # #endif

    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    pc = db.query(PC).filter(PC.device_id == device_id).first()
    if not pc:
        pc = PC(device_id=device_id, name=payload.name)
        db.add(pc)
    # #endif

    pc.name = payload.name
    pc.mac_address = device.get("mac")
    pc.last_known_ip = device.get("ip")
    pc.os_type = device.get("os_type")
    pc.token_hash = token_hash
    pc.paired = True
    db.commit()
    db.refresh(pc)

    try:
        response = httpx.post(f"http://{device['ip']}:{device['port']}/pair", json={"token": token, "server_url": SERVER_PUBLIC_URL}, timeout=5.0)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502, detail=f"Impossibile contattare l'agente per completare il pairing: {exc}"
        )
    # #endtry

    return pc
# #enddef approve_pairing
