// File: chaincode/ipregistry.go

package main

import (
	"encoding/json"
	"fmt"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// IPAsset represents the IP asset structure stored on the ledger
type IPAsset struct {
	ID           string   `json:"id"`
	Hash         string   `json:"hash"`
	Metadata     string   `json:"metadata"`
	Version      string   `json:"version"`
	Owner        string   `json:"owner"`
	License      string   `json:"license"`
	Contributors []string `json:"contributors"`
	Timestamp    string   `json:"timestamp"`
}

// SmartContract provides functions for managing IP assets
type SmartContract struct {
	contractapi.Contract
}

// RegisterIP registers a new IP asset
func (s *SmartContract) RegisterIP(ctx contractapi.TransactionContextInterface, id, hash, metadata, version, owner, license, timestamp string, contributorsJSON string) error {
	// Ensure the asset does not exist already
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return fmt.Errorf("failed to get asset: %v", err)
	}
	if assetJSON != nil {
		return fmt.Errorf("asset %s already exists", id)
	}

	var contributors []string
	if err := json.Unmarshal([]byte(contributorsJSON), &contributors); err != nil {
		return fmt.Errorf("failed to parse contributors: %v", err)
	}

	asset := IPAsset{
		ID:           id,
		Hash:         hash,
		Metadata:     metadata,
		Version:      version,
		Owner:        owner,
		License:      license,
		Contributors: contributors,
		Timestamp:    timestamp,
	}

	assetBytes, err := json.Marshal(asset)
	if err != nil {
		return fmt.Errorf("failed to marshal asset: %v", err)
	}

	return ctx.GetStub().PutState(id, assetBytes)
}

// QueryIP returns the IP asset details by id
func (s *SmartContract) QueryIP(ctx contractapi.TransactionContextInterface, id string) (*IPAsset, error) {
	assetBytes, err := ctx.GetStub().GetState(id)
	if err != nil {
		return nil, fmt.Errorf("failed to read asset: %v", err)
	}
	if assetBytes == nil {
		return nil, fmt.Errorf("asset %s not found", id)
	}
	var asset IPAsset
	if err := json.Unmarshal(assetBytes, &asset); err != nil {
		return nil, fmt.Errorf("failed to unmarshal asset: %v", err)
	}
	return &asset, nil
}

// UpdateIP updates the metadata and version of an existing IP asset
func (s *SmartContract) UpdateIP(ctx contractapi.TransactionContextInterface, id, newMetadata, newVersion, timestamp string) error {
	asset, err := s.QueryIP(ctx, id)
	if err != nil {
		return err
	}
	asset.Metadata = newMetadata
	asset.Version = newVersion
	asset.Timestamp = timestamp

	assetBytes, err := json.Marshal(asset)
	if err != nil {
		return fmt.Errorf("failed to marshal updated asset: %v", err)
	}
	return ctx.GetStub().PutState(id, assetBytes)
}

// TransferOwnership transfers the ownership of an IP asset
func (s *SmartContract) TransferOwnership(ctx contractapi.TransactionContextInterface, id, newOwner, timestamp string) error {
	asset, err := s.QueryIP(ctx, id)
	if err != nil {
		return err
	}
	asset.Owner = newOwner
	asset.Timestamp = timestamp

	assetBytes, err := json.Marshal(asset)
	if err != nil {
		return fmt.Errorf("failed to marshal updated asset: %v", err)
	}
	return ctx.GetStub().PutState(id, assetBytes)
}

func main() {
	chaincode, err := contractapi.NewChaincode(new(SmartContract))
	if err != nil {
		fmt.Printf("Error creating ipregistry chaincode: %v\n", err)
		return
	}
	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting ipregistry chaincode: %v\n", err)
	}
}
