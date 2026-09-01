from recommender import recommend_food


results = recommend_food(

    cuisine="Indian",

    meal_type="Dinner",

    vegetarian=1,

    vegan=0,

    budget=200,

    spice_level="Medium",

    mood="Stressed",

    situation="Relaxing",

    activity="Low"

)


print()
print("=" * 50)
print("FOOD RECOMMENDATIONS")
print("=" * 50)


if not results:

    print("No food found.")


else:

    for index, food in enumerate(
        results,
        start=1
    ):

        print()

        print(
            index,
            food["food"]
        )

        print(
            "Price: ₹",
            food["price"]
        )

        print(
            "Calories:",
            food["calories"]
        )

        print(
            "Protein:",
            food["protein"],
            "g"
        )

        print(
            "Health:",
            food["health_score"],
            "/10"
        )

        print(
            "AI Score:",
            round(
                food["final_score"] * 100,
                2
            ),
            "%"
        )