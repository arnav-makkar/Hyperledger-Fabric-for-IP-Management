# ESDM Blockchain IP Management System

This project demonstrates a blockchain-based IP management system designed for ESDM projects under the Government of India. It leverages Hyperledger Fabric for secure, tamper-proof IP registration and auditing, with a Python-based REST API for easy integration and user access.

## Components

1. **Chaincode (Smart Contract):**
   - **Location:** `chaincode/ipregistry.go`
   - **Functionality:** Implements core functions such as `RegisterIP`, `QueryIP`, `UpdateIP`, and `TransferOwnership`.

2. **Python Backend API:**
   - **Location:** `backend/app.py`
   - **Functionality:** Provides REST endpoints to interact with the blockchain, using the Hyperledger Fabric Python SDK.
   - **Endpoints:**
     - `POST /register` – Register a new IP asset.
     - `GET /query/{ip_id}` – Query details of an IP asset.
     - `POST /update` – Update metadata and version information.
     - `POST /transfer` – Transfer ownership of an IP asset.

3. **Deployment:**
   - **Docker Compose:** `docker-compose.yaml` orchestrates the Fabric network and the Python backend.
   - **Dockerfile:** Located in `backend/` for containerizing the Python API.

## Deployment Steps

1. **Setup Fabric Network:**
   - Follow the [Hyperledger Fabric test-network documentation](https://hyperledger-fabric.readthedocs.io/en/release-2.2/test_network.html) to set up and deploy your network.
   - Deploy the chaincode (`ipregistry.go`) to your channel (e.g., `ipchannel`).

2. **Build and Run the Python Backend:**
   - Navigate to the `backend/` folder and build the Docker image:
     ```bash
     docker build -t ip-management-backend .
     ```
   - From the project root, run:
     ```bash
     docker-compose up
     ```
   - The API will be available at `http://localhost:8000`.

3. **Using the API:**
   - **Register an IP:**
     ```bash
     curl -X POST http://localhost:8000/register \
     -H 'Content-Type: application/json' \
     -d '{
           "id": "IP001",
           "hash": "QmXYZ123...",
           "metadata": "PCB schematic for design X",
           "version": "1.0",
           "owner": "DesignDept",
           "license": "MIT",
           "timestamp": "2025-04-14T12:00:00Z",
           "contributors": ["Alice", "Bob"]
         }'
     ```
   - **Query an IP:**
     ```bash
     curl http://localhost:8000/query/IP001
     ```
   - **Update an IP:**
     ```bash
     curl -X POST http://localhost:8000/update \
     -H 'Content-Type: application/json' \
     -d '{
           "id": "IP001",
           "new_metadata": "Updated PCB schematic for design X",
           "new_version": "1.1",
           "timestamp": "2025-04-15T12:00:00Z"
         }'
     ```
   - **Transfer Ownership:**
     ```bash
     curl -X POST http://localhost:8000/transfer \
     -H 'Content-Type: application/json' \
     -d '{
           "id": "IP001",
           "new_owner": "NewOwnerDept",
           "timestamp": "2025-04-16T12:00:00Z"
         }'
     ```

## Summary

This system provides a robust, permissioned blockchain solution for managing sensitive IP assets in the context of ESDM projects by the Government of India. With secure registration, traceability, and fine-grained access controls, the solution meets the high standards required for confidential government-related IP.

For further questions or to contribute, please refer to the repository instructions.