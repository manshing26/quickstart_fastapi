import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.config.setting import Setting
from app.auth.router import router as auth_router
from app.users.router import router as user_router
from app.audit_log.router import router as log_router
from app.crud.router import router as crud_router

app = FastAPI(debug=Setting.DEBUG)

@app.on_event("startup")
async def startup_event():
    
    handler = logging.handlers.RotatingFileHandler(
        Setting.LOG_FILE_DEST, mode="a", 
        maxBytes = Setting.LOGGING_MAX_BYTES,
        backupCount = Setting.LOGGING_MAX_BACKUP
        )
    handler.setFormatter(logging.Formatter(Setting.LOGGING_FORMAT))

    logger_access = logging.getLogger("uvicorn.access")
    logger_access.setLevel(Setting.LOGGING_LEVEL)
    logger_access.addHandler(handler)
    
    logger_error = logging.getLogger("uvicorn.error")
    logger_error.setLevel(Setting.LOGGING_LEVEL)
    logger_error.addHandler(handler)
    
app.include_router(
    auth_router,
    tags=['Access token']
    )

app.include_router(
    user_router,
    tags=['Users'],
    prefix="/users"
    )

app.include_router(
    log_router,
    tags=['Audit Log'],
    prefix="/log"
    )

app.include_router(
    crud_router,
    tags=['Sample'],
    prefix="/sample"
    )

@app.get("/",include_in_schema=False)
async def root():
    
    return RedirectResponse(url='/docs')
