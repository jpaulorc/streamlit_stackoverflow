import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import seaborn as sns  # type: ignore
import streamlit as st
from matplotlib import pyplot as plt  # type: ignore
from numpy.core.fromnumeric import size
from pandas.core.frame import DataFrame  # type: ignore
from pywaffle import Waffle  # type: ignore

DATA_URL = (
    "https://drive.google.com/uc?export=download&id=1_FUXeTJgZbmggsbkHtOymoufnYT1HYwM"
)


class MakePlots:
    def __init__(self):
        self.df_survey = pd.read_csv(DATA_URL)

    def set_header(self, question_number: int):
        """Display the phrase on each page header according to the number of the question"""
        questions = {
            1: "Percentagem of respondents who consider themselves professionals, non-professionals, students, hobbyists, etc.",
            2: "Distribution of respondents by location. Which country had the most participation?",
            3: "What is the respondent's distribution by level of education?",
            4: "What is the distribution of working time for each type of professional informed in question 1?",
            5: """Concerning people who work professionally:
                    1. What is their profession?
                    2. What is their level of education?
                    3. What is the company's size of those people who work professionally?""",
            6: "The average salary of respondents?",
            7: "Using the top five countries that have the most respondents, what is the salary of these people?",
            8: "What is the percentage of people who work with Python?",
            9: """About python:
                    1. What is the salary level of people working with Python globally?
                    2. In Brazil, what is the salary level?
                    3. In the top five countries that have the most respondents, what is the salary level?""",
            10: "Concerning all respondents, what operating system do they use?",
            11: "Concerning only people who work with Python, what operating system do they use?",
            12: "What is the average age of respondents?",
            13: "Concerning only people who work with Python, what is the average age?",
        }
        st.header(f"Question {question_number}:")
        st.subheader(questions[question_number])

    def display_question_one(self):
        """Display the container of the firt question"""
        self.set_header(question_number=1)

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

        # display the chart
        st.pyplot(fig)

        # displys the metric
        df_main = self.df_survey.loc[:, ["MainBranchSimplified", "MainBranch"]]
        df_simplified = self.df_survey.loc[:, ["MainBranchSimplified", "MainBranch"]]

        df_main.set_index(keys=["MainBranchSimplified"], inplace=True)
        df_simplified.set_index(keys=["MainBranch"], inplace=True)

        df_main = df_main["MainBranch"]
        df_simplified = df_simplified["MainBranchSimplified"]

        for i, j in sf_branch.items():
            branch = "".join(df_main.get(i, "Not Informed").unique())
            simplefied_branch = "".join(
                df_simplified.get(branch, "Not Informed").unique()
            )
            st.metric(
                f"{branch} ({simplefied_branch})",
                f"{j:.2f}%",
            )

    def display_question_two(self):
        """Display the container of the second question"""
        self.set_header(question_number=2)
        sf_country = (
            self.df_survey["Country"].dropna().value_counts(normalize=True) * 100
        )
        df = pd.DataFrame(
            {"Country": sf_country.index, "Percentage": sf_country.values}
        )

        col1, col2 = st.columns(2)

        with col1:
            df_max = df.loc[df["Percentage"] == df["Percentage"].max()]
            st.metric(
                f"The country with the highest participation is {''.join(df_max['Country'])} with: ",
                f"{''.join(round(df_max['Percentage'], 3).astype(str))}%",
            )

            df_bra = df.loc[df["Country"] == "Brazil"]
            st.metric(
                f"Brazil has a participation rate of ",
                f"{''.join(round(df_bra['Percentage'], 3).astype(str))}%",
            )

            df_min = df.loc[df["Percentage"] == df["Percentage"].min()]
            st.metric(
                f"{len(df_min['Country'])} countries have the lowest participation with: ",
                f"{''.join(round(df_min['Percentage'].min(), 3).astype(str))}%",
            )

        with col2:
            df = df.loc[df["Percentage"] > 1]
            fig, ax = plt.subplots()
            sns.set_theme(style="whitegrid")
            sns.barplot(x="Percentage", y="Country", data=df)

            plt.title("Distribution of respondents by location")

            st.pyplot(fig)
            st.write(
                "The chart only presents countries with more than one percent of respondents."
            )

    def display_question_three(self):
        """Display the container of the third question"""
        self.set_header(question_number=3)

        ed_level = {
            "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": "Secondary school",
            "Bachelor’s degree (B.A., B.S., B.Eng., etc.)": "Bachelor’s degree",
            "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)": "Master’s degree",
            "Other doctoral degree (Ph.D., Ed.D., etc.)": "Other doctoral degree",
            "Some college/university study without earning a degree": "Study without degree",
            "Something else": "Something else",
            "Professional degree (JD, MD, etc.)": "Professional degree",
            "Primary/elementary school": "Primary/elementary",
            "Associate degree (A.A., A.S., etc.)": "Associate degree",
        }
        self.df_survey["EducationLevel"] = (
            self.df_survey["EdLevel"]
            .apply(lambda x: ed_level.get(x, "Not Informed"))
            .astype("string")
        )
        sf_education = (
            self.df_survey["EducationLevel"].dropna().value_counts(normalize=True) * 100
        )
        df = pd.DataFrame(
            {"EducationLevel": sf_education.index, "Percentage": sf_education.values}
        )

        col1, col2 = st.columns(2)
        with col1:
            df_max = df.loc[df["Percentage"] == df["Percentage"].max()]
            st.metric(
                """As we can see most users who answered the questions have Bachelor's Degree with """,
                f"{''.join(round(df_max['Percentage'], 2).astype(str))}%",
            )
            df["Percentage"] = df["Percentage"].round(2)
            table = go.Figure(
                data=[
                    go.Table(
                        header=dict(
                            values=list(df.columns),
                            fill_color="paleturquoise",
                            align="left",
                        ),
                        cells=dict(
                            values=df.transpose().values.tolist(),
                            fill_color="lavender",
                            align="left",
                        ),
                    )
                ]
            )
            st.write(table)
        with col2:
            fig = px.pie(
                df,
                values="Percentage",
                names="EducationLevel",
                title="The respondent's distribution by level of education",
            )
            st.write(fig)

    def display_question_four(self):
        """Display the container of the fourth question"""
        self.set_header(question_number=4)

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
        df_new = self.df_survey.loc[
            :, ["YearsCode", "MainBranch", "MainBranchSimplified"]
        ]
        col_numbers = ["YearsCode", "YearsCodePro"]
        df_new.loc[:, ["YearsCode"]] = df_new.loc[:, ["YearsCode"]].apply(
            pd.to_numeric, args=("coerce",), axis="index"
        )
        df_new = df_new.groupby("MainBranchSimplified").apply(
            lambda x: x.fillna(x.mean())
        )
        df_new = df_new.join(
            df_new.groupby("MainBranchSimplified")["YearsCode"].aggregate(
                ["mean", "min", "max"]
            ),
            on="MainBranchSimplified",
        )
        df_new = df_new.drop_duplicates(keep="first")

        branch = df_new.MainBranchSimplified.unique()

        fig = go.Figure(
            data=[
                go.Bar(name="Min", x=branch, y=df_new["min"]),
                go.Bar(name="Mean", x=branch, y=df_new["mean"]),
                go.Bar(name="Max", x=branch, y=df_new["max"]),
            ]
        )
        fig.update_layout(barmode="group")

        col1, col2 = st.columns(2)
        with col1:
            df_table = df_new.sort_values(by=["MainBranchSimplified"])
            df_table = df_table.loc[:, ["MainBranch", "mean", "min", "max"]]
            df_table = df_table.drop_duplicates(keep="first")
            df_table["mean"] = df_table["mean"].round(2)
            table = go.Figure(
                data=[
                    go.Table(
                        header=dict(
                            values=list(df_table.columns),
                            fill_color="paleturquoise",
                            align="left",
                        ),
                        cells=dict(
                            values=df_table.transpose().values.tolist(),
                            fill_color="lavender",
                            align="left",
                        ),
                    )
                ]
            )
            st.write(table)
        with col2:
            st.write(fig)

    def display_question_five(self):
        """Display the container of the fifth question"""
        self.set_header(question_number=5)

    def display_question_six(self):
        pass

    def display_question_seven(self):
        pass

    def display_question_eight(self):
        pass

    def display_question_nine(self):
        pass

    def display_question_ten(self):
        pass

    def display_question_eleven(self):
        pass

    def display_question_twelve(self):
        pass

    def display_question_thirteen(self):
        pass
