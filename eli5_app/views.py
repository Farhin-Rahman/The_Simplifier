from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from dotenv import load_dotenv

load_dotenv()

def home(request):
    return render(request, 'index.html')

# Back to the original model
HUGGING_FACE_API = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HUGGING_FACE_API_KEY = os.getenv('HUGGING_FACE_API_KEY')

@api_view(["POST"])
def explain_like_five(request):
    text = request.data.get("text", "")
    level = request.data.get("level", "5")
    
    if not text:
        return Response({"error": "No text provided"}, status=400)

    # Simplify based on level without changing the input text
    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
    }

    try:
        # First get a summary
        response = requests.post(
            HUGGING_FACE_API,
            headers=headers,
            json={
                "inputs": text,
                "parameters": {
                    "max_length": 100,
                    "min_length": 30,
                    "do_sample": False
                }
            }
        )
        response.raise_for_status()

        # Get the initial summary
        simplified_text = response.json()[0]["summary_text"]

        # Add level-specific prefix
        if level == "5":
            simplified_text = "In simple words: " + simplified_text
        elif level == "10":
            simplified_text = "To explain simply: " + simplified_text
        else:
            simplified_text = "To put it clearly: " + simplified_text

        return Response({"simplified_explanation": simplified_text})

    except requests.exceptions.RequestException as e:
        return Response({"error": f"AI request failed: {str(e)}"}, status=500)