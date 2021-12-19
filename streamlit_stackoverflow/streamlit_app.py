import streamlit as st

from streamlit_stackoverflow.make_plots import MakePlots as mp

st.set_page_config(layout="wide")


def display_welcome():
    """Responsible for showing the welcome page."""

    st.header("This project will answer some information about Stack Overflow.")
    st.subheader("These questions will be answered:")
    st.write(
        """
        1. Percentagem of respondents who consider themseves professionals, non-professionals, students, hobbyists, etc.
        2. Distribution of respondents by location. Which country had the most participation?
        3. What is the respondent's distribution by level of education?
        4. What is the distribution of working time for each type of professional informed in question 1?
        5. Concerning people who work professionally:
            1. What is their profession?
            2. What is their level of education?
            3. What is the company's size of those people who work professionally?
        6. The average salary of respondents?
        7. Using the top five countries that have the most respondents, what is the salary of these people?
        8. What is the percentage of people who work with Python?
        9. About python:
            1. What is the salary level of people working with Python globally?
            2. In Brazil, what is the salary level?
            3. In the top five countries that have the most respondents, what is the salary level?
        10. Concerning all respondents, what operating system do they use?
        11. Concerning only people who work with Python, what operating system do they use?
        12. What is the average age of respondents?
        13. Concerning only people who work with Python, what is the average age?"""
    )


def display_index():
    """Mostra uma barra lateral"""

    options = {
        "Welcome": display_welcome,
        "Question 1": mp.display_question_one,
    }

    with st.container():
        st.title("Stack Overflow Data Analysis")
        opt = st.selectbox("Choose your question", options)

    options[opt]()


display_index()
