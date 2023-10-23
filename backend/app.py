from fastapi import FastAPI
from features.users.controllers.user_controller import router as user_router
from features.authorization.controllers.token_controller import router as auth_router
import mysql.connector
from features.exceptions.handlers.handlers import *
from features.exceptions.definitions.definitions import *

# Quick connection check, you can remove it if you don't want it
# Setting up connection is in database.py and session.py

db_config = {
    "host": "db_TagMedX",
    "user": "user",
    "password": "password",
    "database": "db",
    "port": 3306,
}
# you can remove it
try:
    # Attempt to establish a connection to the database
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        print("Connected to MySQL database")
        connection.close()
    else:
        print("Failed to connect to MySQL database")

except mysql.connector.Error as e:
    print("Error: ", e)


# this cannot be removed

app = FastAPI()
# Include custom exception handler with our own exception
app.exception_handler(UserNotFoundException)(user_not_found_exception_handler)

# Include the user router in your app
app.include_router(user_router)
app.include_router(auth_router)
