import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==============================================================================
# 1. PREMIUM REGISTRATION AND DEPOSITS COMMAND CENTER CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Registration and Deposits Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Registration and Deposits Dashboard")
st.markdown("### Strategic Year, Quarter, and Monthly Business Performance Matrix")
st.markdown("---")

# Initialize global tracking memory cache if it doesn't exist
if "matrix_overrides" not in st.session_state:
    st.session_state.matrix_overrides = {}

# ==============================================================================
# 2. HIGH-FIDELITY AUTOMATED DATA INGESTION PIPELINE
# ==============================================================================
@st.cache_data(ttl=60) # Refreshes automatically every minute or on system state rerun
def load_source_files(target_year):
    m_order = ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]
    
    # Establish structural timeline matrix grid
    df_matrix = pd.DataFrame({"Year": [target_year]*12, "Month": m_order})
    
    # 1. Pull Registrations
    try:
        reg_df = pd.read_csv("Registrations_Cleaned.csv")
        reg_df.columns = [c.strip() for c in reg_df.columns]
        df_matrix = pd.merge(df_matrix, reg_df[reg_df["Year"] == target_year][["Month", "Registration"]], on="Month", how="left")
    except Exception:
        df_matrix["Registration"] = pd.NA

    # 2. Pull First Time Depositors
    try:
        ftd_df = pd.read_csv("FTDS_Cleaned.csv")
        ftd_df.columns = [c.strip() for c in ftd_df.columns]
        df_matrix = pd.merge(df_matrix, ftd_df[ftd_df["Year"] == target_year][["Month", "FTDs"]], on="Month", how="left")
    except Exception:
        df_matrix["FTDs"] = pd.NA

    # 3. Pull Actual Cash Deposits
    try:
        dep_df = pd.read_csv("Deposits_Cleaned.csv")
        dep_df.columns = [c.strip() for c in dep_df.columns]
        df_matrix = pd.merge(df_matrix, dep_df[dep_df["Year"] == target_year][["Month", "Deposits"]], on="Month", how="left")
    except Exception:
        df_matrix["Deposits"] = pd.NA

    # 4. Pull Deposits Projections
    try:
        dep_p_df = pd.read_csv("Deposits_Projection_Cleaned.csv")
        dep_p_df.columns = [c.strip() for c in dep_p_df.columns]
        df_matrix = pd.merge(df_matrix, dep_p_df[dep_p_df["Year"] == target_year][["Month", "Deposits_Projection"]], on="Month", how="left")
    except Exception:
        df_matrix["Deposits_Projection"] = pd.NA

    # 5. Pull Actual Gross Gaming Revenue (GGR)
    try:
        ggr_df = pd.read_csv("GGR_Cleaned.csv")
        ggr_df.columns = [c.strip() for c in ggr_df.columns]
        df_matrix = pd.merge(df_matrix, ggr_df[ggr_df["Year"] == target_year][["Month", "GGR"]], on="Month", how="left")
    except Exception:
        df_matrix["GGR"] = pd.NA

    # 6. Pull GGR Projections
    try:
        ggr_p_df = pd.read_csv("GGR_Projection_Cleaned.csv")
        ggr_p_df.columns = [c.strip() for c in ggr_p_df.columns]
        df_matrix = pd.merge(df_matrix, ggr_p_df[ggr_p_df["Year"] == target_year][["Month", "GGR_Projection"]], on="Month", how="left")
    except Exception:
        df_matrix["GGR_Projection"] = pd.NA

    return df_matrix

# ==============================================================================
# 3. CHROMATIC CALENDAR SELECTOR
# ==============================================================================
review_year = st.radio(
    label="Select Timeline Operating Focus Year View:",
    options=[2024, 2025, 2026],
    index=2, # Initialized securely to the current year 2026
    horizontal=True
)

# Load underlying clean matrix data fields
active_frame = load_source_files(review_year)

# Apply dynamic state changes over baseline dataset rows securely
for override_key, values in st.session_state.matrix_overrides.items():
    yr, mnth = override_key.split("-")
    if int(yr) == review_year:
        mask = active_frame["Month"] == mnth
        if mask.any():
            for col, val in values.items():
                active_frame.loc[mask, col] = val

# ==============================================================================
# 4. CONDITIONAL CONTROL FLAGS (ELIMINATES DATA VOIDS PER USER INSTRUCTION)
# ==============================================================================
has_ggr_proj = review_year != 2024
has_dep_proj = review_year not in [2024, 2025]

# ==============================================================================
# 5. SIDEBAR PANEL: INTUITIVE DATA ENTRY & HISTORICAL OVERRIDES DESK
# ==============================================================================
st.sidebar.header("📝 Executive Editing Desk")
st.sidebar.markdown(f"Select a month below to view, insert, or override metrics for **{review_year}**.")

# Step A: Select month to manipulate
sel_month = st.sidebar.selectbox("Target Month to Edit:", options=active_frame["Month"].tolist(), index=5)

# Step B: Dynamically fetch current values from underlying sheet matrix row
row_match = active_frame[active_frame["Month"] == sel_month]

def extract_safe_val(df_row, column_name):
    val = df_row[column_name].iloc[0]
    if pd.isna(val) or val is None or val == "-":
        return 0
    return int(val)

c_reg = extract_safe_val(row_match, "Registration")
c_ftd = extract_safe_val(row_match, "FTDs")
c_ggr = extract_safe_val(row_match, "GGR")
c_ggr_p = extract_safe_val(row_match, "GGR_Projection")
c_dep = extract_safe_val(row_match, "Deposits")
c_dep_p = extract_safe_val(row_match, "Deposits_Projection")

# Step C: Load input metrics inside form with actual contextual metrics pre-loaded
with st.sidebar.form(key="dynamic_executive_form"):
    st.markdown(f"### Adjusting Figures for: **{sel_month} {review_year}**")
    
    val_regs = st.number_input("Registrations Count", min_value=0, value=c_reg, step=100)
    val_ftds = st.number_input("First Time Depositors (FTDs)", min_value=0, value=c_ftd, step=50)
    val_ggr = st.number_input("Actual GGR Volume (R)", value=c_ggr, step=50000)
    val_dep = st.number_input("Actual Deposits Volume (R)", value=c_dep, step=100000)
    
    # Display forecast target modifiers ONLY when chronologically applicable
    val_ggr_p = st.number_input("Projected GGR Target (R)", min_value=0, value=c_ggr_p, step=50000) if has_ggr_proj else 0
    val_dep_p = st.number_input("Projected Deposits Target (R)", min_value=0, value=c_dep_p, step=100000) if has_dep_proj else 0
    
    st.markdown(" ")
    apply_changes = st.form_submit_button("Update Data Matrix & Recalculate 🚀")

if apply_changes:
    composite_key = f"{review_year}-{sel_month}"
    st.session_state.matrix_overrides[composite_key] = {
        "Registration": val_regs, "FTDs": val_ftds,
        "GGR": val_ggr, "GGR_Projection": val_ggr_p,
        "Deposits": val_dep, "Deposits_Projection": val_dep_p
    }
    st.sidebar.success(f"Metrics recalculated successfully for {sel_month}!")
    st.rerun()

# ==============================================================================
# 6. HIGH-FIDELITY CHARTS & PERFORMANCE GRAPH OVERLAYS
# ==============================================================================
st.markdown(f"## 📊 Executive Visual Command Workspace: {review_year}")

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "💰 Gross Gaming Revenue (GGR)" + (" vs Projections Target Line" if has_ggr_proj else " Actual Performance"),
        "💳 Consolidated Cash Deposits" + (" vs Projections Target Line" if has_dep_proj else " Actual Performance"),
        "👥 User Acquisition Progress (Registrations Volume)",
        "🎯 First Time Depositors (FTDs) Monthly Distribution"
    ),
    vertical_spacing=0.22,
    horizontal_spacing=0.08
)

# ---- Plot 1: GGR Graph ----
fig.add_trace(go.Bar(x=active_frame["Month"], y=active_frame["GGR"], name="Actual GGR", marker_color="#2ecc71"), row=1, col=1)
if has_ggr_proj:
    fig.add_trace(go.Scatter(x=active_frame["Month"], y=active_frame["GGR_Projection"], name="Projected GGR", line=dict(color="#e74c3c", width=3, dash="dash"), mode="lines+markers"), row=1, col=1)

# ---- Plot 2: Deposits Graph ----
fig.add_trace(go.Bar(x=active_frame["Month"], y=active_frame["Deposits"], name="Actual Deposits", marker_color="#3498db"), row=1, col=2)
if has_dep_proj:
    fig.add_trace(go.Scatter(x=active_frame["Month"], y=active_frame["Deposits_Projection"], name="Projected Deposits", line=dict(color="#f39c12", width=3, dash="dash"), mode="lines+markers"), row=1, col=2)

# ---- Plot 3: Registrations Graph ----
fig.add_trace(go.Bar(x=active_frame["Month"], y=active_frame["Registration"], name="Registrations", marker_color="#9b59b6", texttemplate="%{y:,.0f}", textposition="outside"), row=2, col=1)

# ---- Plot 4: FTD Volume Timeline ----
fig.add_trace(go.Scatter(x=active_frame["Month"], y=active_frame["FTDs"], name="FTDs Count", mode="lines+markers+text", line=dict(color="#1abc9c", width=4), text=active_frame["FTDs"], textposition="top center"), row=2, col=2)

fig.update_layout(
    height=800,
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="right", x=1),
    hovermode="x unified"
)
fig.update_xaxes(type="category")
st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# 7. BUSINESS PERFORMANCE DATA BALANCING AUDIT LEDGER (AUTOMATED QUARTER BREAKS)
# ==============================================================================
st.markdown("---")
st.markdown(f"### 📋 Strategic Performance Ledger Audit Sheet ({review_year})")

q_map = {"January":"Q1", "February":"Q1", "March":"Q1", "April":"Q2", "May":"Q2", "June":"Q2", "July":"Q3", "August":"Q3", "September":"Q3", "October":"Q4", "November":"Q4", "December":"Q4"}
active_frame["Quarter"] = active_frame["Month"].map(q_map)

# Replace internal dataframe NaNs safely with 0 for clean formatting operations
clean_active = active_frame.copy()
for c in ["Registration", "FTDs", "Deposits", "Deposits_Projection", "GGR", "GGR_Projection"]:
    if c in clean_active.columns:
        clean_active[c] = pd.to_numeric(clean_active[c]).fillna(0).astype(int)

ledger_matrix = []
for q_id in ["Q1", "Q2", "Q3", "Q4"]:
    q_slice = clean_active[clean_active["Quarter"] == q_id]
    
    for _, r in q_slice.iterrows():
        # Mask future unreached months from displaying flat 0 strings cleanly
        is_blank_month = (review_year == 2026 and r['Month'] not in ["January","February","March","April"] and f"{review_year}-{r['Month']}" not in st.session_state.matrix_overrides)
        
        mask_reg = "-" if (is_blank_month and r['Registration'] == 0) else f"{r['Registration']:,}"
        mask_ftd = "-" if (is_blank_month and r['FTDs'] == 0) else f"{r['FTDs']:,}"
        mask_dep = "-" if (is_blank_month and r['Deposits'] == 0) else f"R {r['Deposits']:,}"
        mask_ggr = "-" if (is_blank_month and r['GGR'] == 0) else f"R {r['GGR']:,}"
        
        row_dict = {
            "Reporting Matrix Segment": r["Month"],
            "Registrations": mask_reg,
            "FTDs": mask_ftd,
            "Actual Deposits": mask_dep,
        }
        
        if has_dep_proj:
            row_dict["Deposits Target"] = f"R {r['Deposits_Projection']:,}"
            
        row_dict["Actual GGR"] = mask_ggr
        
        if has_ggr_proj:
            row_dict["Projected GGR Target"] = f"R {r['GGR_Projection']:,}"
            
        ledger_matrix.append(row_dict)
    
    # Calculate Quarter Milestone Summaries dynamically
    q_summary = {
        "Reporting Matrix Segment": f"== {q_id} PERFORMANCE TOTALS ==",
        "Registrations": f"{q_slice['Registration'].sum():,}",
        "FTDs": f"{q_slice['FTDs'].sum():,}",
        "Actual Deposits": f"R {q_slice['Deposits'].sum():,}",
    }
    if has_dep_proj:
        q_summary["Deposits Target"] = f"R {q_slice['Deposits_Projection'].sum():,}"
    q_summary["Actual GGR"] = f"R {q_slice['GGR'].sum():,}"
    if has_ggr_proj:
        q_summary["Projected GGR Target"] = f"R {q_slice['GGR_Projection'].sum():,}"
        
    ledger_matrix.append(q_summary)

# Calculate Final Grand Consolidated Annual Summary Total Row
annual_summary = {
    "Reporting Matrix Segment": f"🏆 GRAND CONSOLIDATED ANNUAL TOTAL SUMMARY ({review_year})",
    "Registrations": f"{clean_active['Registration'].sum():,}",
    "FTDs": f"{clean_active['FTDs'].sum():,}",
    "Actual Deposits": f"R {clean_active['Deposits'].sum():,}",
}
if has_dep_proj:
    annual_summary["Deposits Target"] = f"R {clean_active['Deposits_Projection'].sum():,}"
annual_summary["Actual GGR"] = f"R {clean_active['GGR'].sum():,}"
if has_ggr_proj:
    annual_summary["Projected GGR Target"] = f"R {clean_active['GGR_Projection'].sum():,}"

ledger_matrix.append(annual_summary)

# Display final formatted dataframe matrix table
st.table(pd.DataFrame(ledger_matrix).set_index("Reporting Matrix Segment"))

if st.session_state.matrix_overrides:
    if st.button("🗑️ Reset Workspace Overrides and Re-Sync Source Files"):
        st.session_state.matrix_overrides = {}
        st.rerun()