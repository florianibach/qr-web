from io import BytesIO
from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image, ImageOps, ImageDraw

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

ECC_MAP = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(
    text: str = Form(...),
    size: int = Form(512),
    ecc: str = Form("M"),
    border: int = Form(4),
    logo: Optional[UploadFile] = File(None),
    logo_percent: int = Form(20),  # how big the logo should be relative to QR width
):
    text = (text or "").strip()
    if not text:
        return Response("Text is required", status_code=400)

    size = max(128, min(2048, int(size)))
    border = max(1, min(20, int(border)))
    ecc = (ecc or "M").upper()
    if ecc not in ECC_MAP:
        return Response("Invalid ECC", status_code=400)

    # Build QR
    qr = qrcode.QRCode(
        version=None,
        error_correction=ECC_MAP[ecc],
        box_size=10,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    # Resize to requested size (keep sharp edges)
    img = img.resize((size, size), Image.NEAREST)

    # Optional logo
    if logo and logo.filename:
        content = await logo.read()
        if content:
            try:
                logo_img = Image.open(BytesIO(content)).convert("RGBA")
            except Exception:
                return Response("Logo file is not a valid image.", status_code=400)

            # Ensure logo isn't too large
            logo_percent = max(5, min(40, int(logo_percent)))
            logo_target_w = int(size * (logo_percent / 100.0))

            # Keep aspect ratio
            logo_img = ImageOps.contain(logo_img, (logo_target_w, logo_target_w), Image.LANCZOS)

            # Add a white rounded background behind the logo for readability
            pad = max(6, logo_target_w // 12)
            bg_w = logo_img.size[0] + pad * 2
            bg_h = logo_img.size[1] + pad * 2

            bg = Image.new("RGBA", (bg_w, bg_h), (255, 255, 255, 255))
            # simple "rounded" look by softening corners via alpha mask
            mask = Image.new("L", (bg_w, bg_h), 0)
            corner_radius = max(8, min(bg_w, bg_h) // 6)

            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([0, 0, bg_w, bg_h], radius=corner_radius, fill=255)

            bg.putalpha(mask)

            # paste logo onto bg
            bg.alpha_composite(logo_img, (pad, pad))

            # center paste onto QR
            pos = ((size - bg_w) // 2, (size - bg_h) // 2)
            img.alpha_composite(bg, pos)

    # Return PNG
    out = BytesIO()
    img.save(out, format="PNG")
    return Response(content=out.getvalue(), media_type="image/png")
