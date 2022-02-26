import json
import os

import streamlit as st

def load_layer_data(file, layer):
    if f"layer_{layer}" not in st.session_state:
        with open(file, "r") as fp:
            st.session_state[f'layer_{layer}'] = json.load(fp)

# set page config to wide layout
st.set_page_config(layout='wide')

# create sidebar
with st.sidebar:
    st.selectbox(
        label='Model',
        options=['gpt2-xl', 'gpt-neo-2.7B', 'gpt-j-6B'],
        index=0,
        key='model',
    )

# get layer file names
path = f'./visualizations/{st.session_state.model}/col_0'
layer_files = [f'{path}/{name}' for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]
layer_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

with st.sidebar:
    # create a checkbox for every layer
    for layer in range(len(layer_files)):
        st.checkbox(f'Layer {layer}', value=False, key=f'check_box_layer_{layer}', on_change=load_layer_data, args=(layer_files[layer], layer))

placeholders = [st.empty() for _ in range(len(layer_files))]

for layer in range(len(layer_files)):
    if f'layer_{layer}' in st.session_state:
        with placeholders[layer].expander(f'Layer {layer}'):
            st.components.v1.html(st.session_state[f'layer_{layer}'], height=1000, width=800, scrolling=True)
    else:
        placeholders[layer].empty()