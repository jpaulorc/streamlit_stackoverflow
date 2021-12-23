import pandas as pd


class QuestionTwo:
    def __init__(self, df_survey):
        self.df = self.set_general_information(df_survey)

    def set_general_information(self, df_survey):
        sf_country = df_survey["Country"].dropna().value_counts(normalize=True) * 100
        return pd.DataFrame(
            {"Country": sf_country.index, "Percentage": sf_country.values}
        )

    def get_max_metric(self):
        return self.df.loc[self.df["Percentage"] == self.df["Percentage"].max()]

    def get_brazil_metric(self):
        return self.df.loc[self.df["Country"] == "Brazil"]

    def get_min_metric(self):
        return self.df.loc[self.df["Percentage"] == self.df["Percentage"].min()]

    def get_question_chart(self):
        return self.df.loc[self.df["Percentage"] > 1]
