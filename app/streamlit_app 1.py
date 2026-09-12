from pathlib import Path
import streamlit as st
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
C=pd.read_csv(ROOT/"data/processed/investigation_cases.csv")
T=pd.read_csv(ROOT/"data/processed/case_transactions.csv")
S=pd.read_csv(ROOT/"data/processed/sar_decisions.csv")

st.set_page_config(page_title="AML Case Investigation & SAR Analytics",layout="wide")
st.title("AML Case Investigation & SAR Decision Analytics")
st.caption("Synthetic portfolio project | SQL + Python + Tableau + Streamlit")

with st.sidebar:
    st.header("Filters")
    case_types=st.multiselect("Case Type",sorted(C.case_type.unique()),default=sorted(C.case_type.unique()))
    priorities=st.multiselect("Priority",sorted(C.priority.unique()),default=sorted(C.priority.unique()))
    dispositions=st.multiselect("Disposition",sorted(C.disposition.unique()),default=sorted(C.disposition.unique()))

F=C[C.case_type.isin(case_types)&C.priority.isin(priorities)&C.disposition.isin(dispositions)]

c1,c2,c3,c4,c5,c6=st.columns(6)
c1.metric("Cases",f"{len(F):,}")
c2.metric("High/Critical",f"{F.priority.isin(['High','Critical']).sum():,}")
c3.metric("SAR Decisions",f"{F.sar_flag.sum():,}")
c4.metric("SAR Filed",f"{(F.disposition=='SAR Filed').sum():,}")
c5.metric("Additional Review",f"{(F.disposition=='Escalate for Additional Review').sum():,}")
c6.metric("Reviewed Amount",f"${F.reviewed_amount.sum()/1e6:.1f}M")

tabs=st.tabs(["Case Queue","Case 360","Transaction Lookback","SAR Decisions","Portfolio Analytics","Tableau Gallery"])

with tabs[0]:
    st.dataframe(F.sort_values(["case_risk_score","case_age_days"],ascending=False),use_container_width=True,hide_index=True)

with tabs[1]:
    case_id=st.selectbox("Select case",F.case_id.tolist() if len(F) else C.case_id.tolist())
    row=C[C.case_id.eq(case_id)]
    st.dataframe(row,use_container_width=True,hide_index=True)
    if len(row):
        st.info(row.iloc[0].investigation_summary)

with tabs[2]:
    case_id2=st.selectbox("Select case for lookback",F.case_id.tolist() if len(F) else C.case_id.tolist(),key="lookback_case")
    st.dataframe(T[T.case_id.eq(case_id2)].sort_values("transaction_date",ascending=False),use_container_width=True,hide_index=True)

with tabs[3]:
    st.dataframe(S.sort_values(["case_risk_score","filing_date"],ascending=False),use_container_width=True,hide_index=True)

with tabs[4]:
    a,b=st.columns(2)
    with a:
        st.bar_chart(F.primary_red_flag.value_counts())
    with b:
        st.bar_chart(F.disposition.value_counts())

with tabs[5]:
    st.subheader("KPI Scorecard")
    st.image(str(ROOT/"images/01_kpi_scorecard.png"),use_container_width=True)
    st.subheader("Executive Dashboard")
    st.image(str(ROOT/"images/02_executive_dashboard.png"),use_container_width=True)

st.caption("Synthetic educational portfolio project. No real bank, customer, case, or SAR data.")
