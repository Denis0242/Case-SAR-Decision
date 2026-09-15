from pathlib import Path
import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "customer_risk_analytics.csv"
CASES = ROOT / "data" / "raw" / "kyc_review_cases.csv"

st.set_page_config(
    page_title="Financial Crime Customer Risk & KYC/EDD Analytics",
    layout="wide"
)

st.title("Financial Crime Customer Risk & KYC/EDD Analytics")
st.caption(
    "Synthetic portfolio project | A simple view of customer risk, KYC completeness, "
    "EDD requirements, sanctions/PEP exposure, and recommended review actions."
)

df = pd.read_csv(DATA)
cases = pd.read_csv(CASES)

with st.sidebar:
    st.header("Filters")
    risk_filter = st.multiselect(
        "Risk level",
        sorted(df["risk_level"].dropna().unique()),
        default=sorted(df["risk_level"].dropna().unique())
    )
    type_filter = st.multiselect(
        "Customer type",
        sorted(df["customer_type"].dropna().unique()),
        default=sorted(df["customer_type"].dropna().unique())
    )
    country_filter = st.multiselect(
        "Country",
        sorted(df["country"].dropna().unique()),
        default=sorted(df["country"].dropna().unique())
    )

f = df[
    df["risk_level"].isin(risk_filter)
    & df["customer_type"].isin(type_filter)
    & df["country"].isin(country_filter)
].copy()

# -------------------------
# KPI calculations
# -------------------------
customers = len(f)
high_critical = f["risk_level"].isin(["High", "Critical"]).sum() if customers else 0
edd_required = int(f["edd_required"].sum()) if customers else 0
kyc_complete = int((f["kyc_complete_pct"] == 100).sum()) if customers else 0
pep_count = int(f["pep_flag"].sum()) if customers else 0
sanctions_hits = int(f["sanctions_hit"].sum()) if customers else 0
adverse_media = int(f["adverse_media_flag"].sum()) if customers and "adverse_media_flag" in f.columns else 0
incomplete_kyc = int((f["kyc_complete_pct"] < 100).sum()) if customers else 0

high_critical_pct = high_critical / customers * 100 if customers else 0.0
edd_pct = edd_required / customers * 100 if customers else 0.0
kyc_complete_pct = kyc_complete / customers * 100 if customers else 0.0

# -------------------------
# Portfolio decision logic
# -------------------------
def get_portfolio_status():
    signals = 0
    if high_critical_pct >= 25:
        signals += 1
    if edd_pct >= 20:
        signals += 1
    if sanctions_hits > 0:
        signals += 1
    if incomplete_kyc > 0:
        signals += 1

    if signals >= 3:
        return (
            "Enhanced Review Required",
            "The selected portfolio shows several KYC/EDD risk indicators that require prioritized review."
        )
    elif signals >= 1:
        return (
            "Targeted Review Recommended",
            "Some customers require additional KYC or EDD attention, while the broader portfolio remains manageable."
        )
    else:
        return (
            "Generally Stable",
            "The selected portfolio shows strong KYC completion and limited elevated-risk indicators."
        )

portfolio_status, portfolio_message = get_portfolio_status()

# -------------------------
# Executive summary
# -------------------------
st.subheader("Executive Summary")

if customers == 0:
    st.warning("No customers match the selected filters.")
else:
    s1, s2, s3 = st.columns([1.3, 1.0, 2.7])

    with s1:
        st.metric("Portfolio Status", portfolio_status)

    with s2:
        st.metric("Customers Requiring EDD", f"{edd_required:,}")

    with s3:
        st.info(portfolio_message)

    st.markdown(
        f"""
        The selected portfolio contains **{customers:,} customers**.
        **{high_critical_pct:.1f}%** are High or Critical risk, **{edd_required:,} customer(s)**
        require Enhanced Due Diligence, and **{kyc_complete_pct:.1f}%** have fully completed KYC.
        There are **{pep_count:,} PEP customer(s)**, **{sanctions_hits:,} sanctions hit(s)**,
        and **{adverse_media:,} adverse-media flag(s)** in the selected population.
        """
    )

    st.markdown("#### What this means")

    insights = []

    if incomplete_kyc > 0:
        insights.append(
            f"{incomplete_kyc} customer(s) have incomplete KYC records and should be remediated before normal onboarding or continuation decisions."
        )
    else:
        insights.append(
            "All selected customers have complete KYC records."
        )

    if edd_required > 0:
        insights.append(
            f"{edd_required} customer(s) require EDD because their risk profile exceeds standard due-diligence requirements."
        )

    if sanctions_hits > 0:
        insights.append(
            f"{sanctions_hits} sanctions hit(s) require validation to determine whether they are true matches, false positives, or escalation cases."
        )

    if pep_count > 0:
        insights.append(
            f"{pep_count} PEP customer(s) require enhanced scrutiny and appropriate approval/monitoring."
        )

    for item in insights:
        st.write(f"• {item}")

    st.markdown("#### Final Portfolio Decision")

    if portfolio_status == "Enhanced Review Required":
        st.error(
            "Prioritize High/Critical-risk customers, incomplete KYC records, sanctions hits, and EDD-required customers. "
            "Do not treat the portfolio as fully cleared until these higher-risk items are resolved."
        )
    elif portfolio_status == "Targeted Review Recommended":
        st.warning(
            "Continue routine onboarding/monitoring for lower-risk customers, but complete targeted KYC remediation "
            "and EDD review for the flagged population."
        )
    else:
        st.success(
            "Maintain normal KYC monitoring. No broad portfolio-level escalation is indicated by the selected data."
        )

st.divider()

# -------------------------
# KPI scorecard
# -------------------------
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Customers", f"{customers:,}")
k2.metric("High/Critical", f"{high_critical:,}")
k3.metric("EDD Required", f"{edd_required:,}")
k4.metric("KYC Complete", f"{kyc_complete:,}")
k5.metric("PEP", f"{pep_count:,}")
k6.metric("Sanctions Hits", f"{sanctions_hits:,}")

# -------------------------
# Customer-level explanation
# -------------------------
st.subheader("Customer KYC / EDD Decision Summary")

available_customers = (
    f.sort_values("risk_score", ascending=False)["customer_id"].tolist()
    if len(f)
    else df.sort_values("risk_score", ascending=False)["customer_id"].tolist()
)

selected_customer = st.selectbox(
    "Select a customer to understand the decision",
    available_customers
)

customer_row = df[df["customer_id"] == selected_customer]

if len(customer_row):
    row = customer_row.iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Risk Score", int(row.risk_score))
    c2.metric("Risk Level", row.risk_level)
    c3.metric("KYC Complete", f"{row.kyc_complete_pct:.0f}%")
    c4.metric("EDD Required", "Yes" if row.edd_required else "No")

    st.markdown("#### Why this customer matters")

    reasons = [
        f"The customer is rated **{row.risk_level} risk** with a risk score of **{int(row.risk_score)}**.",
        f"The main risk driver is **{row.primary_risk_driver}**.",
        f"KYC completion is **{row.kyc_complete_pct:.0f}%**."
    ]

    if row.edd_required:
        reasons.append("Enhanced Due Diligence is required.")
    if row.pep_flag:
        reasons.append("The customer is flagged as a PEP.")
    if row.sanctions_hit:
        reasons.append("The customer has a sanctions-screening hit requiring review.")
    if row.adverse_media_flag:
        reasons.append("The customer has an adverse-media flag.")
    if not row.ubo_complete:
        reasons.append("Beneficial ownership information is incomplete.")
    if not row.source_of_wealth_verified:
        reasons.append("Source of wealth has not been fully verified.")

    st.write(" ".join(reasons))

    st.markdown("#### Control Review")

    control_df = pd.DataFrame({
        "Control": [
            "ID verified",
            "Address verified",
            "Tax verified",
            "UBO complete",
            "Source of wealth verified",
            "PEP",
            "Sanctions hit",
            "Adverse media"
        ],
        "Result": [
            "Complete" if row.id_verified else "Missing / Review",
            "Complete" if row.address_verified else "Missing / Review",
            "Complete" if row.tax_verified else "Missing / Review",
            "Complete" if row.ubo_complete else "Missing / Review",
            "Complete" if row.source_of_wealth_verified else "Missing / Review",
            "Flagged" if row.pep_flag else "No flag",
            "Flagged" if row.sanctions_hit else "No hit",
            "Flagged" if row.adverse_media_flag else "No flag"
        ]
    })

    st.dataframe(control_df, use_container_width=True, hide_index=True)

    st.markdown("#### Final Customer Decision")

    if row.sanctions_hit:
        st.error(
            "Decision: **ESCALATE SANCTIONS REVIEW**. The sanctions hit must be resolved before a normal onboarding or continuation decision."
        )
    elif row.risk_level in ["High", "Critical"] and row.edd_required:
        st.error(
            "Decision: **EDD REQUIRED**. Complete enhanced due diligence, verify outstanding ownership/source-of-wealth information, "
            "and obtain appropriate approval before final clearance."
        )
    elif row.kyc_complete_pct < 100:
        st.warning(
            "Decision: **KYC REMEDIATION REQUIRED**. Missing customer information or control evidence must be completed before final clearance."
        )
    elif row.pep_flag or row.adverse_media_flag:
        st.warning(
            "Decision: **ENHANCED REVIEW**. The customer requires additional review because of PEP or adverse-media exposure."
        )
    else:
        st.success(
            "Decision: **STANDARD KYC APPROVAL / ROUTINE MONITORING**. The current record does not show a major unresolved KYC/EDD issue."
        )

st.divider()

# -------------------------
# Detailed tabs
# -------------------------
tabs = st.tabs([
    "Customer Risk Queue",
    "Customer 360",
    "KYC/EDD Cases",
    "Portfolio Analytics",
    "Tableau Gallery"
])

with tabs[0]:
    st.subheader("Risk-Ranked Customer Queue")
    st.caption(
        "Customers are ranked by risk score so reviewers can quickly identify the population requiring the most attention."
    )

    queue = f[
        [
            "customer_id",
            "customer_type",
            "country",
            "risk_score",
            "risk_level",
            "kyc_complete_pct",
            "edd_required",
            "primary_risk_driver",
            "customer_status"
        ]
    ].sort_values(
        ["risk_score", "kyc_complete_pct"],
        ascending=[False, True]
    )

    st.dataframe(
        queue,
        use_container_width=True,
        hide_index=True
    )

with tabs[1]:
    st.subheader("Customer 360")
    st.caption(
        "Detailed customer profile showing risk, KYC completion, EDD requirements, and key control flags."
    )

    st.dataframe(
        customer_row,
        use_container_width=True,
        hide_index=True
    )

with tabs[2]:
    st.subheader("KYC / EDD Review Cases")
    st.caption(
        "Open or review cases are sorted by risk and age so teams can focus on older and higher-risk remediation work first."
    )

    st.dataframe(
        cases.sort_values(
            ["risk_score", "age_days"],
            ascending=[False, False]
        ),
        use_container_width=True,
        hide_index=True
    )

with tabs[3]:
    st.subheader("Portfolio Analytics")

    a, b = st.columns(2)

    with a:
        st.markdown("##### Risk-Level Distribution")
        st.caption("Shows how customers are distributed across risk categories.")
        st.bar_chart(f["risk_level"].value_counts())

    with b:
        st.markdown("##### Main EDD Drivers")
        st.caption("Shows the most common reasons customers require Enhanced Due Diligence.")
        st.bar_chart(
            f[f.edd_required == 1]["primary_risk_driver"].value_counts()
        )

with tabs[4]:
    st.subheader("Tableau Analytics Gallery")
    st.caption(
        "Static Tableau views for quick recruiter and hiring-manager review."
    )

    images = [
        ("02_executive_dashboard.png", "Executive Dashboard"),
    ]

    for filename, caption in images:
        img = ROOT / "images" / filename
        if img.exists():
            st.image(
                str(img),
                caption=caption,
                use_container_width=True
            )

st.caption(
    "Synthetic educational portfolio project. No real customer or bank data."
)
