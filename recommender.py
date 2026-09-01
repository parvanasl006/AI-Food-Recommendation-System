import io
import os

import pandas as pd
import joblib


MODEL_PATH = "model/food_model.pkl"
DATASET_PATH = "dataset/food_dataset.csv"


def load_dataset(path):
    """Load dataset even when each CSV row is wrapped in quotes."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found: {path}")

    with open(path, "r", encoding="utf-8-sig", newline="") as csv_file:
        rows = [line.strip() for line in csv_file if line.strip()]

    cleaned_rows = []
    for row in rows:
        if row.startswith('"') and row.endswith('"'):
            row = row[1:-1]
        cleaned_rows.append(row)

    csv_buffer = io.StringIO("\n".join(cleaned_rows))
    df = pd.read_csv(csv_buffer)
    df.columns = df.columns.str.strip().str.lower()
    return df


model = joblib.load(
    MODEL_PATH
)

food_data = load_dataset(DATASET_PATH)


def recommend_food(

    cuisine,
    meal_type,
    vegetarian,
    vegan,
    budget,
    spice_level,
    mood,
    situation,
    activity,

    top_n=5

):

    data = food_data.copy()

    data["vegetarian"] = data["vegetarian"].astype(str).str.strip().str.lower().map({
        "yes": 1,
        "no": 0
    })

    data["vegan"] = data["vegan"].astype(str).str.strip().str.lower().map({
        "yes": 1,
        "no": 0
    })


    # ---------------------------------------------
    # Dietary filtering
    # ---------------------------------------------

    if vegetarian == 1:

        data = data[
            data["vegetarian"] == 1
        ].copy()


    if vegan == 1:

        data = data[
            data["vegan"] == 1
        ].copy()


    # ---------------------------------------------
    # Budget filtering
    # ---------------------------------------------

    data = data[
        data["price"] <= budget
    ].copy()


    # ---------------------------------------------
    # Meal filtering
    # ---------------------------------------------

    meal_data = data[
        data["meal_type"].str.lower()
        == meal_type.lower()
    ]


    if not meal_data.empty:

        data = meal_data.copy()


    # ---------------------------------------------
    # Cuisine filtering
    # ---------------------------------------------

    cuisine_data = data[
        data["cuisine"].str.lower()
        == cuisine.lower()
    ]


    if not cuisine_data.empty:

        data = cuisine_data.copy()


    # ---------------------------------------------
    # No results
    # ---------------------------------------------

    if data.empty:

        return []


    # ---------------------------------------------
    # Create input dataframe
    # ---------------------------------------------

    user_data = pd.DataFrame({

        "cuisine":
            [cuisine] * len(data),

        "meal_type":
            [meal_type] * len(data),

        "vegetarian":
            [vegetarian] * len(data),

        "vegan":
            [vegan] * len(data),

        "calories":
            data["calories"].values,

        "protein":
            data["protein"].values,

        "carbs":
            data["carbs"].values,

        "fat":
            data["fat"].values,

        "price":
            data["price"].values,

        "spice_level":
            [spice_level] * len(data),

        "prep_time":
            data["prep_time"].values,

        "health_score":
            data["health_score"].values,

        "mood":
            [mood] * len(data),

        "situation":
            [situation] * len(data),

        "activity":
            [activity] * len(data)

    })


    # ---------------------------------------------
    # ML score
    # ---------------------------------------------

    data = data.copy()
    data.loc[:, "ml_score"] = model.predict(
        user_data
    )


    # ---------------------------------------------
    # Mood match
    # ---------------------------------------------

    data.loc[:, "mood_score"] = (

        data["mood"]
        .str.lower()
        .eq(mood.lower())
        .astype(int)

    )


    # ---------------------------------------------
    # Situation match
    # ---------------------------------------------

    data.loc[:, "situation_score"] = (

        data["situation"]
        .str.lower()
        .eq(situation.lower())
        .astype(int)

    )


    # ---------------------------------------------
    # Activity match
    # ---------------------------------------------

    data.loc[:, "activity_score"] = (

        data["activity"]
        .str.lower()
        .eq(activity.lower())
        .astype(int)

    )


    # ---------------------------------------------
    # Spice match
    # ---------------------------------------------

    data.loc[:, "spice_score"] = (

        data["spice_level"]
        .str.lower()
        .eq(spice_level.lower())
        .astype(int)

    )


    # ---------------------------------------------
    # Normalize ML score
    # ---------------------------------------------

    minimum = data["ml_score"].min()
    maximum = data["ml_score"].max()


    if maximum != minimum:

        data.loc[:, "ml_normalized"] = (

            (data["ml_score"] - minimum)
            /
            (maximum - minimum)

        )

    else:

        data.loc[:, "ml_normalized"] = 1


    # ---------------------------------------------
    # Hybrid score
    # ---------------------------------------------

    data.loc[:, "final_score"] = (

        data["ml_normalized"] * 0.40

        + data["mood_score"] * 0.20

        + data["situation_score"] * 0.15

        + data["activity_score"] * 0.10

        + data["spice_score"] * 0.05

        + (data["health_score"] / 10) * 0.10

    )


    # ---------------------------------------------
    # Sort
    # ---------------------------------------------

    data = data.sort_values(

        by="final_score",

        ascending=False

    )


    return data.head(
        top_n
    ).to_dict(
        orient="records"
    )