from pathlib import Path
import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

C = pd.read_csv(ROOT / "data/processed/investigation_cases.csv")
T = pd.read_csv(ROOT / "data/processed/case_transactions.csv")
S = pd.read_csv(ROOT / "data/processed/sar_decisions.csv")

st.set_page_config(
    page_title="AML Case Investigation & SAR Analytics",
    layout="wide"
)

st.title("AML Case Investigation & SAR Decision Analytics")
st.caption(
    "Synthetic portfolio project | A simple investigation view showing what happened, "
    "why it matters, and the final AML decision."
)

with st.sidebar:
    st.header("Filters")
    case_types = st.multiselect(
        "Case Type",
        sorted(C.case_type.dropna().unique()),
        default=sorted(C.case_type.dropna().unique())
    )
    priorities = st.multiselect(
        "Priority",
        sorted(C.priority.dropna().unique()),
        default=sorted(C.priority.dropna().unique())
    )
    dispositions = st.multiselect(
        "Disposition",
        sorted(C.disposition.dropna().unique()),
        default=sorted(C.disposition.dropna().unique())
    )

F = C[
    C.case_type.isin(case_types)
    & C.priority.isin(priorities)
    & C.disposition.isin(dispositions)
].copy()

# -------------------------
# Portfolio KPIs
# -------------------------
case_count = len(F)
high_critical = F.priority.isin(["High", "Critical"]).sum() if case_count else 0
sar_decisions = int(F.sar_flag.sum()) if case_count and "sar_flag" in F.columns else 0
sar_filed = (F.disposition == "SAR Filed").sum() if case_count else 0
additional_review = (
    (F.disposition == "Escalate for Additional Review").sum() if case_count else 0
)
reviewed_amount = F.reviewed_amount.sum() if case_count and "reviewed_amount" in F.columns else 0

# -------------------------
# Executive Summary
# -------------------------
st.subheader("Executive Summary")

if case_count == 0:
    st.warning("No cases match the selected filters.")
else:
    high_risk_pct = high_critical / case_count * 100
    sar_rate = sar_filed / case_count * 100
    review_rate = additional_review / case_count * 100

    if sar_filed > 0:
        overall_status = "Suspicious Activity Identified"
        summary_message = (
            "The selected portfolio contains cases that resulted in SAR filings. "
            "These cases should be treated as the highest-priority outcomes in the investigation population."
        )
    elif additional_review > 0:
        overall_status = "Further Review Required"
        summary_message = (
            "No SAR filing is shown in the selected portfolio, but some cases require additional review "
            "before a final disposition can be reached."
        )
    else:
        overall_status = "No Immediate Escalation"
        summary_message = (
            "The selected portfolio does not currently show SAR filings or additional-review dispositions."
        )

    a, b, c = st.columns([1.2, 1.2, 2.6])
    with a:
        st.metric("Portfolio Status", overall_status)
    with b:
        st.metric("High/Critical Cases", f"{high_critical:,}")
    with c:
        st.info(summary_message)

    st.markdown(
        f"""
        The current view contains **{case_count:,} cases**.
        **{high_risk_pct:.1f}%** are High or Critical priority.
        **{sar_filed:,} case(s)** resulted in SAR filing and **{additional_review:,} case(s)**
        were escalated for additional review. The total amount reviewed is approximately
        **${reviewed_amount/1e6:.1f}M**.
        """
    )

    st.markdown("#### What this means")
    insights = []

    if high_risk_pct >= 40:
        insights.append(
            "A large share of the selected population is High/Critical priority, so investigator attention should focus there first."
        )
    else:
        insights.append(
            "The selected population has a manageable concentration of High/Critical cases."
        )

    if sar_filed > 0:
        insights.append(
            f"{sar_filed} case(s) resulted in a SAR filing, indicating suspicious activity was supported by the investigation."
        )

    if additional_review > 0:
        insights.append(
            f"{additional_review} case(s) still require additional review before the final AML decision is complete."
        )

    for text in insights:
        st.write(f"• {text}")

st.divider()

# -------------------------
# KPI Scorecard
# -------------------------
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Cases", f"{case_count:,}")
c2.metric("High/Critical", f"{high_critical:,}")
c3.metric("SAR Decisions", f"{sar_decisions:,}")
c4.metric("SAR Filed", f"{sar_filed:,}")
c5.metric("Additional Review", f"{additional_review:,}")
c6.metric("Reviewed Amount", f"${reviewed_amount/1e6:.1f}M")

# -------------------------
# Case-level explanation
# -------------------------
st.subheader("Case Investigation Summary")

available_cases = F.case_id.tolist() if len(F) else C.case_id.tolist()
selected_case = st.selectbox("Select a case to understand the investigation", available_cases)

case_row = C[C.case_id.eq(selected_case)]

if len(case_row):
    r = case_row.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Case", str(r.get("case_id", "")))
    with col2:
        st.metric("Priority", str(r.get("priority", "N/A")))
    with col3:
        st.metric("Risk Score", f"{r.get('case_risk_score', 'N/A')}")
    with col4:
        st.metric("Disposition", str(r.get("disposition", "N/A")))

    st.markdown("#### Investigation Summary")
    investigation_summary = r.get("investigation_summary", "")
    if pd.notna(investigation_summary) and str(investigation_summary).strip():
        st.info(str(investigation_summary))
    else:
        st.info("No narrative investigation summary is available for this case.")

    st.markdown("#### Why this case matters")

    red_flag = r.get("primary_red_flag", "Not available")
    reviewed_amt = r.get("reviewed_amount", None)
    priority = r.get("priority", "N/A")
    disposition = r.get("disposition", "N/A")
    sar_flag = r.get("sar_flag", 0)

    why_text = f"The primary red flag is **{red_flag}**. "
    if pd.notna(reviewed_amt):
        why_text += f"The investigation reviewed approximately **${float(reviewed_amt):,.0f}** in activity. "
    why_text += f"The case was assigned **{priority}** priority."

    st.write(why_text)

    st.markdown("#### Final Decision")

    if disposition == "SAR Filed" or sar_flag == 1:
        st.error(
            "Final decision: **SAR FILED**. The investigation identified sufficient suspicious activity "
            "to support escalation and regulatory reporting."
        )
    elif disposition == "Escalate for Additional Review":
        st.warning(
            "Final decision: **ADDITIONAL REVIEW REQUIRED**. The available information raises concerns, "
            "but further investigation is needed before a final filing decision."
        )
    else:
        st.success(
            f"Final decision: **{disposition}**. Based on the available investigation record, "
            "the case did not require SAR filing at this stage."
        )

    # Optional SAR narrative / reason from sar_decisions dataset
    sar_record = S[S.case_id.eq(selected_case)] if "case_id" in S.columns else pd.DataFrame()
    if len(sar_record):
        sr = sar_record.iloc[0]
        narrative_cols = [
            "decision_reason",
            "sar_rationale",
            "sar_narrative",
            "filing_rationale",
            "decision_summary"
        ]
        narrative = None
        narrative_label = None

        for col in narrative_cols:
            if col in sar_record.columns and pd.notna(sr.get(col)) and str(sr.get(col)).strip():
                narrative = str(sr.get(col))
                narrative_label = col.replace("_", " ").title()
                break

        if narrative:
            st.markdown(f"#### {narrative_label}")
            st.write(narrative)

st.divider()

# -------------------------
# Detailed tabs
# -------------------------
tabs = st.tabs([
    "Case Queue",
    "Case 360",
    "Transaction Lookback",
    "SAR Decisions",
    "Portfolio Analytics",
    "Tableau Gallery"
])

with tabs[0]:
    st.subheader("Case Queue")
    st.caption(
        "Cases are sorted by risk and age so a reviewer can quickly identify which investigations deserve attention first."
    )
    st.dataframe(
        F.sort_values(["case_risk_score", "case_age_days"], ascending=False),
        use_container_width=True,
        hide_index=True
    )

with tabs[1]:
    st.subheader("Case 360")
    st.caption("Complete case-level details for the selected investigation.")
    st.dataframe(case_row, use_container_width=True, hide_index=True)

    if len(case_row):
        st.info(case_row.iloc[0].investigation_summary)

with tabs[2]:
    st.subheader("Transaction Lookback")
    st.caption(
        "Transaction history used to understand patterns, unusual behavior, and the activity supporting the investigation."
    )
    case_id2 = st.selectbox(
        "Select case for transaction lookback",
        available_cases,
        index=available_cases.index(selected_case) if selected_case in available_cases else 0,
        key="lookback_case"
    )

    tx = T[T.case_id.eq(case_id2)].sort_values("transaction_date", ascending=False)
    st.dataframe(tx, use_container_width=True, hide_index=True)

    if len(tx):
        st.markdown("##### Transaction Summary")
        amount_cols = ["amount", "transaction_amount", "txn_amount"]
        amount_col = next((c for c in amount_cols if c in tx.columns), None)

        t1, t2 = st.columns(2)
        with t1:
            st.metric("Transactions Reviewed", f"{len(tx):,}")
        with t2:
            if amount_col:
                st.metric("Transaction Value", f"${tx[amount_col].sum():,.0f}")
            else:
                st.metric("Transaction Value", "See transaction table")

with tabs[3]:
    st.subheader("SAR Decisions")
    st.caption(
        "Shows final filing decisions and supporting case information for regulatory-reporting outcomes."
    )
    sort_cols = [c for c in ["case_risk_score", "filing_date"] if c in S.columns]
    if sort_cols:
        st.dataframe(
            S.sort_values(sort_cols, ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.dataframe(S, use_container_width=True, hide_index=True)

with tabs[4]:
    st.subheader("Portfolio Analytics")
    a, b = st.columns(2)

    with a:
        st.markdown("##### Primary Red Flags")
        st.caption("Shows the most common reasons cases entered or progressed through investigation.")
        if len(F):
            st.bar_chart(F.primary_red_flag.value_counts())

    with b:
        st.markdown("##### Final Case Dispositions")
        st.caption("Shows how investigations ended across the selected case population.")
        if len(F):
            st.bar_chart(F.disposition.value_counts())

with tabs[5]:
    st.subheader("Tableau Gallery")
    st.caption(
        "Final Executive Dashboard aligned with the current processed datasets and verified KPI results."
    )

    executive_img = ROOT / "images/02_executive_dashboard.png"

    if executive_img.exists():
        st.markdown("##### Executive Dashboard")
        st.image(
            str(executive_img),
            caption="AML Case Investigation & SAR Decision Analytics — Final Executive Dashboard",
            use_container_width=True
        )
    else:
        st.info("Executive Dashboard image is not available. Add `02_executive_dashboard.png` to the `images/` folder.")

st.caption(
    "Synthetic educational portfolio project. No real bank, customer, case, or SAR data."
)
