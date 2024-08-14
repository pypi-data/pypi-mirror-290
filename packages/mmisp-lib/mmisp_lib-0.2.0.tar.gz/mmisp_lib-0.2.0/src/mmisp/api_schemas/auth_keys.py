from datetime import datetime

from pydantic import BaseModel, PositiveInt, conint


class SearchGetAuthKeysResponseItemUser(BaseModel):
    id: str
    email: str


class ViewAuthKeyResponseWrapper(BaseModel):
    id: str
    uuid: str
    authkey_start: str
    authkey_end: str
    created: datetime
    expiration: int
    read_only: bool
    user_id: str
    comment: str
    allowed_ips: list[str] | None = None
    unique_ips: list[str] | None = []


class ViewAuthKeysResponse(BaseModel):
    AuthKey: ViewAuthKeyResponseWrapper
    User: SearchGetAuthKeysResponseItemUser


class SearchGetAuthKeysResponseItemAuthKey(BaseModel):
    id: str
    uuid: str
    authkey_start: str
    authkey_end: str
    created: str
    expiration: str
    read_only: bool
    user_id: str
    comment: str | None
    allowed_ips: list[str] | None = None
    unique_ips: list[str] | None = []


class SearchGetAuthKeysResponseItem(BaseModel):
    AuthKey: SearchGetAuthKeysResponseItemAuthKey
    User: SearchGetAuthKeysResponseItemUser

    class Config:
        orm_mode = True


class SearchAuthKeyBody(BaseModel):
    page: PositiveInt = 1
    limit: conint(gt=0, lt=500) = 25  # type: ignore
    id: str | None = None
    uuid: str | None = None
    authkey_start: str | None = None
    authkey_end: str | None = None
    created: str | None = None
    expiration: str | None = None
    read_only: bool | None = None
    user_id: str | None = None
    comment: str | None = None
    allowed_ips: str | list[str] | None = None
    last_used: str | None = None  # deprecated


class EditAuthKeyResponseAuthKey(BaseModel):
    id: str
    uuid: str
    authkey_start: str
    authkey_end: str
    created: str
    expiration: str
    read_only: bool
    user_id: str
    comment: str
    allowed_ips: str | None = None


class EditAuthKeyResponseUser(BaseModel):
    id: str
    org_id: str


class EditAuthKeyResponse(BaseModel):
    AuthKey: EditAuthKeyResponseAuthKey
    User: EditAuthKeyResponseUser


class EditAuthKeyBody(BaseModel):
    read_only: bool | None = None
    comment: str | None = None
    allowed_ips: list[str] | None = None
    expiration: int | None = None


class AddAuthKeyResponseAuthKey(BaseModel):
    id: str
    uuid: str
    authkey_start: str
    authkey_end: str
    created: str
    expiration: str | None = "0"
    read_only: bool
    user_id: str
    comment: str | None = None
    allowed_ips: list[str] | None = None
    unique_ips: list[str]
    authkey_raw: str


class AddAuthKeyResponse(BaseModel):
    AuthKey: AddAuthKeyResponseAuthKey


class AddAuthKeyBody(BaseModel):
    uuid: str | None = None
    read_only: bool | None = None
    user_id: int | None = None
    comment: str | None = None
    allowed_ips: list[str] | None = None
    expiration: int | str | None = 0
