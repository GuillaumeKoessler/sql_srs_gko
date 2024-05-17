import streamlit as st
import pandas as pd
import duckdb
import io

# données sources

csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''
beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))

# query de la solution + table solution
answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
solution = duckdb.sql(answer).df()

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
query = st.text_area(label="Entrez ici votre requête",)

# Calcul de la table en sortie
if query:
    sortie = duckdb.sql(query).df()
    # Affichage de la sortie
    st.write("Table en sortie :")
    st.dataframe(sortie)

# Présentation des sources
tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution)

with tab3:
    st.write(answer)
