from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from dotenv import load_dotenv

load_dotenv()

def home(request):
    return render(request, 'index.html')

HUGGING_FACE_API = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HUGGING_FACE_API_KEY = os.getenv('HUGGING_FACE_API_KEY')

@api_view(["POST"])
def explain_like_five(request):
    text = request.data.get("text", "")
    level = request.data.get("level", "5")  # Default to level 5
    
    if not text:
        return Response({"error": "No text provided"}, status=400)

    # Adjust prompt based on level
    if level == "5":
        prompt = f"Explain this to a 5-year-old in very simple words: {text}"
    elif level == "10":
        prompt = f"Explain this to a 10-year-old using basic concepts: {text}"
    else:
        prompt = f"Explain this in simple terms: {text}"

    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
    }

    try:
        response = requests.post(
            HUGGING_FACE_API,
            headers=headers,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_length": 150,
                    "min_length": 50,
                    "do_sample": True
                }
            }
        )
        response.raise_for_status()

        simplified_text = response.json()[0]["summary_text"]
        return Response({"simplified_explanation": simplified_text})

    except requests.exceptions.RequestException as e:
        return Response({"error": f"AI request failed: {str(e)}"}, status=500)