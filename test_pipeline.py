import pandas as pd
from pipeline import (
    rename_columns,
    remove_non_data_rows,
    clean_str_columns,
    clean_numbers,
    cleaned_sales_data,
    revenue_by_region,
    read_data,
)


def test_rename_columns():
    df = pd.DataFrame(columns = ["Order ID", "Quantity ", "Unit Price"])
    df_result = rename_columns(df)
    assert list(df_result.columns) == ["order_id", "quantity", "unit_price"], "Column names should be lower case, with no extra spaces, and _ instead of space"

def test_remove_header_and_total():
    df = pd.DataFrame({"order_id": ["SO-1", "Order ID", "TOTAL"]})
    df_result = remove_non_data_rows(df)
    assert df_result["order_id"].tolist() == ["SO-1"], "Header and TOTAL rows should be removed"

def test_clean_region_names():
    df = pd.DataFrame({"region": [" North  ", " EAST", "west  "], "product": ["Product1", "Product1", "Product1"]})
    df_result = clean_str_columns(df)
    assert df_result["region"].tolist() == ["north", "east", "west"], "Regions should be lower case with no spaces"

def test_clean_numbers():
    df = pd.DataFrame({"quantity": ["1 234 567"], "unit_price": ["99,00"], "discount": [""]})
    df_result = clean_numbers(df)
    assert df_result["quantity"].tolist() == [1234567], "1 234 567 should become 1234567"
    assert df_result["unit_price"].tolist() == [99.0], "99,00 should become 99.0"
    assert df_result["discount"].tolist() == [0], "Empty discount value should turn into 0"

def test_missing_price_filling():
    df = pd.DataFrame({
        "Order ID": ["SO-1", "SO-2"],
        "Region": ["North", "South"],
        "Product": ["Keyboard", "Keyboard"],
        "Quantity": ["2", "1"],
        "Unit Price": ["", "89.00"],
        "Discount": ["", ""],
    })
    df_result = cleaned_sales_data(df)
    assert df_result["unit_price"].tolist() == [89.0, 89.0], "Missing price should be taken from the same product"

def test_revenue_by_region():
    df = pd.DataFrame({
        "region": ["north", "north", "south"],
        "quantity": [2, 1, 10],
        "unit_price": [10.0, 5.0, 1.0],
        "discount": [3.0, 0.0, 0.0],
    })
    df_result = revenue_by_region(df)
    assert df_result["revenue"].tolist() == [22.0, 10.0], "Correct values are north = 22 and south = 10"

def test_sales_cleanup():
    df = cleaned_sales_data(read_data("sales.csv"))
    assert len(df) == 1500, "Only 2 rows should be dopped - TOTAL and header"
    assert sorted(df["region"].unique()) == ["central", "east", "north", "south", "west"], "There should be only 5 regions"
    assert not df["unit_price"].isna().any(), "There should be price in every row"
