# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from common.database.mysql.read import read_database
from common.register import APIRouterRegister
from common.response import PermissionDeniedException, error, NotFoundException, BadRequestException
from common.database.mysql.write import write_database
from config import Config


@asynccontextmanager
async def lifespan(app: FastAPI):
    await write_database.connect()
    await read_database.connect()
    # scheduler.start()
    yield
    await write_database.disconnect()
    await read_database.disconnect()

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
APIRouterRegister(app, 'admin').register()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.mount('/static', StaticFiles(directory=Config.STATIC_DIR), name='static')
templates = Jinja2Templates(directory=Config.TEMPLATES_DIR)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content=error(42200))


@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(status_code=400, content=error(40000))


@app.exception_handler(PermissionDeniedException)
async def permission_denied_exception_handler(request: Request, exc: PermissionDeniedException):
    return JSONResponse(status_code=403, content=error(40300))


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=404, content=error(40400))


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    print(exc)
    return JSONResponse(status_code=500, content=error(50000))


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(f'{Config.STATIC_DIR}/favicon.ico')
