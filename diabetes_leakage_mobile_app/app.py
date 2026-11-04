from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='Diabetes Leakage Explorer',
    page_icon='🔬',
    layout='wide'
)

ROOT = Path(__file__).parent / 'diabetes_results'

@st.cache_data
def load(name):
    return pd.read_csv(ROOT / name)

st.title('🔬 Diabetes Leakage Explorer')
st.caption('Mobile-responsive duplicate-profile leakage dashboard')

audit = load('table_1_dataset_audit.csv').iloc[0]

a, b = st.columns(2)
a.metric('Rows', int(audit['Rows']))
b.metric('Exact profiles', int(audit['Distinct exact profiles']))

t1, t2, t3 = st.tabs(['Benchmark', 'Exposure', 'Calibration'])

with t1:
    d = load('table_3_naive_vs_grouped.csv')
    metric = st.selectbox('Metric', d['Metric'].unique())
    q = d[d['Metric'].eq(metric)]

    p = q.melt(
        id_vars='Model',
        value_vars=['Naive mean', 'Grouped mean'],
        var_name='Validation',
        value_name='Score',
    )

    st.plotly_chart(
        px.bar(
            p,
            x='Model',
            y='Score',
            color='Validation',
            barmode='group'
        ),
        use_container_width=True,
    )

    st.dataframe(q, use_container_width=True, hide_index=True)

with t2:
    d = load('table_7_dose_response.csv')
    q = d[d['Subgroup'].eq('Eligible profiles')]

    st.plotly_chart(
        px.line(
            q,
            x='Actual exposure',
            y='accuracy_change',
            color='Model',
            markers=True
        ),
        use_container_width=True,
    )

with t3:
    st.dataframe(
        load('table_5_calibration.csv'),
        use_container_width=True,
        hide_index=True,
    )

    st.dataframe(
        load('table_6_prior_shift.csv'),
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    'Research use only: grouped CV tests unseen exact profiles within this dataset, '
    'not external clinical validity.'
)
