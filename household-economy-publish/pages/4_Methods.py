from pathlib import Path
import streamlit as st
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
st.title('Evidence you can inspect')
st.caption('November 10, 2026 · Original downloads, transformations and model assumptions travel with this local bundle.')
for name in ['coverage','findings','methodology','limitations','model_tests']:
    with st.expander(name.replace('_',' ').title(),expanded=name=='coverage'):
        p=ROOT/'reports'/f'{name}.md'
        if p.exists(): st.markdown(p.read_text(encoding='utf-8'))
        else: st.info('See the project reports included in the bundle.')
p=ROOT/'reports/source_register.csv'
if p.exists():
    st.subheader('Source register')
    st.dataframe(pd.read_csv(p),hide_index=True,width='stretch')
    st.download_button('Download source register',p.read_bytes(),p.name,'text/csv')
