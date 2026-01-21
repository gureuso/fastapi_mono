# -*- coding: utf-8 -*-
import jwt
from typing import Literal
from datetime import datetime, timedelta
from fastapi import APIRouter, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from common.database.mysql.entity import UserEntity
from common.service.user import UserService
from common.sns import SNSInfo
from config import Config, JsonConfig

router = APIRouter(prefix='/api/users')
templates = Jinja2Templates(directory=Config.TEMPLATES_DIR)


class TokenItem(BaseModel):
    token: str


@router.get('/signout')
async def signout():
    response = RedirectResponse(
        url='http://localhost:8889/admin', status_code=status.HTTP_302_FOUND)
    response.delete_cookie(
        key='x-access-token',
        domain='localhost',
    )
    return response


@router.get('/callback/{provider}')
async def callback(provider: Literal['google', 'facebook', 'kakao', 'naver', 'github'], code: str):
    sns_info = SNSInfo(provider, code)
    email = sns_info.get_info().email

    user = await UserService.find_one_by_email(email)
    if not user:
        user = await UserService.create(UserEntity(
            email=email,
            provider=provider,
            created_at=datetime.now(),
        ))
        await UserService.update_num(user)

    response = RedirectResponse(
        url='http://localhost:8889/admin',
        status_code=status.HTTP_302_FOUND
    )
    new_token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)}, JsonConfig.get_data('SECRET'), algorithm='HS256')
    response.set_cookie('x-access-token', new_token, httponly=True)
    return response
