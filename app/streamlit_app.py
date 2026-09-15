from pathlib import Path
import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

C = pd.read_csv(ROOT / "data/processed/investigation_cases.csv")
T = pd.read_csv(ROOT / "data/processed/case_transactions.csv")
S = pd.read_csv(ROOT / "data/processed/sar_decisions.csv")

C["created_date"] = pd.to_datetime(C["created_date"], errors="coerce")
T["transaction_date"] = pd.to_datetime(T["transaction_date"], errors="coerce")
if "filing_date" in S.columns:
    S["filing_date"] = pd.to_datetime(S["filing_date"], errors="coerce")

st.set_page_config(
    page_title="AML Case Investigation & SAR Decision Analytics",
    page_icon="🔎",
    layout="wide",
)

st.title("AML Case Investigation & SAR Decision Analytics")
st.caption("Investigate. Analyze. Decide. | From alerts to defensible outcomes.")
st.caption("Synthetic Financial Crime Analytics portfolio project")

# -------------------------
# Dashboard-aligned filters
# -------------------------
min_date = C["created_date"].min().date()
max_date = C["created_date"].max().date()

with st.sidebar:
    st.header("Portfolio Filters")

    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    case_type = st.selectbox(
        "Case Type", ["All"] + sorted(C["case_type"].dropna().unique().tolist())
    )

    risk_rating = st.selectbox(
        "Risk Rating", ["All"] + sorted(C["priority"].dropna().unique().tolist())
    )

    customer_segment = st.selectbox(
        "Customer Segment", ["All"] + sorted(C["customer_type"].dropna().unique().tolist())
    )

F = C.copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

F = F[
    (F["created_date"].dt.date >= start_date)
    & (F["created_date"].dt.date <= end_date)
]

if case_type != "All":
    F = F[F["case_type"].eq(case_type)]
if risk_rating != "All":
    F = F[F["priority"].eq(risk_rating)]
if customer_segment != "All":
    F = F[F["customer_type"].eq(customer_segment)]

case_ids = set(F["case_id"])
TF = T[T["case_id"].isin(case_ids)].copy()
SF = S[S["case_id"].isin(case_ids)].copy()

# -------------------------
# KPI calculations
# -------------------------
case_count = len(F)
high_critical = int(F["priority"].isin(["High", "Critical"]).sum())
sar_decisions = int(F["sar_flag"].sum()) if case_count else 0
sar_filed = int(F["disposition"].eq("SAR Filed").sum())
additional_review = int(F["disposition"].eq("Escalate for Additional Review").sum())
reviewed_amount = float(F["reviewed_amount"].sum()) if case_count else 0.0

high_pct = high_critical / case_count * 100 if case_count else 0
decision_pct = sar_decisions / case_count * 100 if case_count else 0
filed_pct = sar_filed / case_count * 100 if case_count else 0
review_pct = additional_review / case_count * 100 if case_count else 0

st.divider()

# -------------------------
# KPI scorecard
# -------------------------
st.markdown("### Portfolio Summary")
st.write(
    f"The current filtered portfolio contains **{case_count:,} investigation cases** "
    f"covering **${reviewed_amount/1e6:.1f}M in reviewed activity**. "
    f"Of these cases, **{high_critical:,} ({high_pct:.1f}%)** are rated High or Critical, "
    f"while **{sar_decisions:,} ({decision_pct:.1f}%)** reached a SAR decision. "
    "The KPI scorecard below provides a quick view of investigation volume, risk exposure, "
    "SAR outcomes, escalation activity, and the total amount reviewed."
)

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Cases", f"{case_count:,}")
k2.metric("High / Critical", f"{high_critical:,}", f"{high_pct:.1f}%")
k3.metric("SAR Decisions", f"{sar_decisions:,}", f"{decision_pct:.1f}%")
k4.metric("SAR Filed", f"{sar_filed:,}", f"{filed_pct:.1f}%")
k5.metric("Additional Review", f"{additional_review:,}", f"{review_pct:.1f}%")
k6.metric("Reviewed Amount", f"${reviewed_amount/1e6:.1f}M")

if case_count == 0:
    st.warning("No cases match the selected filters. Adjust the portfolio filters.")
    st.stop()

# -------------------------
# Tabs
# -------------------------
tabs = st.tabs([
    "Executive Overview",
    "Case Queue",
    "Case 360",
    "Transaction Lookback",
    "SAR Decisions",
    "Tableau Gallery",
])

with tabs[0]:
    st.subheader("Executive Overview")
    st.caption("Interactive portfolio analytics aligned to the final Tableau executive dashboard.")

    monthly = (
        F.assign(month=F["created_date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month")
        .agg(
            Cases=("case_id", "count"),
            SAR_Decisions=("sar_flag", "sum"),
            SAR_Filed=("disposition", lambda x: x.eq("SAR Filed").sum()),
        )
    )
    st.markdown("#### Cases & SAR Decisions Trend")
    st.line_chart(monthly)

    a, b = st.columns(2)
    with a:
        st.markdown("#### Case Disposition")
        disposition = F["disposition"].value_counts().rename("Cases")
        st.bar_chart(disposition)
    with b:
        st.markdown("#### Top 5 Investigation Red Flags")
        red_flags = F["primary_red_flag"].value_counts().head(5).rename("Cases")
        st.bar_chart(red_flags)

    a, b = st.columns(2)
    with a:
        st.markdown("#### Case Aging Distribution")
        aging = pd.cut(
            F["case_age_days"],
            bins=[-1, 7, 30, 60, float("inf")],
            labels=["0–7", "8–30", "31–60", "60+"],
        ).value_counts(sort=False).rename("Cases")
        st.bar_chart(aging)

    with b:
        st.markdown("#### SAR Decision Rate by Case Type")
        rate = (
            F.groupby("case_type")["sar_flag"]
            .mean()
            .mul(100)
            .sort_values(ascending=False)
            .rename("SAR Decision Rate (%)")
        )
        st.bar_chart(rate)

    st.markdown("#### Reviewed Amount vs Case Risk")
    scatter_data = F[["reviewed_amount", "case_risk_score"]].rename(
        columns={"reviewed_amount": "Reviewed Amount", "case_risk_score": "Case Risk Score"}
    )
    st.scatter_chart(scatter_data, x="Reviewed Amount", y="Case Risk Score")

    st.markdown("#### Key Insights & Recommended Actions")
    filing_rate = sar_filed / sar_decisions * 100 if sar_decisions else 0
    top_flags = F["primary_red_flag"].value_counts().head(2).index.tolist()
    flag_text = " and ".join(top_flags) if top_flags else "No red flags"

    st.write(
        f"• **{high_pct:.1f}% ({high_critical:,})** of cases are High/Critical; prioritize elevated-risk investigations."
    )
    st.write(
        f"• **{sar_filed:,} SARs** were filed from **{sar_decisions:,} SAR decisions** "
        f"(**{filing_rate:.1f}% filing rate among SAR decisions**)."
    )
    st.write(
        f"• **{review_pct:.1f}% ({additional_review:,})** of cases were escalated for additional review."
    )
    st.write(f"• **{flag_text}** are the leading red flags in the current filtered population.")
    st.write("• Focus on timely investigation, complete documentation, and clear decision rationale.")

with tabs[1]:
    st.subheader("Case Queue")
    st.caption("Prioritized investigation queue sorted by case risk score and case age.")
    queue_cols = [
        "case_id", "customer_id", "case_type", "created_date", "priority",
        "case_risk_score", "case_age_days", "primary_red_flag",
        "reviewed_amount", "disposition"
    ]
    st.dataframe(
        F.sort_values(["case_risk_score", "case_age_days"], ascending=False)[queue_cols],
        use_container_width=True,
        hide_index=True,
    )

with tabs[2]:
    st.subheader("Case 360")
    available_cases = F["case_id"].tolist()
    selected_case = st.selectbox("Select Investigation Case", available_cases, key="case360")
    r = F[F["case_id"].eq(selected_case)].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Case", r["case_id"])
    c2.metric("Risk Rating", r["priority"])
    c3.metric("Case Risk Score", f"{r['case_risk_score']}")
    c4.metric("Disposition", r["disposition"])

    st.markdown("#### Customer / KYC Context")
    customer_view = pd.DataFrame([{
        "Customer ID": r["customer_id"],
        "Customer": r["customer_name"],
        "Segment": r["customer_type"],
        "Country": r["country"],
        "KYC Risk": r["kyc_risk"],
        "PEP Flag": "Yes" if r["pep_flag"] == 1 else "No",
        "Expected Monthly Volume": f"${r['expected_monthly_volume']:,.0f}",
    }])
    st.dataframe(customer_view, use_container_width=True, hide_index=True)

    st.markdown("#### Investigation Context")
    i1, i2, i3, i4 = st.columns(4)
    i1.metric("Primary Red Flag", r["primary_red_flag"])
    i2.metric("Red Flag Count", f"{r['red_flag_count']}")
    i3.metric("Transactions Reviewed", f"{r['reviewed_txn_count']:,}")
    i4.metric("Reviewed Amount", f"${r['reviewed_amount']:,.0f}")

    st.markdown("#### Investigation Summary")
    st.info(str(r["investigation_summary"]))

    st.markdown("#### Decision Rationale")
    st.write(str(r["sar_decision_reason"]))

    st.markdown("#### Final Decision")
    if r["disposition"] == "SAR Filed":
        st.error("SAR FILED — the synthetic investigation record supports a filing outcome.")
    elif r["disposition"] == "SAR Recommended":
        st.warning("SAR RECOMMENDED — the case reached a SAR recommendation outcome.")
    elif r["disposition"] == "Escalate for Additional Review":
        st.warning("ADDITIONAL REVIEW REQUIRED — further investigation is required before closure.")
    else:
        st.success("CLOSE — NO SUSPICION — the case did not require SAR escalation at this stage.")

with tabs[3]:
    st.subheader("Transaction Lookback")
    lookback_case = st.selectbox(
        "Select Case for Transaction Lookback",
        F["case_id"].tolist(),
        key="lookback",
    )
    tx = TF[TF["case_id"].eq(lookback_case)].sort_values("transaction_date", ascending=False)

    t1, t2, t3 = st.columns(3)
    t1.metric("Transactions Reviewed", f"{len(tx):,}")
    t2.metric("Transaction Value", f"${tx['amount'].sum():,.0f}")
    t3.metric("High-Risk Geography Txns", f"{int(tx['high_risk_geo_flag'].sum()):,}")

    st.dataframe(tx, use_container_width=True, hide_index=True)

    if len(tx):
        st.markdown("#### Activity by Channel")
        st.bar_chart(tx.groupby("channel")["amount"].sum().sort_values(ascending=False))

with tabs[4]:
    st.subheader("SAR Decisions")
    st.caption("SAR decision and filing records associated with the filtered case population.")

    d1, d2, d3 = st.columns(3)
    d1.metric("SAR Decisions", f"{sar_decisions:,}")
    d2.metric("SAR Filed", f"{sar_filed:,}")
    d3.metric(
        "Filing Rate",
        f"{(sar_filed / sar_decisions * 100 if sar_decisions else 0):.1f}%"
    )

    if len(SF):
        sort_cols = [c for c in ["case_risk_score", "filing_date"] if c in SF.columns]
        st.dataframe(
            SF.sort_values(sort_cols, ascending=False) if sort_cols else SF,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No SAR decision records match the current filters.")

with tabs[5]:
    st.subheader("Tableau Gallery")
    st.caption("Final executive dashboard aligned with the processed project data and verified KPI results.")

    executive_img = ROOT / "images/02_executive_dashboard.png"
    if executive_img.exists():
        st.image(
            str(executive_img),
            caption="AML Case Investigation & SAR Decision Analytics — Executive Dashboard",
            use_container_width=True,
        )
    else:
        st.info("Add `02_executive_dashboard.png` to the `images/` folder.")

st.divider()
st.caption(
    "Synthetic educational portfolio project. No real customer, bank, investigation case, or SAR data is included."
)
