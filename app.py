import io

import duckdb
import pandas as pd
import streamlit as st

# données sources

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

# query de la solution + table solution
ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
solution_df = duckdb.sql(ANSWER_STR).df()

# Mise en page
st.header("enter your code:")

# ajout de la slide bar
with st.sidebar:
    type_exec = st.selectbox(
        "Veuillez choisir une catégorie d'exercice",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Sélection du type d'exercice...",
    )
    st.write("Vous avez choisi", type_exec)

# Saisie de la requête
query_str = st.text_area(
    label="Entrez ici votre requête",
)

# Calcul de la table en sortie
if query_str:
    try:
        sortie_df = duckdb.sql(query_str).df()
        # Affichage de la sortie
        st.write("Table en sortie :")
        st.dataframe(sortie_df)
        try:
            sortie_df = sortie_df[solution_df.columns]
            st.dataframe(sortie_df.compare(solution_df))
        except KeyError as e:
            st.write("Noms de colonnes non identiques")

        nb_line_diff = sortie_df.shape[0] - solution_df.shape[0]
        if nb_line_diff > 0:
            st.write(f"Le résultat à {nb_line_diff} lignes en trop")
        if nb_line_diff < 0:
            st.write(f"Le résultat à {abs(nb_line_diff)} lignes en moins")
    except:
        st.write("Erreur de syntaxe SQL")

# Présentation des sources
tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution_df)

with tab3:
    st.write(ANSWER_STR)
