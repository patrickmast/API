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

@app.post("/shorten-url")
async def shorten_url(url: str):
    shortcode = generate_shortcode()
    url_mappings[shortcode] = url
    return {"shortcode": shortcode}


@app.get("/redirect")
async def redirect_url(shortcode: str):
    if shortcode not in url_mappings:
        raise HTTPException(status_code=404, detail=f"Shortcode '{shortcode}' not found")

    original_url = url_mappings[shortcode]
    return {"url": original_url}
