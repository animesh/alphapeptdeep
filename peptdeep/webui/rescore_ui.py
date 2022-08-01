import streamlit as st
import pandas as pd
import os
import time

from peptdeep.settings import global_settings
from peptdeep.webui.ui_utils import files_in_folder_pandas

def show():
    """Streamlit page that displays information on how to rescore."""
    st.write("# DDA Rescoring")

    raw_folder = st.text_input('Raw folder')
    #st.write('The current raw folder is', raw_folder)
    MS_type = st.selectbox(
     'MS file type',
     ('Raw', 'MGF', 'hdf'))
    #st.write('You selected:', MS_type)
    if raw_folder:
        st.text(
            f"PeptDeep looks for MS files in {raw_folder}.\nThese can be selected in the new experiment tab.\nYou can add own files to this folder."
            )

        st.write("### Existing files")

        raw_files = files_in_folder_pandas(raw_folder,MS_type)

        st.table(raw_files)

    result_folder = st.text_input('Result folder')
    #st.write('The current result folder is', result_folder)
    PSM_type = st.selectbox(
     'PSM file type',
     ('AlphaPept', 'pFind', 'MaxQuant'))
    if PSM_type == 'AlphaPept':
        psm_type = 'ms_data.hdf'
    elif PSM_type == 'pFind':
        psm_type = 'spectra'
    elif PSM_type == 'MaxQuant':
        psm_type = 'msms.txt'
    #st.write('You selected:', PSM_type)
    if result_folder:
        st.text(
            f"PeptDeep looks for PSM files in {result_folder}.\nThese can be selected in the new experiment tab.\nYou can add own files to this folder."
        )

        st.write("### Existing files")

        result_files = files_in_folder_pandas(result_folder,psm_type)

        st.table(result_files)