from pydantic import BaseModel


class Config(BaseModel):
    port = 8080
    host = '127.0.0.1'

    onebot_access_token: str = ''

    lagrange_path: str = 'Lagrange'
    lagrange_auto_start: bool = True
    lagrange_auto_install: bool = True
