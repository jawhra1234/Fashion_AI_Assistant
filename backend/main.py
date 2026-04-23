from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from backend.orchestrator import FashionOrchestrator
import uvicorn

app = FastAPI(title="Fashion AI Assistant", description="AI-powered fashion recommendations")

orchestrator = FashionOrchestrator()

@app.post("/recommend")
async def recommend_outfit(
    occasion: str = Form(...),
    image: UploadFile = File(None)
):
    """
    Endpoint to get outfit recommendations.
    
    Args:
        occasion: The occasion for the outfit (e.g., "casual", "formal")
        image: Optional image file containing clothing items
    
    Returns:
        JSON response with outfit recommendations
    """
    try:
        # Read image if provided
        image_bytes = None
        if image:
            image_bytes = await image.read()
        
        # Get recommendation from orchestrator
        result = orchestrator.recommend(occasion, image_bytes)
        
        return JSONResponse(content=result)
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)