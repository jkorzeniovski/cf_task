# Virtual columns in a pandas DataFrame

The `add_virtual_column` function is in `solution.py`. `pipeline.py` uses it on `sales.csv` - it cleans the data, adds a revenue column and writes the total revenue of each region to `revenue_by_region.csv`. My tests are in `test_solution.py` and `test_pipeline.py`, next to the sample tests from the task. There is also a small script, `report.py`, which I used to count the problems in the data (the numbers further down come from it).

## Setup and running

You need Python 3 with pandas and pytest:

```
pip install pandas pytest
```

Then, from the project folder, run the pipeline with:

```
python pipeline.py
```

and all the tests with:

```
python -m pytest
```

## Assumptions

For the function, I allowed spaces anywhere around column names and operators, so `quantity*price` and ` quantity * price ` both work. Every column used in the role has to exist in the DataFrame and names are case sensitive. If something is wrong with the role or with the new column name, the function just returns an empty DataFrame.

For the pipeline, revenue is `quantity * unit_price - discount`, where the discount is an amount taken off the whole line, not a percentage. An empty discount means there was no discount, so I set it to 0. I assumed each product always has the same price, so when the unit price is missing I take it from other rows with the same product.

Some numbers are written in a different format: a quantity like `1 762` has a space as a thousands separator (read as 1762), and a price like `59,00` has a comma instead of a dot (read as 59.00). Negative quantities look like returns, so I kept them - they lower the revenue of their region. Rows that are the same in every column are the same order line exported twice, so I keep only one copy. The `TOTAL` row at the bottom of the file is not a sale, so it is skipped. In the output file region names are in lower case (e.g. `north`).

## Problems in `sales.csv`

The file has 1507 rows under the header. Two of them are not data (a repeated header and the `TOTAL` row), which leaves 1505, and after removing duplicates there are exactly 1500 rows - one for each order from SO-10001 to SO-11500. No row that could be fixed was dropped.

What I found and what I did with it:

- The `Quantity ` column name has a trailing space. All column names are trimmed, lower-cased and spaces are replaced with `_`.
- There is a repeated header row in the middle of the file (1 row) - removed.
- There is a `TOTAL` row at the end (1 row) - removed.
- 5 rows are exact duplicates - only one copy is kept.
- Region names are messy: 8 have extra spaces (like `" North"` or `"west  "`) and 10 have the wrong letter case (like `EAST`). Some rows have both, so it's 15 rows in total. Spaces are stripped and everything is lower-cased.
- 4 quantities use a space as a thousands separator - the space is removed.
- 6 quantities are negative - kept as returns.
- 7 unit prices use a comma instead of a dot - changed to a dot.
- 4 unit prices are missing - filled with the price of the same product.
- 963 discounts are empty - set to 0.

I also checked products and order dates. No product had extra spaces, but the pipeline strips them anyway just in case, and all the dates were fine.
