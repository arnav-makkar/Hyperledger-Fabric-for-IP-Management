# File: backend/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn
import json

# Import Hyperledger Fabric SDK for Python
from hfc.fabric import Client

app = FastAPI(title="IP Management API")

# Initialize Fabric client using a network profile JSON file
network_profile = "network.json"  # Place your Fabric network profile here
client = Client(net_profile=network_profile)
channel_name = "ipchannel"
client.new_channel(channel_name)

# Models for the API payloads
class RegisterIPRequest(BaseModel):
    id: str
    hash: str
    metadata: str
    version: str
    owner: str
    license: str
    timestamp: str
    contributors: list[str] = Field(default_factory=list)

class UpdateIPRequest(BaseModel):
    id: str
    new_metadata: str
    new_version: str
    timestamp: str

class TransferOwnershipRequest(BaseModel):
    id: str
    new_owner: str
    timestamp: str

@app.post("/register")
async def register_ip(req: RegisterIPRequest):
    try:
        contributors_json = json.dumps(req.contributors)
        response = client.chaincode_invoke(
            requestor='Admin',
            channel_name=channel_name,
            peers=['peer0.org1.example.com'],
            cc_name='ipregistry',
            args=['RegisterIP', req.id, req.hash, req.metadata, req.version, req.owner, req.license, req.timestamp, contributors_json]
        )
        return {"transaction_id": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/query/{ip_id}")
async def query_ip(ip_id: str):
    try:
        response = client.chaincode_query(
            requestor='Admin',
            channel_name=channel_name,
            peers=['peer0.org1.example.com'],
            cc_name='ipregistry',
            args=['QueryIP', ip_id]
        )
        if not response:
            raise HTTPException(status_code=404, detail="IP asset not found")
        return json.loads(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update")
async def update_ip(req: UpdateIPRequest):
    try:
        response = client.chaincode_invoke(
            requestor='Admin',
            channel_name=channel_name,
            peers=['peer0.org1.example.com'],
            cc_name='ipregistry',
            args=['UpdateIP', req.id, req.new_metadata, req.new_version, req.timestamp]
        )
        return {"transaction_id": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transfer")
async def transfer_ip(req: TransferOwnershipRequest):
    try:
        response = client.chaincode_invoke(
            requestor='Admin',
            channel_name=channel_name,
            peers=['peer0.org1.example.com'],
            cc_name='ipregistry',
            args=['TransferOwnership', req.id, req.new_owner, req.timestamp]
        )
        return {"transaction_id": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
