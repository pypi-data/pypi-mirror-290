from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import aiofiles
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join(os.getenv("VIRTUAL_ENV"),"lib/python3.12/site-packages/agentbuddy/webapp/fe/static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def get():
    async with aiofiles.open(os.path.join(os.getenv("VIRTUAL_ENV"),"lib/python3.12/site-packages/agentbuddy/webapp/fe/static/chat.html"), mode="r") as file:
        content = await file.read()
    return HTMLResponse(content=content)

# Avvio dell'app con uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
