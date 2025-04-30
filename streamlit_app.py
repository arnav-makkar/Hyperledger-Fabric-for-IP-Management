# File: streamlit_app.py

import streamlit as st
import requests
import json

# Set the base URL of your FastAPI backend
API_BASE = "http://localhost:8000"

st.title("ESDM IP Management Dashboard")
st.sidebar.title("Operations")
operation = st.sidebar.selectbox("Choose an Action", 
                                 ["Register IP", "Query IP", "Update IP", "Transfer Ownership"])

# --- Register IP ---
if operation == "Register IP":
    st.header("Register a New IP Asset")
    asset_id = st.text_input("Asset ID")
    ipfs_hash = st.text_input("File Hash (IPFS)")
    metadata = st.text_area("Metadata (e.g., description, specifications)")
    version = st.text_input("Version")
    owner = st.text_input("Owner")
    license_type = st.text_input("License Type")
    timestamp = st.text_input("Timestamp (e.g., 2025-04-14T12:00:00Z)")
    contributors = st.text_input("Contributors (comma separated)")

    if st.button("Register IP"):
        # Create a list of contributors (strip extra spaces)
        contributors_list = [item.strip() for item in contributors.split(",")] if contributors else []
        payload = {
            "id": asset_id,
            "hash": ipfs_hash,
            "metadata": metadata,
            "version": version,
            "owner": owner,
            "license": license_type,
            "timestamp": timestamp,
            "contributors": contributors_list
        }
        try:
            res = requests.post(f"{API_BASE}/register", json=payload)
            res.raise_for_status()
            tx_id = res.json().get("transaction_id", "No transaction ID")
            st.success(f"IP Asset Registered Successfully!\nTransaction ID: {tx_id}")
        except Exception as e:
            st.error(f"Registration failed: {e}")

# --- Query IP ---
elif operation == "Query IP":
    st.header("Query IP Asset")
    query_id = st.text_input("Enter the IP Asset ID to query")
    
    if st.button("Query"):
        try:
            res = requests.get(f"{API_BASE}/query/{query_id}")
            res.raise_for_status()
            asset_data = res.json()
            st.json(asset_data)
        except Exception as e:
            st.error(f"Query failed: {e}")

# --- Update IP ---
elif operation == "Update IP":
    st.header("Update IP Asset")
    update_id = st.text_input("Asset ID to update")
    new_metadata = st.text_area("New Metadata")
    new_version = st.text_input("New Version")
    update_timestamp = st.text_input("Timestamp (e.g., 2025-04-15T12:00:00Z)")
    
    if st.button("Update IP"):
        payload = {
            "id": update_id,
            "new_metadata": new_metadata,
            "new_version": new_version,
            "timestamp": update_timestamp
        }
        try:
            res = requests.post(f"{API_BASE}/update", json=payload)
            res.raise_for_status()
            tx_id = res.json().get("transaction_id", "No transaction ID")
            st.success(f"IP Asset Updated Successfully!\nTransaction ID: {tx_id}")
        except Exception as e:
            st.error(f"Update failed: {e}")

# --- Transfer Ownership ---
elif operation == "Transfer Ownership":
    st.header("Transfer Ownership of an IP Asset")
    transfer_id = st.text_input("Asset ID for Ownership Transfer")
    new_owner = st.text_input("New Owner")
    transfer_timestamp = st.text_input("Timestamp (e.g., 2025-04-16T12:00:00Z)")
    
    if st.button("Transfer Ownership"):
        payload = {
            "id": transfer_id,
            "new_owner": new_owner,
            "timestamp": transfer_timestamp
        }
        try:
            res = requests.post(f"{API_BASE}/transfer", json=payload)
            res.raise_for_status()
            tx_id = res.json().get("transaction_id", "No transaction ID")
            st.success(f"Ownership Transferred Successfully!\nTransaction ID: {tx_id}")
        except Exception as e:
            st.error(f"Transfer failed: {e}")
