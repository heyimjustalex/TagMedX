from fastapi.responses import JSONResponse


async def group_not_found_exception_handler(request, exc):
    if exc.status_code == 404 and exc.context == "Group not found":
        return JSONResponse(
            content={"detail": "Group not found"},
            status_code=404,
        )
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
    )


async def invalid_connection_string(request, exc):
    if exc.status_code == 400 and exc.context == "Invalid connection string":
        return JSONResponse(
            content={"detail": "Invalid connection string"},
            status_code=400,
        )
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
    )


async def user_not_found_exception_handler(request, exc):
    if exc.status_code == 404 and exc.context == "User not found":
        return JSONResponse(
            content={"detail": "User not found"},
            status_code=404,
        )
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
    )
