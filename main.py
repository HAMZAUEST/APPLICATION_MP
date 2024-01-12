import streamlit as st
from user_interface.window_main import display_data_information, display_missing_values, display_descriptive_statistics
from machine_learning.data_management.data_loader import load_data
from machine_learning.data_management.data_modeling import select_model_and_train
from machine_learning.data_management.data_preprocessing import (
    delete_columns,
    handle_missing_values_numeric,
    handle_outliers,
    handle_missing_values_categorical,
    encoding_categorical,
    scaler,
)
import time
from machine_learning.data_management.Visualization import visualize_data
import os
import streamlit as st
from streamlit_option_menu import option_menu as om





def main():

    st.set_page_config(page_title="Machine Learning in Action", page_icon="💾", menu_items={
        'About': "### Welcome to our Machine Learning in Action. \n *Version 1.0* - Created with passion by HAMZA HAFDAOUI [Hamza Hafdaoui on GitHub](https://github.com/HAMZAUEST) and SALMA AMGAROU.   [Salma Amgarou on GitHub](https://github.com/SalmaAmgarou) \n What is this? \n **Explore the fascinating world of machine learning through our Streamlit app! We've curated an interactive experience that allows you to witness machine learning algorithms in action."})
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
        .dot-matrix {
            font-family: 'VT323', monospace;
            font-size: 32px;
            margin: 0; /* Set margins to zero */
            padding: 0; /* Set padding to zero */
        }
        .title {
            font-family: 'VT323', monospace;
            font-size: 60px;
        }
        .titles {
            font-family: 'VT323', monospace;
            font-size: 32px;
        }
        .titles {
            font-family: 'VT323', monospace;
            font-size: 30px;
            color: #FFA500;
        }
        .visualize{
            font-family: 'VT323', monospace;
            font-size: 38px;
        }
        .divider{
            font-family: 'VT323', monospace;
            font-size: 32px;
            margin: 0; /* Set margins to zero */
            padding: 0; /* Set padding to zero */
            color:#000000;
        }
        </style>
        """, unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])  # Two columns of equal width
    with col1:
        st.image('images/LOGO IADS FR.png',  width=240)
    with col2:
        st.image('images/fstt.png',  width=420)
    st.markdown('<p class="title">Machine Learning In Action</p>', unsafe_allow_html=True)
    selected = om("", ['', ' '], icons=['house', 'book', 'list-task', 'gear'], menu_icon='cast', default_index=0, orientation='horizontal')
    selected
    if selected == '':



        tab1, tab2, tab3 = st.tabs(["Upload Data", "Visualize Data", "Data Modeling"])

        if 'original_df' not in st.session_state:
            st.session_state.original_df = None
        if 'preprocessed_df' not in st.session_state:
            st.session_state.preprocessed_df = None
        if 'model' not in st.session_state:
            st.session_state.model = None  # Initialize model attribute

        with tab1:
            with st.status("Downloading data..."):
                time.sleep(0.8)
                st.session_state.original_df = load_data()


            if st.session_state.original_df is not None:
                st.success('Data Loaded Successfully!')
                st.write(":red[Switch to the 'Visualize Data' tab to see the visualizations.]")
                columns = st.columns(2)
                if st.session_state.preprocessed_df is None:
                    preprocessed_df = st.session_state.original_df.copy()
                else:
                    preprocessed_df = st.session_state.preprocessed_df.copy()
                st.sidebar.markdown('<p class="divider">####################</p>', unsafe_allow_html=True)
                st.sidebar.markdown('<p class="dot-matrix">Features selection</p>', unsafe_allow_html=True)
                st.sidebar.markdown('<p class="divider">####################</p>', unsafe_allow_html=True)
                delete_columns_checkbox = st.checkbox("Enable Column Deletion")
                if delete_columns_checkbox:
                    preprocessed_df = delete_columns(preprocessed_df)
                missing_values_numeric = st.sidebar.checkbox("Handle Missing Values (Numeric)")
                if missing_values_numeric:
                    preprocessed_df = handle_missing_values_numeric(preprocessed_df)
                missing_values_categorical = st.sidebar.checkbox("Handle Missing Values (Categorical)")
                if missing_values_categorical:
                    preprocessed_df = handle_missing_values_categorical(preprocessed_df)
                handle_out = st.sidebar.checkbox("Handle Outliers (Z-score)")
                if handle_out:
                    preprocessed_df = handle_outliers(preprocessed_df, threshold=3.0)
                st.sidebar.markdown('<p class="divider">####################</p>', unsafe_allow_html=True)
                st.sidebar.markdown('<p class="dot-matrix">Data transformation</p>', unsafe_allow_html=True)
                st.sidebar.markdown('<p class="divider">####################</p>', unsafe_allow_html=True)
                encoding = st.sidebar.checkbox("Encoding categorical and numeric")
                if encoding:
                    preprocessed_df = encoding_categorical(preprocessed_df)
                scaling = st.sidebar.checkbox("Feature Scaling")
                if scaling:
                    preprocessed_df = scaler(preprocessed_df)

                st.header("")
                st.data_editor(preprocessed_df)
                st.header("")
                col2, col3 = st.columns([1, 1])
                with col2:
                    display_data_information(preprocessed_df)
                with col3:
                    display_missing_values(preprocessed_df)
                display_descriptive_statistics(preprocessed_df)

                st.session_state.preprocessed_df = preprocessed_df

        with tab2:
            visualize_data(st.session_state.preprocessed_df)
        with tab3:
            st.markdown('<p class="titles">Data Modeling</p>', unsafe_allow_html=True)
            st.header("")

            if st.session_state.preprocessed_df is None:
                st.warning("Please upload and preprocess data first.")
            else:
                task = st.radio("Select Task", ["Classification", "Regression", "Clustering"])
                select_model_and_train(st.session_state.preprocessed_df, task)
    elif selected == ' ':
        st.header("docs")


if __name__ == "__main__":
    main()

