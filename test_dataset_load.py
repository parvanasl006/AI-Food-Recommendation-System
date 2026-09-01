import train_model


def test_dataset_loads_with_expected_columns():
    df = train_model.load_dataset("dataset/food_dataset.csv")
    assert "cuisine" in df.columns
    assert "mood" in df.columns
    assert len(df.columns) > 1
