from llm import explain_recommendation


food = {

    "food": "Vegetable Soup",

    "cuisine": "Continental",

    "calories": 180,

    "protein": 5,

    "price": 100,

    "health_score": 10

}


result = explain_recommendation(

    food=food,

    mood="Stressed",

    situation="Relaxing",

    activity="Low",

    budget=200

)


print()
print("=" * 50)
print("OLLAMA AI EXPLANATION")
print("=" * 50)
print()
print(result)