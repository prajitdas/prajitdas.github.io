#!/bin/bash
HASH=$(openssl dgst -sha384 -binary assets/js/main.js | openssl base64)
echo "Hash output from openssl:"
echo $HASH
if grep -q "integrity=\"sha384-$HASH\"" index.html; then
  echo "Hash matches index.html"
else
  echo "Hash DOES NOT MATCH index.html"
  grep -n "assets/js/main.js" index.html
fi
