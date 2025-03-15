from fastapi import FastAPI, File, UploadFile
import requests
import os

app = FastAPI()

GEMINI_API_KEY = "AIzaSyDN5254cp4j0BzzL9a8A51oUkcF6mqVJSw"  # Replace this with your Gemini API key
GEMINI_API_URL = "https://api.gemini.com/v1/scam-detection"  # Example Gemini endpoint

@app.get("/")
def read_root():
    return {"message": "Welcome to IsItScam API!"}

@app.post("/detect-scam/")
async def detect_scam(file: UploadFile = File(...)):
    try:
        # Read the image file
        file_content = await file.read()

        # Send the file content to Gemini API
        response = requests.post(
            GEMINI_API_URL,
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
            files={"file": file_content},
        )

        # Handle response from Gemini API
        if response.status_code == 200:
            result = response.json()
            # Process and send the scam detection result back
            return {"scam_prob": result.get("probability"), "message": "Detection complete"}
        else:
            return {"message": "Error during scam detection", "status": response.status_code}

    except Exception as e:
        return {"message": f"Error: {str(e)}"}
