from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    port: int = 6502
    interval: int = 45
    image_directory: Path = Path("/tmp/images")

    model_config = SettingsConfigDict(env_prefix="CAROUSEL_")


config = Config()
app = FastAPI()


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
app.mount("/images", StaticFiles(directory=config.image_directory), name="images")


def get_files() -> list[str]:
    return list(p.name for p in config.image_directory.glob("*") if p.suffix in [".jpeg", ".jpg", ".png"])


@app.get("/")
def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html.j2", {"request": request, "files": get_files()})


@app.get("/carousel.js")
def carousel_js(request: Request) -> PlainTextResponse:
    return templates.TemplateResponse(
        "carousel.js.j2",
        {"request": request, "count": len(get_files()), "interval": config.interval},
    )


def run():
    uvicorn.run(app, port=config.port)


if __name__ == "__main__":
    run()
