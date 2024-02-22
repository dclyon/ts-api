#!/bin/bash

# function prompts for username and password, will then save token as var
login_and_save_token() {
    echo "-----API.LOGIN-----"
    echo "**THIS SCRIPT MUST BE RUN WITH source COMMAND**"
    sleep 1
    echo -n "Enter username: "
    read USERNAME
    echo -n "Enter password: "
    read -s PASSWORD

    json_input=$(curl -k -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}")
    echo $json_input | jq '.'

    if [ -n "${json_input}" ]; then
        TOKEN=$(echo $json_input | jq -r '.access_token')
        echo "Access Token: $TOKEN"
        export TOKEN="$TOKEN"
        REFRESH_TOKEN=$(echo $json_input | jq -r '.refresh_token')
        export REFRESH_TOKEN="$REFRESH_TOKEN"
        echo "Tokens saved as environment variables."
    else
        echo "Error: Try again."
        exit 1
    fi
}

execute_curl_for_refresh() {
    url="http://localhost:5000/token/refresh"
    auth_header="Authorization: Bearer $REFRESH_TOKEN"

    response=$(curl -k -X POST "$url" -H "$auth_header")
    echo "$response"
    echo -en "\n"

    # updates TOKEN environment variable with new token
    if [ -n "${response}" ]; then
        NEW_ACCESS_TOKEN=$(echo $response | jq -r '.access_token')
        if [ -n "${NEW_ACCESS_TOKEN}" ]; then
            export TOKEN="$NEW_ACCESS_TOKEN"
            echo "New access token acquired and saved."
        fi
    fi
}


# function for curl commands
execute_curl() {
    local route=$1
    local method=$2  # GET or POST section of command
    local data="$3"  # data for POST request

    url="http://localhost:5000${route}"
    auth_header="Authorization: Bearer $TOKEN"

    if [ "$method" == "POST" ]; then
        curl -k -X $method "$url" -H "$auth_header" -H "Content-Type: application/json" -d "$data"
    else
        curl -k -X $method "$url" -H "$auth_header"
    fi
    echo -en "\n"
}

# main

login_and_save_token

while true; do
    echo "Available routes:"
    echo "/protected - Access to protected page"
    echo "/api/items - Get or add items"
    echo "/logs - View logs"
    echo "/groups - View groups"
    echo "/primarygroup - Get primary group for a user"
    echo "/token/refresh - Refresh your access token"
    echo "exit - Exit the script"
    echo -n "Enter the route you wish to access or 'exit' to quit: "
    read route

    if [ "$route" == "exit" ]; then
        echo "Exiting script."
        break
    fi

    case $route in
        "/protected")
            execute_curl "/protected" "GET"
            ;;
        "/api/items")
            echo -n "Do you want to GET or POST to /api/items? (GET/POST): "
            read action
            if [ "$action" == "POST" ]; then
                echo -n "Enter JSON data for the item: "
                read data
                execute_curl "/api/items" "POST" "$data"
            else
                execute_curl "/api/items" "GET"
            fi
            ;;
        "/logs")
            execute_curl "/logs" "GET"
            ;;
        "/groups")
            execute_curl "/groups" "GET"
            ;;
        "/primarygroup")
            echo -n "Enter username for primary group: "
            read username
            execute_curl "/primarygroup?user=$username" "GET"
            ;;
        "/token/refresh")
            execute_curl_for_refresh
            ;;
        *)
            echo "Invalid route"
            ;;
    esac
done
