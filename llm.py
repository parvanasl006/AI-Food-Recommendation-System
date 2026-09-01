import ollama


MODEL_NAME = "llama3.2"


def ollama_available():

    try:

        ollama.list()

        return True

    except Exception:

        return False


def explain_recommendation(

    food,
    mood,
    situation,
    activity,
    budget

):

    if not ollama_available():

        return (
            "Ollama is not running. "
            "Please start Ollama and try again."
        )


    prompt = f"""

You are MoodMeal AI, an intelligent food
recommendation assistant.

The machine learning recommendation engine
selected the following food.

Food:
{food["food"]}

Cuisine:
{food["cuisine"]}

Calories:
{food["calories"]}

Protein:
{food["protein"]} grams

Price:
₹{food["price"]}

Health Score:
{food["health_score"]}/10


USER CONTEXT

Mood:
{mood}

Situation:
{situation}

Activity:
{activity}

Budget:
₹{budget}


Explain why this food is a suitable recommendation.

Your answer must contain:

1. Mood compatibility
2. Situation compatibility
3. Activity compatibility
4. Budget compatibility
5. One nutritional advantage

Use simple language.

Do not invent nutritional values.

Do not make medical claims.

Do not claim that the food treats or cures diseases.

Keep the answer under 150 words.

"""


    response = ollama.chat(

        model=MODEL_NAME,

        messages=[

            {

                "role": "user",

                "content": prompt

            }

        ]

    )


    return response[
        "message"
    ][
        "content"
    ]