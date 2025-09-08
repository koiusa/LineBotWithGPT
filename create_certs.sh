#!/usr/bin/env bash

CURRENT=$(cd $(dirname $0) && pwd)
CERT_DIR="$CURRENT/frontend/certs"
mkdir -p "$CERT_DIR"

pushd .
cd $CERT_DIR
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
popd