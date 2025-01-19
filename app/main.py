from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app import routes

app = FastAPI(
    title="HealthLink Backend",
    description="Backend for HealthLink that handels authoritation, patient data retrival, and chat requests",
    version="1.0.0"
)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except ValueError:
        return JSONResponse(status_code=400, content={"detail": "Value Error"})
    except RequestValidationError:
        return JSONResponse(status_code=422, content={"detail": "Request Validation Error."})
    except Exception:
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

app.include_router(routes.router, tags=["API"])
