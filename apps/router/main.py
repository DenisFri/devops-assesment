from fastapi import FastAPI, Request
import httpx

app = FastAPI()

CELL_SERVICE_MAP = {
    1: "http://nginx-cell-1",
    2: "http://nginx-cell-2",
    3: "http://nginx-cell-3",
}

@app.post("/")
async def route_request(request: Request):
    data = await request.json()
    cell_id = data.get("cellID")

    if not cell_id or cell_id not in CELL_SERVICE_MAP:
        return{"error": "Invalid or missing cellID"}
    
    target_url = CELL_SERVICE_MAP[cell_id]

    async with httpx.AsyncClient() as client:
        response = await client.get(target_url)

    return{
        "target": target_url,
        "status_code": response.status_code,
        "body": response.text,
    }