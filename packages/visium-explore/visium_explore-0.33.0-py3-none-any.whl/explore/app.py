"""Streamlit app for data exploration."""
import pathlib

import streamlit as st

from explore.constants import NROWS
from explore.containers.correlations.main import correlation_container
from explore.containers.data_exploration.main import explorer_container
from explore.containers.dvc_graph.main import graph_container
from explore.containers.metrics.main import metrics_container
from explore.containers.params.main import params_container
from explore.containers.sample_df.main import display_sample_df_container
from explore.io import read_df_top_rows
from explore.sidebar import SideBarOptions, set_side_bar
from explore.utils import discover_parquet_files, parse_dvc_steps_from_dvc_yaml, select_file_container

DATA_PATH = pathlib.Path("data")


st.set_page_config(layout="wide")


def main() -> None:
    """Main function for the Streamlit app."""
    col1, col2, col3 = st.columns([1, 2, 3])
    dvc_steps = parse_dvc_steps_from_dvc_yaml()

    view_name = set_side_bar()

    with col1:
        selected_dvc_step = st.selectbox(label="DVC Step selection", options=dvc_steps, format_func=lambda x: x.name)
        dvc_step_key = f"select_box_{selected_dvc_step.name}"
        parquet_files_path_list = discover_parquet_files(selected_dvc_step.output_path)
        if len(parquet_files_path_list) > 0:
            file_path = select_file_container(parquet_files_path_list, dvc_step_key)
        else:
            st.warning("No output parquet data found for this DVC step.")
            file_path = None
    with col2:
        graph_container()
    with col3:
        with st.container(border=True):
            params_container()
            metrics_container()

    if file_path:
        sample_df = read_df_top_rows(file_path, nrows=NROWS)
        columns = list(sample_df.columns)

        if view_name == SideBarOptions.SAMPLE:
            display_sample_df_container(sample_df)
        elif view_name == SideBarOptions.EDA:
            explorer_container(file_path, dvc_step_key, columns=columns)
        elif view_name == SideBarOptions.CORRELATION:
            correlation_container(file_path, dvc_step_key, columns=columns)
        elif view_name == SideBarOptions.EXPERIMENTS:
            st.write("Work in progress...")
        elif view_name == SideBarOptions.MODEL:
            st.write("Work in progress...")
    else:
        st.warning("No parquet file found for this DVC step.")


if __name__ == "__main__":
    main()
