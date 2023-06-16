import motor.motor_asyncio

from app.config.setting import Setting

client = motor.motor_asyncio.AsyncIOMotorClient(Setting.MONGO_URL)
db = client.testdb
