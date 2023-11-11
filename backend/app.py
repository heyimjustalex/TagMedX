import mysql.connector
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from features.exceptions.handlers.handlers import *
from features.exceptions.definitions.definitions import *
from features.users.controllers.user_controller import router as user_router
from features.authorization.controllers.token_controller import router as auth_router
from features.groups.controllers.group_controller import router as group_router
from features.sets.controllers.set_controller import router as set_router
from features.label.controllers.label_controller import router as label_router

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
origins = ["http://localhost:3000"]

# this cannot be removed

app = FastAPI()

# Add CORS rules
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include custom exception handler with our own exception
app.exception_handler(UserNotFoundException)(user_not_found_exception_handler)
app.exception_handler(GroupNotFoundException)(group_not_found_exception_handler)
app.exception_handler(InvalidConnectionString)(invalid_connection_string)
app.exception_handler(PermissionDenied)(permission_denied)

# Include the user router in your app
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(group_router)
app.include_router(set_router)
app.include_router(label_router)
