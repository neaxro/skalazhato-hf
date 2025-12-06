#!/bin/bash

BASE_URL=http://172.21.0.2:30000
HOSTNAME=skalazhato.nemes.local

while true
do
    curl --location $BASE_URL/recipe/recipes \
    --silent \
    --request POST \
    --header "Host: $HOSTNAME" \
    --header 'Content-Type: application/json' \
    --data '{
        "name": "Test recipe",
        "description": "This is a test recipe."
    }' >> /dev/null

    echo -n "Recipe count in DB: "
    curl --location $BASE_URL/recipe/recipes \
        --silent \
        --header "Host: $HOSTNAME" | jq '.recipes | length'
done
