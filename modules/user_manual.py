import streamlit as st


def show_user_manual():

    try:

        with open(
            "docs/manual.md",
            "r",
            encoding="utf-8"
        ) as file:

            manual = file.read()

        st.markdown(manual)

    except Exception as e:

        st.error(
            f"Error Loading Manual: {e}"
        )