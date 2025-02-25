from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Your Hugging Face API details
HUGGING_FACE_API = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HUGGING_FACE_API_KEY = "your_hugging_face_api_key"

# View to render the homepage
def home(request):
    return render(request, 'index.html')

# API view to handle text explanation
@api_view(["POST"])
def explain_like_five(request):
    text = request.data.get("text", "")
    if not text:
        return Response({"error": "No text provided"}, status=400)

    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
    }

    try:
        response = requests.post(HUGGING_FACE_API, headers=headers, json={"inputs": text})
        response.raise_for_status()  # Raises an error for 4xx/5xx responses

        simplified_text = response.json()[0]["summary_text"]
        return Response({"simplified_explanation": simplified_text})

    except requests.exceptions.RequestException as e:
        return Response({"error": f"AI request failed: {str(e)}"}, status=500)
