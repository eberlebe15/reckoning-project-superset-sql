#!/bin/bash
set -e

# Initialize the database
superset db upgrade

# set flask app
export FLASK_APP=superset

# Create an admin user (you will be prompted to set a username, first and last name before setting a password)
if [ $(superset fab list-users | grep -c reckoning_admin) -eq 0 ]; then
    superset fab create-admin \
        --username "$ADMIN_USERNAME" \
        --firstname "$ADMIN_FIRSTNAME" \
        --lastname "$ADMIN_LASTNAME" \
        --email "$ADMIN_EMAIL" \
        --password "$ADMIN_PASSWORD"
fi

# Create default roles and permissions
superset init

# To start a development web server, use the -h option to bind to host and -p option to bind to port
superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger
