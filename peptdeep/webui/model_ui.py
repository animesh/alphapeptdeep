import streamlit as st
from peptdeep.settings import global_settings
import multiprocessing

def predict():
    batch_size_ms2 = st.number_input('Batch size to predict MS2', value = global_settings['model_mgr']['predict']['batch_size_ms2'])
    global_settings['model_mgr']['predict']['batch_size_ms2'] = batch_size_ms2
    batch_size_rt_ccs = st.number_input('Batch size to predict RT and CCS', value = global_settings['model_mgr']['predict']['batch_size_rt_ccs'])
    global_settings['model_mgr']['predict']['batch_size_rt_ccs'] = batch_size_rt_ccs

    default_instrument = st.selectbox('Instrument',(list(global_settings['model_mgr']['instrument_group'].keys())),index = 0)
    global_settings['model_mgr']['default_instrument'] = default_instrument
    default_nce = st.number_input('NCE', value = global_settings['model_mgr']['default_nce'],disabled=(default_instrument=='timsTOF'))
    global_settings['model_mgr']['default_nce'] = default_nce


    verbose = st.checkbox('Verbose', global_settings['model_mgr']['predict']['verbose'])
    global_settings['model_mgr']['predict']['verbose'] = verbose
    multiprocessing = st.checkbox('Multiprocessing', global_settings['model_mgr']['predict']['multiprocessing'])
    global_settings['model_mgr']['predict']['multiprocessing'] = multiprocessing

def model():
    model_url = st.text_input('URL (or local path) to download the pre-trained models',value = global_settings['model_url'])
    global_settings['model_url'] = model_url
    
    thread_num = st.number_input('Thread number', value = multiprocessing.cpu_count()-1)
    global_settings['thread_num'] = thread_num

    global_settings['model_mgr']['external_ms2_model'] = st.text_input('External MS2 model')
    global_settings['model_mgr']['external_rt_model'] = st.text_input('External RT model')
    global_settings['model_mgr']['external_ccs_model'] = st.text_input('External CCS model')


def show():

    st.write("# Model Configuration")
    st.write('### Model parameters')
    model()

    model_type = st.selectbox('Model type',(global_settings['model_mgr']['model_choices']),index = 0)
    global_settings['model_mgr']['model_type'] = model_type
    global_settings['model_mgr']['mask_modloss'] = bool(
        st.checkbox('mask modloss (setting intensity values to zero for neutral loss of PTMs (e.g. -98 Da for Phospho@S/T))',
        value = global_settings['model_mgr']['mask_modloss'])
    )

    st.write('### Prediction parameters')
    predict()
