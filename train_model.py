import io
import os
import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


DATASET_PATH = "dataset/food_dataset.csv"
MODEL_PATH = "model/food_model.pkl"


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


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = load_dataset(DATASET_PATH)


# --------------------------------------------------
# 2. Convert Yes / No values
# --------------------------------------------------

df["vegetarian"] = df["vegetarian"].map({
    "Yes": 1,
    "No": 0
})

df["vegan"] = df["vegan"].map({
    "Yes": 1,
    "No": 0
})


# --------------------------------------------------
# 3. Create recommendation target
# --------------------------------------------------

df["target_score"] = (
    df["health_score"] * 0.35
    + (df["protein"] / df["protein"].max()) * 20
    + (1 - df["price"] / df["price"].max()) * 20
    + (1 - df["calories"] / df["calories"].max()) * 10
)


# --------------------------------------------------
# 4. Features
# --------------------------------------------------

features = [
    "cuisine",
    "meal_type",
    "vegetarian",
    "vegan",
    "calories",
    "protein",
    "carbs",
    "fat",
    "price",
    "spice_level",
    "prep_time",
    "health_score",
    "mood",
    "situation",
    "activity"
]


X = df[features]
y = df["target_score"]


# --------------------------------------------------
# 5. Feature categories
# --------------------------------------------------

categorical_features = [
    "cuisine",
    "meal_type",
    "spice_level",
    "mood",
    "situation",
    "activity"
]


numeric_features = [
    "vegetarian",
    "vegan",
    "calories",
    "protein",
    "carbs",
    "fat",
    "price",
    "prep_time",
    "health_score"
]


# --------------------------------------------------
# 6. Preprocessing
# --------------------------------------------------

preprocessor = ColumnTransformer(

    transformers=[

        (
            "categorical",

            OneHotEncoder(
                handle_unknown="ignore"
            ),

            categorical_features
        ),

        (
            "numeric",

            StandardScaler(),

            numeric_features
        )

    ]
)


# --------------------------------------------------
# 7. Random Forest
# --------------------------------------------------

model = RandomForestRegressor(

    n_estimators=200,

    random_state=42

)


# --------------------------------------------------
# 8. Pipeline
# --------------------------------------------------

pipeline = Pipeline(

    steps=[

        (
            "preprocessor",
            preprocessor
        ),

        (
            "model",
            model
        )

    ]

)


# --------------------------------------------------
# 9. Train / Test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)


# --------------------------------------------------
# 10. Train
# --------------------------------------------------

pipeline.fit(
    X_train,
    y_train
)


# --------------------------------------------------
# 11. Evaluate
# --------------------------------------------------

predictions = pipeline.predict(
    X_test
)


mae = mean_absolute_error(
    y_test,
    predictions
)


r2 = r2_score(
    y_test,
    predictions
)


print()
print("=" * 45)
print("MOODMEAL AI - MODEL TRAINING")
print("=" * 45)

print(
    "Mean Absolute Error:",
    round(mae, 3)
)

print(
    "R2 Score:",
    round(r2, 3)
)


# --------------------------------------------------
# 12. Create model directory
# --------------------------------------------------

os.makedirs(
    "model",
    exist_ok=True
)


# --------------------------------------------------
# 13. Save model
# --------------------------------------------------

joblib.dump(
    pipeline,
    MODEL_PATH
)


print()
print("Model saved successfully:")
print(MODEL_PATH)
print("=" * 45)