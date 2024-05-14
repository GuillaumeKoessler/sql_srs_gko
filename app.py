import duckdb
import streamlit as st
import pandas as pd
import duckdb as duck

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

# Présentation de la source
st.write("Table source (df) :")
st.dataframe(df)

# Saisie de la requête
query = st.text_area(label="Entrez ici votre requête")

# Calcul de la table en sortie
sortie = duckdb.sql(query).df()

# affichage de la sortie

st.write("Table en sortie :")
st.dataframe(sortie)
