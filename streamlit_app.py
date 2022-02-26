import json
import os

import streamlit as st

def load_layer(model, layer, placeholders, file):
    if st.session_state[f'layer_{layer}']:
        with placeholders[layer]:
            with st.expander(f'Layer {layer}'):
                with open(file, "r") as fp:
                    data = json.load(fp)
                st.components.v1.html(fp, height=1000, width=800, scrolling=True)
    else:
        placeholders[layer] = st.empty()

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

path = f'./visualizations/{st.session_state.model}'

# get number of directories in path
num_cols = len([name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))])
col_path = f'{path}/col_0'

layer_files = [f'{col_path}/{name}' for name in os.listdir(col_path) if os.path.isfile(os.path.join(col_path, name))]
print(f"num layers = {len(layer_files)}")

# create a placeholder for every layer
placeholders = [st.empty() for _ in range(len(layer_files))]

with st.sidebar:
    # create a checkbox for every layer
    for layer in range(len(layer_files)):
        st.checkbox(f'Layer {layer}', value=False, key=f'layer_{layer}', on_change=load_layer, args=(st.session_state.model, layer, placeholders, layer_files[layer]))