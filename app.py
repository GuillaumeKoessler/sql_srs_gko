import ast
import io
import logging
import os

import duckdb
import pandas as pd
import streamlit as st
from datetime import date, timedelta


def check_user_solution(user_query: str) -> None:
    """
    Verification de la query SQL saisie par l'user via :
    -1: comparaison totale des tables
    -2: comparaison du nombre de lignes
    """
    try:
        sortie_df = con.execute(user_query).df()
        # Affichage de la sortie
        st.write("Table en sortie :")
        st.dataframe(sortie_df)
        try:
            sortie_df = sortie_df[solution_df.columns]
            compare_df = sortie_df.compare(solution_df)
            nb_line_diff = sortie_df.shape[0] - solution_df.shape[0]
            if compare_df.shape == (0, 0):
                st.write("Bravo !")
                st.balloons()
            else:
                st.dataframe(compare_df)
        except KeyError as e:
            nb_line_diff = sortie_df.shape[0] - solution_df.shape[0]
            st.write("Noms de colonnes non identiques")
            if nb_line_diff > 0:
                st.write(f"Le résultat à {nb_line_diff} lignes en trop")
            if nb_line_diff < 0:
                st.write(f"Le résultat à {abs(nb_line_diff)} lignes en moins")
    except duckdb.ParserException as pe:
        st.write("Erreur de syntaxe SQL")
    except duckdb.CatalogException as ce:
        st.write("La(les) table(s) n'existe(nt) pas")
    except duckdb.BinderException as be:
        st.write("La(les) colonne(s) n'existe(nt) pas")


# on crée le dossier data si il n'existe pas


if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("Creation du dossier data")
    os.mkdir("data")

# on crée la db si elle n'existe pas

if "exercices_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

# connexion a la base de données
con = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)

# Mise en page
st.header("enter your code:")

# ajout de la slide bar
with st.sidebar:
    # recuperation des themes dexo disponibles
    theme_list = (
        con.execute("SELECT DISTINCT theme FROM memory_state_df").df()["theme"].unique()
    )
    type_exec = st.selectbox(
        "Veuillez choisir une catégorie d'exercice",
        theme_list,
        index=None,
        placeholder="Sélection du type d'exercice...",
    )
    if type_exec:
        st.write("Vous avez choisi", type_exec)
        list_exe_query = (
            f"SELECT * FROM memory_state_df WHERE theme = LOWER('{type_exec}')"
        )

    else:
        list_exe_query = "SELECT * FROM memory_state_df"

    # selections des exercices en lien avec la connexion
    list_exo_sl_df = (
        con.execute(list_exe_query).df().sort_values("last_reviewed").reset_index()
    )
    st.dataframe(list_exo_sl_df)

    # recherche du script sql solution
    EXO_NAME_STR = list_exo_sl_df.loc[0, "exercice_name"]
    with open(f"answers/{EXO_NAME_STR}.sql", "r") as f:
        answer = f.read()
        solution_df = con.execute(f"{answer}").df()

# Saisie de la requête
query_str = st.text_area(
    label="Entrez ici votre requête",
)

# Calcul de la table en sortie
if query_str:
    try:
        sortie_df = con.execute(query_str).df()
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
    exe_tables = list_exo_sl_df.loc[0, "tables"]
    for tbl in exe_tables:
        st.write(f"table: {tbl}")
        table_print = con.execute(f"SELECT * FROM {tbl}").df()
        st.dataframe(table_print)
    st.write("expected:")
    st.dataframe(solution_df)

with tab3:
    st.write(answer)
