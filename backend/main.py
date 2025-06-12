import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
from torchvision import transforms
import torchvision.models as models
from torchvision.models import EfficientNet_B4_Weights
import torch.nn as nn
import os
from dotenv import load_dotenv
import logging
import json
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not found in environment variables.")
    raise RuntimeError("GEMINI_API_KEY not found. Please set it in your .env file.")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Google Gemini API configured successfully.")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {e}")
    raise

CLASS_NAMES = ['兰州牛肉面', '冬瓜排骨汤', '凉拌木耳', '凉拌海带丝', '凉拌豆腐皮', '凉拌黄瓜', '剁椒蒸排骨', '剁椒鱼', '剁椒鱼头', '卤水拼盘', '卤猪蹄', '卤鸡爪', '卤鸡蛋', '口水鸡', '咕噜肉', '咸蛋黄焗南瓜', '回锅肉', '地三鲜', '地锅鸡', '孜然羊肉', '宫保虾球', '宫保鸡丁', '家常豆腐', '干煸四季豆', '干煸牛肉', '干煸牛肉丝', '干煸豆角', '干煸鸡丁', '干锅土豆片', '干锅牛蛙', '干锅花菜', '干锅菜花', '干锅虾', '干锅豆腐', '干锅鸡', '木耳炒鸡蛋', '木须肉', '梅菜扣肉', '椒盐虾', '毛血旺', '水煮肉片', '水煮鱼', '清炒芥蓝', '清炒西兰花', '清蒸大闸蟹', '清蒸鲈鱼', '清蒸鲫鱼', '炒猪肝', '炒芦笋', '炒豌豆', '炒青椒', '炒青菜', '炒香干', '炒鸡心', '炒黄豆芽', '炝拌土豆丝', '炝炒白菜', '炸酱面', '炸鲜奶', '炸鸡块', '爆炒腰花', '牛排', '番茄炒蛋', '番茄牛腩', '白切鸡', '白灼虾', '盐焗鸡', '米饭', '粉蒸排骨', '粉蒸肉', '糖醋排骨', '糖醋豆腐', '糖醋里脊', '糖醋鱼', '红烧冬瓜', '红烧带鱼', '红烧排骨', '红烧牛肉面', '红烧牛腩', '红烧狮子头', '红烧猪蹄', '红烧肉', '红烧茄子', '红烧豆腐', '红烧鱼', '红烧鲤鱼', '红烧鲫鱼', '红烧鸡翅', '红烧鸡腿', '红烧鸭', '肉末茄子', '肉末豆腐', '腐乳空心菜', '腐乳肉片', '花椒鸡', '花雕鸡', '荷塘小炒', '萝卜炖牛肉', '葱姜炒蟹', '葱油拌面', '葱油鸡', '葱爆羊肉', '葱花炒蛋', '蒜苗炒肉', '蒜蓉油麦菜', '蒜蓉炒虾', '蒜蓉炒西兰花', '蒜蓉生菜', '蒜蓉粉丝蒸扇贝', '蒜香排骨', '蒸蛋', '虎皮青椒', '虾仁炒蛋', '虾仁豆腐', '蚂蚁上树', '蚝油牛肉', '蚝油生菜', '蚝油鸡翅', '蛋炒饭', '蛋花汤', '西红柿炒虾仁', '豆腐煲', '豆腐脑', '豆豉炒苦瓜', '豆豉炒蛤蜊', '豆豉蒸排骨', '豆豉鲮鱼炒苦瓜', '豆豉鸡丁', '豉汁蒸凤爪', '辣子鸡丁', '辣椒炒肉', '辣椒炒蛋', '辣白菜炒肉', '酱烧茄子', '酱爆茄子', '酱香茄子', '酸菜炒粉丝', '酸菜白肉', '酸菜豆腐汤', '酸菜鱼', '酸辣土豆丝', '酸辣汤', '酸辣粉', '酸辣肥肠', '酸辣藕片', '酸辣虾', '酸辣鱼', '雪菜炒冬笋', '青椒炒肉丝', '青花椒鱼', '香干炒肉丝', '香菇炒青菜', '香菇炒鸡', '香菇炖排骨', '香菇炖鸡', '香菇焖鸡', '香辣牛蛙', '香辣虾', '香辣蟹', '鱼头泡饼', '鱼头豆腐汤', '鱼香肉丝', '鱼香茄子', '鱼香豆腐', '鱼香鸡丝', '麻婆豆腐', '麻辣兔丁', '麻辣烤鱼', '麻辣牛肉', '麻辣豆腐', '麻辣香锅', '麻辣鸡块', '麻辣鸭脖', '黄焖排骨', '黄焖鸡米饭']
NUM_CLASSES = len(CLASS_NAMES)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'best_model_food_classifier.pth')

vision_model = models.efficientnet_b4(weights=EfficientNet_B4_Weights.IMAGENET1K_V1)
num_ftrs = vision_model.classifier[1].in_features

vision_model.classifier = nn.Sequential(
    nn.Dropout(0.3),
    nn.Linear(num_ftrs, 512),
    nn.BatchNorm1d(512),
    nn.ReLU(inplace=True),
    nn.Dropout(0.2),
    nn.Linear(512, NUM_CLASSES)
)

try:
    checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
    if 'model_state_dict' in checkpoint:
        model_state_dict = checkpoint['model_state_dict']
    else:
        model_state_dict = checkpoint
    vision_model.load_state_dict(model_state_dict)
    vision_model.eval()
    logger.info(f"Model loaded successfully from {MODEL_PATH}")
except FileNotFoundError:
    logger.error(f"Model file not found at {MODEL_PATH}")
    raise HTTPException(status_code=500, detail=f"Model file not found at {MODEL_PATH}")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise HTTPException(status_code=500, detail=f"Failed to load model: {e}")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
vision_model.to(device)
logger.info(f"Model is running on device: {device}")

image_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

try:
    gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
    logger.info("Gemini model 'gemini-1.5-flash-latest' initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Gemini model: {e}")
    raise

async def call_gemini_api(prompt: str) -> dict:
    try:
        logger.info(f"Sending prompt to Gemini...")
        response = await gemini_model.generate_content_async(prompt)
        logger.info(f"Received text from Gemini.")
        return {"success": True, "content": response.text}
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return {"success": False, "error": str(e)}

def parse_llm_response(raw_text: str) -> dict:
    try:
        json_str_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_str_match:
            json_part = json_str_match.group(0)
            llm_info = json.loads(json_part)
            logger.info("Successfully parsed JSON from Gemini response.")
            return llm_info
        else:
            logger.error(f"No JSON object found in Gemini response. Output: {raw_text}")
            return {"error": f"No JSON object found in AI response. Output: {raw_text}"}
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}. JSON part: {raw_text}")
        return {"error": f"Failed to parse JSON from AI response. Output: {raw_text}"}

app = FastAPI()


origins = ["*"]  
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/predict_food_class/")
async def predict_food(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_tensor = image_transform(image).unsqueeze(0).to(device)
        with torch.no_grad():
            outputs = vision_model(image_tensor)
        predicted_idx = torch.argmax(outputs, dim=1).item()
        predicted_class = CLASS_NAMES[predicted_idx]

        logger.info(f"Model predicted class: '{predicted_class}'")

        prompt = (
            f"You are an expert cuisine assistant. For the food named '{predicted_class.replace('_', ' ')}', provide the following information. "
            f"Your response MUST be a valid JSON object with no other text, comments, or markdown formatting outside of it. "
            f"The JSON structure must have the following keys:\n"
            f"- 'food_name': string (the well-formatted name of the food).\n"
            f"- 'recipe': an object containing:\n"
            f"  - 'ingredients': an array of strings.\n"
            f"  - 'steps': an array of strings for the cooking steps.\n"
            f"- 'calories': string (e.g., '300-400 kcal per serving').\n"
            f"- 'nutrition': string (a summary of nutritional info).\n"
            f"- 'youtube_tutorial_link': string (A URL to a relevant and popular YouTube cooking tutorial. If none is found, this should be an empty string '')."
        )

        result = await call_gemini_api(prompt)

        if not result["success"]:
            raise HTTPException(status_code=500, detail=f"Gemini API error: {result['error']}")
        llm_info = parse_llm_response(result["content"])
        if "error" in llm_info:
            final_response = {
                "predicted_food": predicted_class,  
                "llm_info": llm_info  
            }
            return JSONResponse(status_code=502, content=final_response)

        if 'youtube_tutorial_link' in llm_info and llm_info['youtube_tutorial_link']:
            llm_info['youtube'] = llm_info['youtube_tutorial_link']
        else:
            llm_info['youtube'] = ""

        final_response = {
            "predicted_food": predicted_class, 
            "llm_info": llm_info  
        }
        return JSONResponse(content=final_response)

    except Exception as e:
        logger.error(f"Error in prediction endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))