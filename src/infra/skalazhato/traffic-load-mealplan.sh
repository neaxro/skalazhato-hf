#!/bin/bash

BASE_URL=http://172.21.0.2:30000
HOSTNAME=skalazhato.nemes.local

while true
do
    curl --location $BASE_URL/planner/mealplans \
    --header "Host: $HOSTNAME" \
    --header 'Content-Type: application/json' \
    --data '{
        "user_id": 1,
        "week_start": "2025-12-14",
        "recipes": [
            {
            "recipe_id": 1,
            "day_of_week": 0
            },
            {
            "recipe_id": 1,
            "day_of_week": 1
            },
            {
            "recipe_id": 1,
            "day_of_week": 2
            },
            {
            "recipe_id": 1,
            "day_of_week": 3
            },
            {
            "recipe_id": 1,
            "day_of_week": 4
            },
            {
            "recipe_id": 1,
            "day_of_week": 5
            },
            {
            "recipe_id": 1,
            "day_of_week": 6
            }
        ]
    }' >> /dev/null

    MEALPLAN_ID=$((1 + RANDOM % 5))

    echo -n "Recipe count in mealplan: "
    curl --location $BASE_URL/planner/mealplans/$MEALPLAN_ID/recipes \
        --silent \
        --header "Host: $HOSTNAME" | jq '.mealplan.recipes | length'
done
