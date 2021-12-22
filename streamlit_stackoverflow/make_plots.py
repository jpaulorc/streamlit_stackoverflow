import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import seaborn as sns  # type: ignore
import streamlit as st
from matplotlib import pyplot as plt  # type: ignore
from numpy.core.fromnumeric import size
from pandas.core.frame import DataFrame  # type: ignore
from pywaffle import Waffle  # type: ignore

DATA_FILE = (
    "data/survey_results_public.csv"
    # "https://drive.google.com/uc?export=download&id=1_FUXeTJgZbmggsbkHtOymoufnYT1HYwM"
)

DATA_FILE_2020 = "data/survey_results_public_2020.csv"


class MakePlots:
    def __init__(self):
        self.df_survey = pd.read_csv(DATA_FILE)

    def set_header(self, question_number: int):
        """Display the phrase on each page header according to the number of the question"""
        questions = {
            1: "Percentagem of respondents who consider themselves professionals, non-professionals, students, hobbyists, etc.",
            2: "Distribution of respondents by location. Which country had the most participation?",
            3: "What is the respondent's distribution by level of education?",
            4: "What is the distribution of working time for each type of professional informed in question 1?",
            5: "Concerning people who work professionally:",
            6: "The average salary of respondents?",
            7: "Using the top five countries that have the most respondents, what is the salary of these people?",
            8: "What is the percentage of people who work with Python?",
            9: "About python:",
            10: "Concerning all respondents, what operating system do they use?",
            11: "Concerning only people who work with Python, what operating system do they use?",
            12: "What is the average age of respondents?",
            13: "Concerning only people who work with Python, what is the average age?",
        }
        st.header(f"Question {question_number}:")
        st.subheader(questions[question_number])
        if question_number == 5:
            st.markdown(
                """
                1. What is their profession?
                2. What is their level of education?
                3. What is the company's size of those people who work professionally?
                ---
                """
            )
        elif question_number == 9:
            st.markdown(
                """
                1. What is the salary level of people working with Python globally?
                2. In Brazil, what is the salary level?
                3. In the top five countries that have the most respondents, what is the salary level?
                ---
                """
            )
        else:
            st.markdown(
                """
                ---
                """
            )

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

            st.write(fig)
            st.write(
                "The chart only presents countries with more than one percent of respondents."
            )

    def set_ed_level_simplified(self) -> dict:
        """Return a Dictionary containing the education level simplified"""
        return {
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

    def display_question_three(self):
        """Display the container of the third question"""
        self.set_header(question_number=3)
        self.df_survey["EducationLevel"] = (
            self.df_survey["EdLevel"]
            .apply(lambda x: self.set_ed_level_simplified().get(x, "Not Informed"))
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
            :, ["YearsCodePro", "MainBranch", "MainBranchSimplified"]
        ]
        df_new.loc[:, ["YearsCodePro"]] = df_new.loc[:, ["YearsCodePro"]].apply(
            pd.to_numeric, args=("coerce",), axis="index"
        )
        df_new = (
            df_new.groupby("MainBranchSimplified")
            .apply(lambda x: x.fillna(x.mean()))
            .dropna()
        )
        df_new = df_new.join(
            df_new.groupby("MainBranchSimplified")["YearsCodePro"].aggregate(
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

    def set_devtype_group(self) -> dict:
        """Return a Dictionary containing the dev type grouped by function"""
        return {
            "Developer, full-stack": "Dev, full-stack",
            "Developer, mobile;Developer, front-end;Developer, full-stack;Developer, back-end": "Dev, full-stack, mobile",
            "Developer, mobile;Developer, full-stack": "Dev, full-stack; mobile",
            "Developer, back-end": "Dev, back-end",
            "Developer, front-end": "Dev, front-end",
            "Developer, front-end;Developer, full-stack;Developer, back-end": "Dev, full-stack",
            "Developer, front-end;Developer, full-stack": "Dev, full-stack",
            "Developer, full-stack;Developer, back-end": "Dev, full-stack",
            "Developer, mobile": "Developer, mobile",
            "Developer, desktop or enterprise applications": "Dev, desktop",
            "Developer, desktop or enterprise applications;Developer, back-end": "Dev, desktop",
            "Developer, front-end;Developer, desktop or enterprise applications;Developer, full-stack;Developer, back-end": "Dev, desktop",
            "Developer, embedded applications or devices": "Dev, embedded",
            "Data scientist or machine learning specialist": "Data Scientist",
            "Developer, desktop or enterprise applications;Developer, full-stack;Developer, back-end": "Dev, desktop",
            "Other (please specify):": "Other",
            "Developer, mobile;Developer, front-end": "Dev, mobile; front-end",
            "Developer, desktop or enterprise applications;Developer, full-stack": "Dev, desktop",
            "Developer, front-end;Developer, back-end": "Dev, full-stack",
            "Developer, full-stack;DevOps specialist": "Dev;DevOps",
            "Developer, back-end;DevOps specialist": "Dev;DevOps",
            "Engineer, data;Developer, back-end": "Engineer, data",
            "Engineer, data": "Engineer, data",
            "Developer, full-stack;Engineering manager": "Dev, full-stack;Eng manager",
            "Engineering manager": "Engineer manager",
            "Developer, full-stack;Developer, back-end;DevOps specialist": "Dev;DevOps",
            "Developer, mobile;Developer, front-end;Developer, desktop or enterprise applications;Developer, full-stack;Developer, back-end": "Dev, full-stack",
            "Developer, QA or test": "Dev;QA",
            "Developer, mobile;Developer, front-end;Developer, full-stack": "Dev, full-stack",
            "Developer, front-end;Developer, full-stack;Developer, back-end;DevOps specialist": "Dev;DevOps",
            "DevOps specialist": "DevOps",
            "Developer, mobile;Developer, back-end": "Dev;DevOps",
            "Developer, desktop or enterprise applications;Developer, embedded applications or devices": "Dev, embedded, desktop",
            "Developer, game or graphics": "Dev, game or graphics",
            "Senior Executive (C-Suite, VP, etc.)": "Senior Executive",
            "Developer, back-end;Engineering manager": "Dev, back-end;Eng manager",
            "Developer, full-stack;Student": "Dev, full-stack;Student",
            "Data scientist or machine learning specialist;Developer, back-end": "Data scientist;Dev, back-end",
            "Developer, full-stack;System administrator": "Dev, full-stack;System adm",
            "Developer, front-end;Developer, full-stack;Developer, back-end;Designer": "Dev, full-stack;Designer",
            "Developer, back-end;Developer, embedded applications or devices": "Dev, back-end;embedded",
            "Developer, mobile;Developer, full-stack;Developer, back-end": "Dev, full-stack",
            "Academic researcher": "Student",
            "Developer, front-end;Designer": "Dev, front-end;Designer",
            "Developer, front-end;Developer, full-stack;Developer, back-end;Database administrator": "Dev, full-stack;System adm",
            "Developer, full-stack;Other (please specify)": "Dev, full-stack",
            "Developer, front-end;Developer, desktop or enterprise applications;Developer, back-end": "Dev, back-end;embedded",
            "Data scientist or machine learning specialist;Data or business analyst": "Data Scientist",
            "Developer, front-end;Developer, full-stack;Developer, back-end;Developer, QA or test": "Dev;QA",
            "Developer, full-stack;Senior Executive (C-Suite, VP, etc.)": "Senior Executive",
            "Other (please specify):;Developer, back-end": "Dev, back-end",
            "Developer, back-end;Student": "Dev, back-end;Student",
            "Developer, back-end;DevOps specialist;Engineer, site reliability": "Dev;DevOps",
            "Developer, front-end;Developer, desktop or enterprise applications": "Dev, front-end, desktop",
            "Developer, front-end;Developer, full-stack;Developer, back-end;Student": "Dev, full-stack;Student",
            "Engineer, data;Data scientist or machine learning specialist": "Engineer, data;Data scientist",
            "Developer, mobile;Developer, front-end;Developer, back-end": "Dev, full-stack, mobile",
            "Developer, full-stack;Data scientist or machine learning specialist": "Dev, full-stack;Data scientist",
            "Developer, full-stack;Designer": "Dev, full-stack;Designer",
            "Developer, back-end;Engineer, site reliability": "Dev, back-end;Engineer",
            "Developer, full-stack;Product manager": "Dev, full-stack;PM",
            "Data or business analyst": "Data Scientist",
        }

    def display_question_five(self):
        """Display the container of the fifth question"""
        self.set_header(question_number=5)

        df = self.df_survey.loc[:]
        df.set_index(keys=["MainBranch"], inplace=True)
        df = df.loc[["I am a developer by profession"], :]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("What is their profession?")
            df1 = df.loc[:]
            df1 = df1["DevType"].dropna().value_counts(normalize=True) * 100
            df1 = pd.DataFrame({"DevType": df1.index, "Percentage": df1.values})
            df1["DevTypeGrouped"] = (
                df1["DevType"]
                .apply(lambda x: self.set_devtype_group().get(x, "not_used"))
                .astype("string")
            )
            df1 = df1.loc[df1["DevTypeGrouped"] != "not_used"]
            df1 = df1.loc[:, ["DevTypeGrouped", "Percentage"]]
            df1 = (
                df1.groupby(["DevTypeGrouped"])
                .sum()
                .reset_index()
                .sort_values(by=["Percentage"], ascending=False)
            )
            fig = px.bar(
                df1,
                y="DevTypeGrouped",
                x="Percentage",
                labels={
                    "DevTypeGrouped": "Professions",
                    "Percentage": "Percentage(%)",
                },
                title="Professions of professional workers ",
            )
            st.write(fig)

        with col2:
            st.subheader("What is their level of education?")
            df2 = df.loc[:]
            df2 = df["EdLevel"].dropna().value_counts(normalize=True) * 100
            df2 = pd.DataFrame({"EdLevel": df2.index, "Percentage": df2.values})
            df2["EdLevelSimplified"] = (
                df2["EdLevel"]
                .apply(
                    lambda x: self.set_ed_level_simplified().get(x, "Something Else")
                )
                .astype("string")
            )

            fig = px.pie(
                df2,
                values="Percentage",
                names="EdLevelSimplified",
                title="The professional distribution by level of education",
                labels={
                    "EdLevelSimplified": "Education Level",
                    "Percentage": "Percentage(%)",
                },
            )
            st.write(fig)

        st.subheader(
            "What is the company's size of those people who work professionally?"
        )
        df3 = self.df_survey.loc[:, ["MainBranch", "OrgSize"]]
        df3.set_index(keys=["MainBranch"], inplace=True)
        df3 = df3.loc[["I am a developer by profession"], :]
        just_me = "Just me - I am a freelancer, sole proprietor, etc."
        df3.loc[df3["OrgSize"] == just_me, "OrgSize"] = "1 employee"
        df3 = (
            df3.dropna()
            .value_counts(subset=["OrgSize"], normalize=False)
            .reset_index(name="count")
        )

        fig, ax = plt.subplots()
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(x="count", y="OrgSize", data=df3)
        ax.set(xlabel="Number of employee", ylabel="Company Size")
        plt.title("Company size of the professional workers")
        st.write(fig)

    def get_difference(self, a, b):
        return ((a - b) / b) * 100

    def display_question_six(self):
        self.set_header(question_number=6)
        df_survey_2020 = pd.read_csv(DATA_FILE_2020)
        mean_salary_2021 = self.df_survey["ConvertedCompYearly"].mean()
        mean_salary_2020 = df_survey_2020["ConvertedComp"].mean()

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                f"The average salary of 2021",
                f"{mean_salary_2021:,.2f}",
                f"{self.get_difference(mean_salary_2021, mean_salary_2020):.2f}%",
            )
        with col2:
            st.metric(
                f"The average salary of 2020",
                f"{mean_salary_2020:,.2f}",
                f"{self.get_difference(mean_salary_2020, mean_salary_2021):.2f}%",
            )

    def display_question_seven(self):
        self.set_header(question_number=7)

    def display_question_eight(self):
        self.set_header(question_number=8)

    def display_question_nine(self):
        self.set_header(question_number=9)

    def display_question_ten(self):
        self.set_header(question_number=10)

    def display_question_eleven(self):
        self.set_header(question_number=11)

    def display_question_twelve(self):
        self.set_header(question_number=12)

    def display_question_thirteen(self):
        self.set_header(question_number=13)
