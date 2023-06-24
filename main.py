import random
import string
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Msg(BaseModel):
    msg: str

# Function to generate random shortcode
def generate_shortcode(length: int = 6) -> str:
    shortcode = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return shortcode

# Dictionary to store shortcode to URL mappings
url_mappings = {}


@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/path")
async def demo_get():
    return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}


@app.post("/shorten-url")
async def shorten_url(url: str):
    shortcode = generate_shortcode()
    url_mappings[shortcode] = url
    return {"shortcode": shortcode}


@app.get("/{shortcode}")
async def redirect_url(shortcode: str):
    if shortcode not in url_mappings:
        raise HTTPException(status_code=404, detail="Shortcode not found")

    original_url = url_mappings[shortcode]
    return {"url": original_url}
