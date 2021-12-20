import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore
import streamlit as st
from pywaffle import Waffle  # type: ignore

DATA_URL = (
    "https://drive.google.com/uc?export=download&id=1_FUXeTJgZbmggsbkHtOymoufnYT1HYwM"
)


class MakePlots:
    def __init__(self):
        self.df_survey = pd.read_csv(DATA_URL)

    def display_question_one(self):
        """Mostrando como usar o streamlit"""
        st.title("Stack Overflow Data Analysis")
        st.text(
            """O Streamlit permite escrever aplicações simplesmente chamando funções."""
        )
        branch = {
            "I am a developer by profession": "professional",
            "I code primarily as a hobby": "hobby",
            "I used to be a developer by profession, but no longer am": "ex-professional",
            "I am not primarily a developer, but I write code sometimes as part of my work": "adventurer",
            "I am a student who is learning to code": "student",
        }
        self.df_survey["MainBranchSimplified"] = (
            self.df_survey["MainBranch"]
            .apply(lambda x: branch.get(x, "not_informed"))
            .astype("string")
        )
        sf_branch = (
            self.df_survey["MainBranchSimplified"].dropna().value_counts(normalize=True)
            * 100
        )
        df = pd.DataFrame(
            {"MainBranchSimplified": sf_branch.index, "Percentage": sf_branch.values}
        )
        fig, ax = plt.subplots()
        # with st.echo():
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=df.Percentage,
            title={"label": "Percentage of respondents by Activity", "loc": "left"},
            labels=[
                f"{x.MainBranchSimplified} ({round(x.Percentage, 2)}%)"
                for x in df.itertuples()
            ],
            legend={"loc": "upper left", "bbox_to_anchor": (1, 1)},
            icons="child",
            icon_size=18,
            figsize=(10, 6),
        )

        fig.gca().set_facecolor("#EEEEEE")
        fig.set_facecolor("#EEEEEE")
        st.pyplot(fig)
