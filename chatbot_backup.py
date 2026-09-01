import ollama


DEFAULT_MODELS = ["llama3.2:latest", "llama3.2", "llama3.1"]


def ask_food_ai(question):

    system_prompt = """

You are MoodMeal AI, a food recommendation
and meal planning assistant.

You can help users with:

- Food recommendations
- Indian food
- South Indian food
- Vegetarian food
- Vegan food
- High-protein food
- Budget-friendly food
- Ingredients
- Recipes
- Meal planning
- Calories and nutrition information

Give concise and useful answers.

Do not make medical claims.

Do not diagnose diseases.

Do not claim that food can cure diseases.

If nutritional information is uncertain,
clearly say that it is an estimate.

"""

    last_error = None

    for model_name in DEFAULT_MODELS:
        try:
            response = ollama.chat(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            return response["message"]["content"]

        except Exception as error:
            last_error = error

    return (
        "Unable to connect to Ollama or the model is not available. "
        "Please make sure Ollama is running and the model is installed.\n\n"
        f"Error: {last_error}"
    )
