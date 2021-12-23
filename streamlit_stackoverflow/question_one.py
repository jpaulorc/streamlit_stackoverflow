import pandas as pd
from matplotlib import pyplot as plt  # type: ignore
from pywaffle import Waffle  # type: ignore


class QuestionOne:
    """Responsible to process all information about the question one"""

    def __init__(self, df_survey):
        self.df, self.sf = self.set_general_information(df_survey)

    def set_general_information(self, df_survey: pd.core.frame.DataFrame):
        """Responsible to process all information to use in question one.

        Args:
            df_survey (pandas.core.frame.DataFrame): The Stack Overflow Survey Dataframe

        Returns:
            tuple[pd.core.frame.DataFrame, pd.core.series.Series]: All proccessed information
        """
        branch = {
            "I am a developer by profession": "professional",
            "I code primarily as a hobby": "hobby",
            "I used to be a developer by profession, but no longer am": "ex-professional",
            "I am not primarily a developer, but I write code sometimes as part of my work": "adventurer",
            "I am a student who is learning to code": "student",
        }
        df_survey["MainBranchSimplified"] = (
            df_survey["MainBranch"]
            .apply(lambda x: branch.get(x, "not_informed"))
            .astype("string")
        )
        sf = (
            df_survey["MainBranchSimplified"].dropna().value_counts(normalize=True)
            * 100
        )
        df = pd.DataFrame({"MainBranchSimplified": sf.index, "Percentage": sf.values})

        return df, sf

    def question_one_chart(self) -> plt.figure:
        """Responsible to make the chart.

        Returns:
            plt.figure: Waffle Chart
        """
        return plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=self.df.Percentage,
            title={"label": "Percentage of respondents by Activity", "loc": "left"},
            labels=[
                f"{x.MainBranchSimplified} ({round(x.Percentage, 2)}%)"
                for x in self.df.itertuples()
            ],
            legend={"loc": "upper left", "bbox_to_anchor": (1, 1)},
            icons="child",
            icon_size=18,
            figsize=(10, 6),
        )

    def question_one_metric(self, df_survey: pd.core.frame.DataFrame) -> list:
        """Responsible to proccess all information to use in the metrics.

        Args:
            df_survey (pandas.core.frame.DataFrame): The Stack Overflow Survey Dataframe

        Returns:
            list: A list containing the branches of work and the percentage of each one of them
        """
        df_main = df_survey.loc[:, ["MainBranchSimplified", "MainBranch"]]
        df_main.set_index(keys=["MainBranchSimplified"], inplace=True)
        df_main = df_main["MainBranch"]
        df_simplified = df_survey.loc[:, ["MainBranchSimplified", "MainBranch"]]
        df_simplified.set_index(keys=["MainBranch"], inplace=True)
        df_simplified = df_simplified["MainBranchSimplified"]

        metric_list = list()
        for i, j in self.sf.items():
            branch = "".join(df_main.get(i, "Not Informed").unique())
            simplefied_branch = "".join(
                df_simplified.get(branch, "Not Informed").unique()
            )
            metric_list.append([branch, simplefied_branch, j])
        return metric_list
