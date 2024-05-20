import io

import duckdb
import pandas as pd
import streamlit as st

# connections a la base de données
con = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)

# query de la solution + table solution
# ANSWER_STR = """
# SELECT * FROM beverages
# CROSS JOIN food_items
# """
# solution_df = duckdb.sql(ANSWER_STR).df()

# Mise en page
st.header("enter your code:")

# ajout de la slide bar
with st.sidebar:
    type_exec = st.selectbox(
        "Veuillez choisir une catégorie d'exercice",
        ("Cross_Joins", "GroupBy", "Window_Functions"),
        index=None,
        placeholder="Sélection du type d'exercice...",
    )
    st.write("Vous avez choisi", type_exec)

# selections des exercices en lien avec la connections
list_exo_sl_df = con.execute(
    f"SELECT * FROM memory_state_df WHERE theme = LOWER('{type_exec}')"
).df()
st.dataframe(list_exo_sl_df)

# Saisie de la requête
query_str = st.text_area(
    label="Entrez ici votre requête",
)

# Calcul de la table en sortie
# if query_str:
#     try:
#         sortie_df = duckdb.sql(query_str).df()
#         # Affichage de la sortie
#         st.write("Table en sortie :")
#         st.dataframe(sortie_df)
#         try:
#             sortie_df = sortie_df[solution_df.columns]
#             st.dataframe(sortie_df.compare(solution_df))
#         except KeyError as e:
#             st.write("Noms de colonnes non identiques")
#
#         nb_line_diff = sortie_df.shape[0] - solution_df.shape[0]
#         if nb_line_diff > 0:
#             st.write(f"Le résultat à {nb_line_diff} lignes en trop")
#         if nb_line_diff < 0:
#             st.write(f"Le résultat à {abs(nb_line_diff)} lignes en moins")
#     except:
#         st.write("Erreur de syntaxe SQL")

# Présentation des sources
# tab2, tab3 = st.tabs(["Tables", "Solution"])
#
# with tab2:
#     st.write("table: beverages")
#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected:")
#     st.dataframe(solution_df)
#
# with tab3:
#     st.write(ANSWER_STR)
