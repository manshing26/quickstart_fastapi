import os
import logging
from passlib.context import CryptContext
from app.config.role_and_permission import ROLE, PERMISSION

class Setting():
    # security and encrypt
    SECRET_KEY = os.environ['SECRET_KEY']
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ALGORITHM = os.environ['ALGORITHM']
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])
    
    ## mongodb
    MONGO_URL = os.environ['MONGO_URL']
    PAGINATION_MAX_DOCS = 20
    
    ## generic
    DEBUG = os.environ['DEBUG']
    ROLE = ROLE
    PERMISSION = PERMISSION
    
    ## System Log
    LOG_FILE_DEST = "logs/system_log.log"
    LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    LOGGING_LEVEL = logging.INFO
    LOGGING_MAX_BYTES = 1000*1024
    LOGGING_MAX_BACKUP = 10