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
from features.samples.controllers.sample_controller import router as sample_router
from features.packages.controllers.package_controller import router as package_router

# from features.bbox.controllers.bbox_controller import router as bbox_router
from features.examination.controllers.examination_controller import (
    router as examination_router,
)

# define CORS domain white list
origins = ["http://localhost:3000"]

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
app.include_router(package_router)
app.include_router(sample_router)
# app.include_router(bbox_router)
app.include_router(examination_router)
