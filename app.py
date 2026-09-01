import json
import os
from datetime import datetime

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

history = []

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

def normalize_bool(value):
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}

def get_diet_mode(vegetarian_value, vegan_value):
    if normalize_bool(vegan_value):
        return "vegan"
    if normalize_bool(vegetarian_value):
        return "vegetarian"
    return "nonveg"

def parse_ollama_response(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(text)
        if isinstance(data, list):
            items = [str(x).strip() for x in data]
            return [x for x in items if x][:5]
        if isinstance(data, dict):
            for key in ("recommendations", "items", "suggestions", "meals"):
                if key in data and isinstance(data[key], list):
                    items = [str(x).strip() for x in data[key]]
                    return [x for x in items if x][:5]
    except json.JSONDecodeError:
        pass

    lines = []
    for line in text.splitlines():
        s = line.strip().strip("-*• ").strip()
        if s:
            lines.append(s)

    cleaned = [x for x in lines if x and not x.lower().startswith(("here are", "sure", "based on"))]
    return cleaned[:5]

def ask_ollama_recommendations(mood, cuisine, meal_type, diet_mode, budget, spice_level, activity):
    prompt = f"""
You are a meal planner AI.
Return exactly 5 different meal recommendations based only on the user inputs.
Use valid JSON in this format:
["Meal 1", "Meal 2", "Meal 3", "Meal 4", "Meal 5"]

Inputs:
- mood: {mood}
- cuisine: {cuisine}
- meal_type: {meal_type}
- diet: {diet_mode}
- budget: ₹{budget}
- spice_level: {spice_level}
- activity: {activity}

Rules:
- Respect diet strictly.
- Respect cuisine.
- Keep meals realistic and different.
- Do not include explanations.
- Return only JSON.
"""
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.8},
            },
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        text = payload.get("response", "")
        parsed = parse_ollama_response(text)
        if parsed:
            return parsed
    except Exception:
        pass

    return [
        "Balanced protein bowl",
        "Fresh salad bowl",
        "Healthy rice plate",
        "Comfort meal bowl",
        "Light dinner wrap",
    ]

def ask_ollama_chat(message):
    prompt = f"""
You are a helpful food and wellness assistant.
Answer as a natural chatbot, in 1-2 short, friendly sentences.
Keep the reply practical and specific to food and health.
User message: {message}
"""
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": 0.8},
            },
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        content = payload.get("message", {}).get("content", "").strip()
        if content:
            return content
    except Exception:
        pass

    return "I can help with meal ideas, mood-based suggestions, and balanced food choices. Try asking for a breakfast, lunch, dinner, protein-heavy, or vegetarian option."

def build_recommendations(mood, cuisine, meal_type, vegetarian_value, vegan_value, budget, spice_level, activity):
    diet_mode = get_diet_mode(vegetarian_value, vegan_value)
    return ask_ollama_recommendations(
        mood=mood,
        cuisine=cuisine,
        meal_type=meal_type,
        diet_mode=diet_mode,
        budget=budget,
        spice_level=spice_level,
        activity=activity,
    )[:5]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    mood = request.form.get("mood", "neutral")
    meal_type = request.form.get("meal_type", "Lunch")
    cuisine = request.form.get("cuisine", "Indian")
    vegetarian = request.form.get("vegetarian", "1")
    vegan = request.form.get("vegan", "0")
    budget = request.form.get("budget", "200")
    spice_level = request.form.get("spice_level", "Medium")
    activity = request.form.get("activity", "Medium")

    try:
        budget = int(budget)
    except ValueError:
        budget = 200

    recommendations = build_recommendations(
        mood=mood,
        cuisine=cuisine,
        meal_type=meal_type,
        vegetarian_value=vegetarian,
        vegan_value=vegan,
        budget=budget,
        spice_level=spice_level,
        activity=activity,
    )

    result = {
        "meal_name": recommendations[0],
        "recommendations": recommendations,
        "summary": (
            f"Based on your {mood.lower()} mood and {meal_type.lower()} preference, "
            f"these {cuisine} options fit your {spice_level.lower()} spice level, "
            f"{activity.lower()} activity level, and ₹{budget} budget."
        ),
        "mood": mood,
        "meal_type": meal_type,
        "cuisine": cuisine,
        "budget": budget,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    history.append(result)
    return render_template("result.html", result=result)

@app.route("/history")
def show_history():
    return render_template("history.html", history=history)

@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json(force=True, silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return {"reply": "Tell me about your mood or preferred foods."}

    reply = ask_ollama_chat(message)
    return {"reply": reply}

if __name__ == "__main__":
    app.run(debug=True)