from fastapi.responses import JSONResponse

#exception handlers are plugged in app.py
async def user_not_found_exception_handler(request, exc):
    if exc.status_code == 404:
        return JSONResponse(
            # you can define other parameters in definition linked with this exception
            content={"context":  exc.context},
            status_code=404,
        )
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
    )
