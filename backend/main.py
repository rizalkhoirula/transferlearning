from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
from torchvision import transforms
import torchvision.models as models
from torchvision.models import ViT_B_16_Weights
import torch.nn as nn
import os
from dotenv import load_dotenv
import logging
import json
import requests

# --- Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Load .env ---
load_dotenv()
BAICHUAN_API = os.getenv("BAICHUAN_API")
if not BAICHUAN_API:
    logger.error("BAICHUAN_API token not found in environment variables.")
    raise RuntimeError("BAICHUAN_API token not found. Please set it in your environment variables.")

# --- Class & Model Setup ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'padang_food_classifier_state_dict.pth')
CLASS_NAMES = [
    "ayam_goreng", "ayam_pop", "daging_rendang", "dendeng_batokok",
    "gulai_ikan", "gulai_tambusu", "gulai_tunjang", "telur_balado", "telur_dadar"
]
NUM_CLASSES = len(CLASS_NAMES)

# --- Vision Transformer Setup ---
model = models.vit_b_16(weights=ViT_B_16_Weights.IMAGENET1K_SWAG_LINEAR_V1)
model.heads = nn.Sequential(
    nn.Dropout(p=0.2, inplace=True),
    nn.Linear(in_features=768, out_features=NUM_CLASSES, bias=True)
)

try:
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    model.eval()
except FileNotFoundError:
    raise HTTPException(status_code=500, detail=f"Model not found at {MODEL_PATH}")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to load model: {e}")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# --- Function to call Baichuan API ---
def call_baichuan_api(prompt: str) -> dict:
    api_url = "https://api.baichuan-ai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {BAICHUAN_API}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "Baichuan2-Turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        logger.info(f"Calling Baichuan API with prompt: {prompt}")
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        resp_json = response.json()

        if "choices" in resp_json and len(resp_json["choices"]) > 0:
            content = resp_json["choices"][0]["message"]["content"]
            return {"success": True, "content": content}
        else:
            return {"success": False, "error": "Invalid response format from Baichuan API."}

    except requests.exceptions.HTTPError as http_err:
        return {"success": False, "error": f"HTTP error: {http_err}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# --- FastAPI ---
app = FastAPI(
    title="Padang Food Classifier & Baichuan2 API",
    description="Classifies Padang food and provides recipe, calorie, and nutrition info via Baichuan2 API.",
    version="1.1.0"
)

# --- CORS configuration ---
origins = [
    "http://localhost:5173",  # Vite default dev server
    "http://localhost:3000",  # another possible frontend port
    # Add your production frontend URLs here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or use ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Padang Food Classifier API with Baichuan2 API is running."}

@app.post("/predict_food_class/")
async def predict_food_class(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_tensor = image_transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(image_tensor)
        predicted_idx = torch.argmax(outputs, dim=1).item()
        predicted_class = CLASS_NAMES[predicted_idx]

        prompt = (
            f"Give me the recipe, estimated calories, and general nutrition info "
            f"for an Indonesian food called '{predicted_class}'. Respond in JSON format "
            "with keys: 'recipe', 'calories', and 'nutrition'."
        )
        result = call_baichuan_api(prompt)

        if not result["success"]:
            raise HTTPException(status_code=500, detail=f"Baichuan API error: {result['error']}")

        response = result["content"]

        # Extract JSON from response text
        json_start = response.find('{')
        json_end = response.rfind('}')
        if json_start != -1 and json_end != -1:
            json_part = response[json_start:json_end+1]
            try:
                llm_info = json.loads(json_part)
            except json.JSONDecodeError:
                llm_info = {
                    "recipe": f"Unable to parse response. Raw output: {response}",
                    "calories": "N/A",
                    "nutrition": "N/A"
                }
        else:
            llm_info = {
                "recipe": "Failed to extract JSON from response.",
                "calories": "N/A",
                "nutrition": "N/A",
                "raw_response": response
            }

        return JSONResponse(content={
            "predicted_food": predicted_class,
            "llm_info": llm_info
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")

@app.get("/get_food_info/{food_name}")
async def get_food_info(food_name: str):
    if food_name not in CLASS_NAMES:
        raise HTTPException(status_code=400, detail=f"Food '{food_name}' not in recognized list.")

    prompt = (
        f"Give me the recipe, estimated calories, and general nutrition info "
        f"for an Indonesian food called '{food_name}'. Respond in JSON format "
        "with keys: 'recipe', 'calories', and 'nutrition'."
    )

    result = call_baichuan_api(prompt)

    if not result["success"]:
        raise HTTPException(status_code=500, detail=f"Baichuan API error: {result['error']}")

    response = result["content"]

    # Extract JSON from response text
    json_start = response.find('{')
    json_end = response.rfind('}')
    if json_start != -1 and json_end != -1:
        json_part = response[json_start:json_end+1]
        try:
            llm_info = json.loads(json_part)
        except json.JSONDecodeError:
            llm_info = {
                "recipe": f"Unable to parse response. Raw output: {response}",
                "calories": "N/A",
                "nutrition": "N/A"
            }
    else:
        llm_info = {
            "recipe": "Failed to extract JSON from response.",
            "calories": "N/A",
            "nutrition": "N/A",
            "raw_response": response
        }

    return JSONResponse(content={
        "food_name": food_name,
        "llm_info": llm_info
    })
