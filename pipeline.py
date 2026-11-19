import pandas as pd

from solution import add_virtual_column

INPUT_FILE = "sales.csv"
OUTPUT_FILE = "revenue_by_region.csv"


def read_data(path: str) -> pd.DataFrame:
    # Read everything as text first, so we can fix the values before converting them.
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    stripping column names of spaces in the front and end, changing spaces in middle to _, and changing to lower case for consistency.
    """
    df = df.copy()
    df.columns = [column.strip().lower().replace(" ", "_") for column in df.columns]
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    dropping duplicates
    """
    return df.drop_duplicates()

def remove_non_data_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    removing header and total at the end to keep only data we will work with
    """
    is_header = df["order_id"] == "Order ID"
    is_total = df["order_id"] == "TOTAL"
    return df[~is_header & ~is_total]

def clean_str_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    data cleanup for string columns
    """
    df = df.copy()
    df["region"] = df["region"].str.strip().str.lower()
    df["product"] = df["product"].str.strip()
    return df

def fill_missing_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    every product has its own price, so we fill missing spots with prices we know based on product
    """
    df = df.copy()
    known_prices = df.groupby("product")["unit_price"].first()
    looked_up_prices = df["product"].map(known_prices)
    df["unit_price"] = df["unit_price"].fillna(looked_up_prices)
    return df

def clean_numbers(df: pd.DataFrame) -> pd.DataFrame:
    """
    cleaning up numeric columns to make them actual numbers
    """
    df = df.copy()
    df["quantity"] = pd.to_numeric(df["quantity"].str.replace(" ", "")) #replacing 1 000 with 1000 etc
    df["unit_price"] = pd.to_numeric(df["unit_price"].str.replace(",", ".")) #swapping , with .
    df["discount"] = pd.to_numeric(df["discount"].replace("", "0")) #replacing empty string with 0 as a numeric 0 discount
    return df

def cleaned_sales_data(data: pd.DataFrame) -> pd.DataFrame:
    data = rename_columns(data)
    data = remove_duplicates(data)
    data = remove_non_data_rows(data)
    data = clean_str_columns(data)
    data = clean_numbers(data)
    data = fill_missing_prices(data)
    return data

def revenue_by_region(df: pd.DataFrame) -> pd.DataFrame:
    df = add_virtual_column(df, "quantity * unit_price - discount", "revenue")

    if df.empty:
        raise ValueError("Couldn't calculate.")
    
    total_region = df.groupby("region", as_index=False)["revenue"].sum()
    return total_region


def main():
    sales = read_data(INPUT_FILE)
    sales = cleaned_sales_data(sales)
    total_rev = revenue_by_region(sales)
    total_rev.to_csv(OUTPUT_FILE, index=False)
    print(total_rev.to_string(index=False))


if __name__ == "__main__":
    main()