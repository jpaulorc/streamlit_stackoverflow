import pandas as pd
import streamlit as st


class MakePlots:
    def read_files(self):
        df_schema = pd.read_csv("")
        pass

    def display_question_one(self):
        """Mostrando como usar o streamlit"""
        st.title("Stack Overflow Data Analysis")
        st.text(
            """O Streamlit permite escrever aplicações simplesmente chamando funções."""
        )
        print(st)
