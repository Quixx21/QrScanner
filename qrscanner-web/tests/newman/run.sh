#!/bin/bash
ENV_FILE="../postman/qrscanner.postman_environment.json"
COLLECTION_FILE="../postman/qrscanner.postman_collection.json"

newman run "$COLLECTION_FILE" -e "$ENV_FILE"

