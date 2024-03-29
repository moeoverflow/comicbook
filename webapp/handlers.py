import os
import logging

import sentry_sdk
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_socketio import SocketManager
from engineio.payload import Payload

import config
from crawler import Crawler
from .utils import comic_file, which_type

logger = logging.getLogger(__name__)
sentry_sdk.init(dsn=config.SENTRY_DSN)
templates = Jinja2Templates(directory="webapp/templates")
Payload.max_decode_packets = 50

app = FastAPI()
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/comic/download/{comic_type}-{comic_id}.epub")
async def download_comic(comic_type: str, comic_id: int):
    file_path = comic_file(which_type(comic_type), str(comic_id))
    if file_path is None:
        raise HTTPException(status_code=404, detail="comic not found")
    else:
        return FileResponse(
            file_path,
            media_type="application/epub+zip",
            filename=os.path.basename(file_path),
        )


sio = SocketManager(
    app=app,
    mount_location="/",
    socketio_path="socket.io",
    cors_allowed_origins=config.CORS_ALLOWED_ORIGINS,
    async_mode="asgi",
)


@sio.on("check-status")
async def handle_status(sid, data):
    url = data.get("url")
    if url is None:
        return {"status": "error", "error": "no url provided"}
    else:
        if data.get("start", False):
            return Crawler.add_download_task(url)["data"]
        else:
            return Crawler.check(url)["data"]
