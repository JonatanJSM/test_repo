from fastapi import FastAPI, Response
import requests

app = FastAPI()

SUPABASE_BASE_URL = "https://pceciwkdppctvwugwpew.supabase.co/storage/v1/object/public/qr-images/citizens/"

@app.get("/image/{filename}")
def proxy_image(filename: str):
    image_url = SUPABASE_BASE_URL + filename
    r = requests.get(image_url, stream=True)

    if r.status_code != 200:
        return Response(content="Image not found", status_code=404)

    content = r.content
    content_type = r.headers.get("Content-Type", "image/png")

    return Response(
        content=content,
        media_type=content_type,
        headers={
            "Content-Length": str(len(content)),
            "Cache-Control": "public, max-age=86400",
            "Content-Disposition": f"inline; filename={filename}",
        }
    )