from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from dotenv import load_dotenv

load_dotenv()

# Change back to the original model
HUGGING_FACE_API = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HUGGING_FACE_API_KEY = os.getenv('HUGGING_FACE_API_KEY')

@api_view(["POST"])
def explain_like_five(request):
    text = request.data.get("text", "")
    if not text:
        return Response({"error": "No text provided"}, status=400)

    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
    }

    try:
        response = requests.post(
            HUGGING_FACE_API, 
            headers=headers, 
            json={"inputs": text}
        )
        response.raise_for_status()

        simplified_text = response.json()[0]["summary_text"]
        return Response({"simplified_explanation": simplified_text})

    except requests.exceptions.RequestException as e:
        return Response({"error": f"AI request failed: {str(e)}"}, status=500)