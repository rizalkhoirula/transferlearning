from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import torch
from torchvision import transforms
from transformers import ViTForImageClassification, ViTConfig # Pastikan ViTConfig juga diimport
import os 
from dotenv import load_dotenv 

# Muat variabel lingkungan dari file .env
load_dotenv() 

import google.generativeai as genai 

# --- Konfigurasi Model & Data ---
# Gunakan os.path.join untuk path yang lebih robust
# Asumsi folder 'model' berada di direktori yang sama dengan main.py
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'padang_food_classifier_state_dict.pth')


CLASS_NAMES = [
    "ayam_goreng", "ayam_pop", "daging_rendang", "dendeng_batokok",
    "gulai_ikan", "gulai_tambusu", "gulai_tunjang", "telur_balado", "telur_dadar"
]
NUM_CLASSES = len(CLASS_NAMES)

MODEL_NAME_FOR_LOAD = "google/vit-base-patch16-224"

# --- SOLUSI: Load model dasar dengan ignore_mismatched_sizes=True ---
# Ini akan memuat arsitektur dan bobot semua lapisan KECUALI lapisan klasifikasi terakhir
# karena kita akan menggantinya dengan bobot fine-tuned kita.
model = ViTForImageClassification.from_pretrained(
    MODEL_NAME_FOR_LOAD,
    num_labels=NUM_CLASSES, # Ini penting untuk arsitektur akhir
    ignore_mismatched_sizes=True # <-- INI PERUBAHAN UTAMA
)

try:
    # Muat state_dict model yang sudah terlatih ke dalam model yang sudah diinisialisasi
    # Karena kita sudah menggunakan ignore_mismatched_sizes=True di atas,
    # load_state_dict ini seharusnya tidak lagi melihat mismatch pada head.
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    model.eval() 
except FileNotFoundError:
    raise HTTPException(status_code=500, detail=f"Model file not found at {MODEL_PATH}. Please ensure the 'model' directory exists and contains the model file.")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}. Check model architecture and file integrity.")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# --- Inisialisasi Gemini Pro ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in a .env file or directly.")
    
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro') 

# --- Inisialisasi FastAPI ---
app = FastAPI(
    title="Padang Food Classifier & LLM API",
    description="API untuk mengklasifikasi makanan Padang dan memberikan informasi resep/kalori dari Gemini Pro.",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    return {"message": "Hello World! Food Classifier API is running."}

@app.post("/predict_food_class/")
async def predict_food_class(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_transformed = image_transform(image).unsqueeze(0).to(device)

        model.eval()
        with torch.no_grad():
            outputs = model(image_transformed)
        
        predicted_idx = torch.argmax(outputs.logits, dim=1).item()
        predicted_class_name = CLASS_NAMES[predicted_idx]

        prompt_llm = f"Berikan resep lengkap, perkiraan kalori, dan informasi nutrisi umum untuk makanan bernama '{predicted_class_name}' dalam format JSON. Format JSON harus memiliki kunci 'resep', 'kalori', dan 'nutrisi'. Contoh: {{'resep': '...', 'kalori': '...', 'nutrisi': '...'}}."
        
        llm_response = gemini_model.generate_content(prompt_llm)
        llm_text = llm_response.text

        import json
        try:
            llm_info = json.loads(llm_text)
        except json.JSONDecodeError:
            llm_info = {
                "resep": f"Gagal mendapatkan resep dari LLM. Ini adalah {predicted_class_name}.",
                "kalori": "Gagal mendapatkan kalori.",
                "nutrisi": "Gagal mendapatkan nutrisi.",
                "raw_llm_response": llm_text 
            }

        return JSONResponse(content={
            "predicted_food": predicted_class_name,
            "llm_info": llm_info
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/get_food_info/{food_name}")
async def get_food_info(food_name: str):
    if food_name not in CLASS_NAMES:
        raise HTTPException(status_code=400, detail=f"Food '{food_name}' not in recognized list.")
    
    prompt_llm = f"Berikan resep lengkap, perkiraan kalori, dan informasi nutrisi umum untuk makanan bernama '{food_name}' dalam format JSON. Format JSON harus memiliki kunci 'resep', 'kalori', dan 'nutrisi'. Contoh: {{'resep': '...', 'kalori': '...', 'nutrisi': '...'}}."
    
    llm_response = gemini_model.generate_content(prompt_llm)
    llm_text = llm_response.text

    try:
        llm_info = json.loads(llm_text)
    except json.JSONDecodeError:
        llm_info = {
            "food_name": food_name,
            "resep": f"Gagal mendapatkan resep untuk {food_name} dari LLM.",
            "kalori": "Gagal mendapatkan kalori.",
            "nutrisi": "Gagal mendapatkan nutrisi.",
            "raw_llm_response": llm_text 
        }

    return JSONResponse(content=llm_info)