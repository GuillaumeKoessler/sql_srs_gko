import io

import duckdb
import pandas as pd

# connection a la database
con = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)

# -------------------------------------------------------------------------------------
# EXERCICES LISTE
# -------------------------------------------------------------------------------------

exe_list = {
    "theme": ["cross_joins", "cross_joins", "window_functions"],
    "exercice_name": ["beverages_and_food", "sizes_and_trademarks", "simple_window"],
    "tables": [["beverages", "food_items"], ["sizes", "trademarks"],  ["simple_window"]],
    "last_reviewed": ["1980-01-01", "1970-01-01", "1970-01-01"],
}
memory_state_df = pd.DataFrame(exe_list)
con.execute("CREATE TABLE IF NOT EXISTS memory_state_df AS SELECT * FROM memory_state_df")

# -------------------------------------------------------------------------------------
# DONNEES SOURCES POUR EXO
# -------------------------------------------------------------------------------------

CSV_BEVERAGES = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV_BEVERAGES))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV_FOOD = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV_FOOD))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

CSV_SIZE = """
size
XS
M
L
XL
"""
sizes = pd.read_csv(io.StringIO(CSV_SIZE))
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")

CSV_TRADEMARKS = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""
trademarks = pd.read_csv(io.StringIO(CSV_TRADEMARKS))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")

# -------------------------------------------------------------------------------------
# CROSS-JOINS EXERCICES
# -------------------------------------------------------------------------------------
