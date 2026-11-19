import pandas as pd
from solution import add_virtual_column


def test_float_values():
    df = pd.DataFrame([[3, 1.5]] * 2, columns = ["quantity", "price"])
    df_result = add_virtual_column(df, "quantity * price", "total")
    assert df_result["total"].tolist() == [4.5, 4.5], "Should work with decimals" 

def test_empty_result_when_dividing():
    df = pd.DataFrame([[4, 2]] * 2, columns = ["label_one", "label_two"])
    df_result = add_virtual_column(df, "label_one / label_two", "label_three")
    assert df_result.empty, "Dividing is not a supported"

def test_column_case_sensitivity():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_result = add_virtual_column(df, "Label_one + label_two", "label_three")
    assert df_result.empty, "Label_one amd label_one are two different columns due to case sensitivity"

