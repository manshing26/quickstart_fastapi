from passlib.context import CryptContext
from datetime import datetime, timedelta
from time import sleep

# plain_text = 'lalalala'
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# print(pwd_context.hash(plain_text))

# expire = datetime.utcnow() + timedelta(seconds=10)
# print((expire))
# sleep(2)
# print(expire > datetime.utcnow())
now = datetime.now()
print(now)