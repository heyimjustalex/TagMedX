from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from features.users.controllers.user_controller import router as user_router
from features.authorization.controllers.token_controller import router as auth_router
from features.groups.controllers.group_controller import router as group_router
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

# define CORS domain white list
origins = [
  "http://localhost:3000"
]


# this cannot be removed

app = FastAPI()
# Include custom exception handler with our own exception
app.exception_handler(UserNotFoundException)(user_not_found_exception_handler)
app.exception_handler(GroupNotFoundException)(group_not_found_exception_handler)

# Include the user router in your app
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(group_router)

# Add CORS rules
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
