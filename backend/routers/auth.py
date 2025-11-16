from fastapi  import APIRouter, HTTPException, Response
from authx import AuthX, AuthXConfig

from Schemas.UserLoginSchema import UserLoginSchema


router = APIRouter()

config = AuthXConfig()
config.JWT_SECRET_KEY="SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)


@router.post("/login")
def login(creds: UserLoginSchema, response: Response):
    if creds.username == 'test' and creds.password == 'huy123':
        token = security.create_access_token(uid = '12345')
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {'access_token': token}
    raise HTTPException(status_code=401, detail='Incorrect username or password')

@router.get('/protected')
def protected():
    return {"data":'TOP SECRET'}