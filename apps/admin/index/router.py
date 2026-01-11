from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from common.database.mysql.entity import UserEntity
from common.response import verify_token
from config import Config, JsonConfig

router = APIRouter(prefix='/admin')
templates = Jinja2Templates(directory=Config.TEMPLATES_DIR)


@router.get('')
async def index(request: Request, current_user: Optional[UserEntity] = Depends(verify_token)):
    return templates.TemplateResponse('index.html', context={'request': request, 'current_user': current_user})


@router.get('/login')
async def login(request: Request, current_user: Optional[UserEntity] = Depends(verify_token)):
    return templates.TemplateResponse('login.html', context={'request': request, 'current_user': current_user,
                                                             'GOOGLE_CLIENT_ID': JsonConfig.get_data('GOOGLE_CLIENT_ID'),
                                                             'GITHUB_CLIENT_ID': JsonConfig.get_data('GITHUB_CLIENT_ID'),
                                                             'KAKAO_CLIENT_ID': JsonConfig.get_data('KAKAO_CLIENT_ID')})
