#!/bin/bash

# Initialize the database
superset db upgrade

# set flask app
export FLASK_APP=superset

# Create an admin user (you will be prompted to set a username, first and last name before setting a password)
# superset fab create-admin \
#               --username  \
#               --firstname  \
#               --lastname  \
#               --email  \
#               --password 

# Create default roles and permissions
superset init

# To start a development web server, use the -h option to bind to host and -p option to bind to port
superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger
