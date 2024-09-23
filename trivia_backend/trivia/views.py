# trivia/views.py
import requests
from django.shortcuts import render
from django.http import JsonResponse

def fetch_trivia(request):
    # Set the OpenTDB API URL
    opentdb_url = "https://opentdb.com/api.php?amount=5"  # Fetch 5 questions as an example

    # Fetch data from the OpenTDB API
    response = requests.get(opentdb_url)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Failed to fetch trivia questions"}, status=500)
