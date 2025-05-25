# import streamlit as st
# import pandas as pd
# import os
# import subprocess

# EXPLANATIONS_FILE = "top3_gpt_explanations.csv"
# FEEDBACK_FILE = "feedback_log.csv"

# df = pd.read_csv(EXPLANATIONS_FILE)

# # Appraisal Selection 
# order_ids = sorted(df["orderID"].unique())
# selected_order = st.selectbox("Select an Appraisal (orderID)", order_ids)

# appraisal_df = df[df["orderID"] == selected_order].sort_values("rank")

# st.title("🏠 Property Comparison Feedback")
# st.subheader(f"Subject Property: {appraisal_df['subject_address'].iloc[0]}")
# st.markdown("---")

# feedback_records = []

# def format_int(val):
#     try:
#         return int(round(float(val)))
#     except:
#         return "Not available"

# def format_price(val):
#     try:
#         return f"${int(round(float(val))):,}"
#     except:
#         return "Not available"

# # Selected Comp Loop
# valid_prices = []

# for _, row in appraisal_df.iterrows():
#     st.markdown(f"### 🏘️ Candidate Property (Rank {int(row['rank'])}):")
#     st.markdown(f"**Address:** {row['candidate_address']}")
#     st.markdown(f"**Model Score:** `{row['score']:.2f}`")
#     st.markdown(f"**Explanation:** {row['explanation']}")

#     # Feature Comparison Table 
#     st.markdown("#### 📊 Feature Comparison")

#     comparison_data = {
#         "Feature": [
#             "Bedrooms", "Full Bathrooms", "Half Bathrooms",
#             "GLA (sq ft)", "Lot Size (sq ft)",
#             "Property Type"
#         ],
#         "Subject": [
#             format_int(row.get("subject_bedrooms")),
#             format_int(row.get("subject_num_full_baths")),
#             format_int(row.get("subject_num_half_baths")),
#             format_int(row.get("subject_gla")),
#             format_int(row.get("subject_lot_size_sf")),
#             row.get('subject_property_type') or "Not available"
#         ],
#         "Candidate": [
#             format_int(row.get("candidate_bedrooms")),
#             format_int(row.get("candidate_num_full_baths")),
#             format_int(row.get("candidate_num_half_baths")),
#             format_int(row.get("candidate_gla")),
#             format_int(row.get("candidate_lot_size_sf")),

#             row.get('candidate_property_type') or "Not available"
#         ]
#     }

#     comparison_df = pd.DataFrame(comparison_data).astype(str)
#     st.table(comparison_df)

#     close_price = row.get("candidate_close_price")
#     st.markdown(f"**Candidate Close Price:** {format_price(close_price)}")

#     # Collect price for suggestion calculation
#     try:
#         valid_prices.append(float(close_price))
#     except:
#         pass

#     # Feedback Radio Button
#     key = f"feedback_{row['orderID']}_{row['rank']}"
#     feedback = st.radio("Do you agree this is a good comparable?", ("👍 Yes", "👎 No"), key=key)

#     feedback_records.append({
#         "orderID": row["orderID"],
#         "rank": row["rank"],
#         "candidate_address": row["candidate_address"],
#         "subject_address": row["subject_address"],
#         "score": row["score"],
#         "is_comp": row["is_comp"],
#         "user_feedback": 1 if feedback == "👍 Yes" else 0
#     })

# st.markdown("---")

# # Suggested Price Estimate
# st.header("💰 Suggested Value Estimate")

# if valid_prices:
#     avg_price = sum(valid_prices) / len(valid_prices)
#     min_price = min(valid_prices)
#     max_price = max(valid_prices)
#     mid_point = min_price + ((max_price-min_price) / 2)

#     st.markdown(
#         f"""
#         <div style='margin-top: 1rem;'>
#             <span style='font-size: 1.15rem; font-weight: 600;'>Average Price of Top-3 Comps:</span>
#             <span style='font-size: 1.15rem; font-weight: 500; margin-left: 0.5rem;'>
#                 {format_price(avg_price)}
#             </span>
#         </div>
#         <div style='margin-top: 1rem;'>
#             <span style='font-size: 1.15rem; font-weight: 600;'>Suggested Price Range:</span>
#             <span style='font-size: 1.15rem; font-weight: 500; margin-left: 0.5rem;'>
#                 {format_price(min_price)} - {format_price(max_price)}
#             </span>
#         </div>
#         <div style='margin-top: 1rem;'>
#             <span style='font-size: 1.15rem; font-weight: 600;'>Suggested Price Range Midpoint:</span>
#             <span style='font-size: 1.15rem; font-weight: 500; margin-left: 0.5rem;'>
#                 {format_price(mid_point)}
#             </span>
#         </div>
#         <div style='margin-top: 1rem; margin-bottom: 1rem'>
#             <span style='font-size: 0.8rem; font-weight: 600; color: grey'>
#                 This estimate is based on the closing prices of the top 3 comparable properties selected by the model.
#             </span>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


# else:
#     st.markdown("Not enough valid close price data to calculate a suggested value.")

# # Submit Feedback 
# if st.button("✅ Submit Feedback"):
#     feedback_df = pd.DataFrame(feedback_records)

#     if os.path.exists(FEEDBACK_FILE):
#         try:
#             existing = pd.read_csv(FEEDBACK_FILE)

#             # Drop duplicates by orderID and candidate_address
#             combined = pd.concat([existing, feedback_df])
#             combined = combined.drop_duplicates(
#                 subset=["orderID", "candidate_address"], keep="last"
#             )
#             combined.to_csv(FEEDBACK_FILE, index=False)
#         except pd.errors.EmptyDataError:
#             feedback_df.to_csv(FEEDBACK_FILE, index=False)
#     else:
#         feedback_df.to_csv(FEEDBACK_FILE, index=False)

#     st.success("✅ Feedback saved to feedback_log.csv!")

#     # Re-run the pipeline from training_data onwards
#     st.info("🔁 Updating model with new feedback...")

#     subprocess.run(["/usr/local/bin/python3.12", "training_data.py"])
#     subprocess.run(["/usr/local/bin/python3.12", "train_model.py"])
#     subprocess.run(["/usr/local/bin/python3.12", "top3_explanations.py"])

#     st.success("✅ Model updated with feedback.")

#     st.rerun()

# if st.button("🔄  Reset Feedback and Model"):
#     if os.path.exists(FEEDBACK_FILE):
#         os.remove(FEEDBACK_FILE)
#         st.warning("🗑️ Feedback log reset.")

#     st.info("🔄 Rebuilding model with original data...")

#     subprocess.run(["/usr/local/bin/python3.12", "data_pipeline.py"])

#     st.success("✅ Model and explanations reset.")
#     st.rerun()


import streamlit as st
import pandas as pd
import os
import subprocess
import altair as alt

st.set_page_config(page_title="🏘️ CompWise AI", layout="wide")


st.markdown("""
<style>
body {
    background-color: #F0F0F0;
    font-family: 'Helvetica Neue', sans-serif;
}
h1, h2, h3, h4 {
    color: #003C2F;
}
div.stButton > button {
    background-color: #69D385;
    color: black;
    font-weight: bold;
    border-radius: 8px;
}
div.stButton > button:hover {
    background-color: #56B973;
}
hr {
    border: none;
    height: 2px;
    background-color: #69D385;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)


EXPLANATIONS_FILE = "top3_gpt_explanations.csv"
FEEDBACK_FILE = "feedback_log.csv"
df = pd.read_csv(EXPLANATIONS_FILE)

# --- SIDEBAR ---
st.sidebar.title("🏠 Property Review Filters")
selected_order = st.sidebar.selectbox("📋 Choose Appraisal (Order ID)", sorted(df["orderID"].unique()))
min_score = st.sidebar.slider("🔍 Min Score Threshold", 0.0, 1.0, 0.5, 0.05)
bedroom_filter = st.sidebar.multiselect(
    "🛏️ Filter by Bedroom Count",
    sorted(df["candidate_bedrooms"].dropna().unique().astype(int)),
    default=None
)
# property_types = st.sidebar.multiselect(
#     "🏡 Property Type",
#     df["candidate_property_type"].dropna().unique(),
#     default=None
# )
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ by Harman")

# --- FILTER DATA ---
filtered_df = df[(df["orderID"] == selected_order) & (df["score"] >= min_score)]
if bedroom_filter:
    filtered_df = filtered_df[filtered_df["candidate_bedrooms"].isin(bedroom_filter)]
# if property_types:
#     filtered_df = filtered_df[filtered_df["candidate_property_type"].isin(property_types)]

appraisal_df = filtered_df.sort_values("rank")

# --- LANDING TITLE ---
st.title("📊 CompWise AI Dashboard")
st.subheader(f"Subject Property: `{appraisal_df['subject_address'].iloc[0]}`")
st.caption("Compare, filter, and interact with top-ranked candidate properties selected by the model.")

# --- FEATURED METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("🔢 Total Candidates", len(appraisal_df))
col2.metric("📉 Avg Score", round(appraisal_df["score"].mean(), 2))
col3.metric("💲Price Range", f"${int(appraisal_df['candidate_close_price'].min()):,} - ${int(appraisal_df['candidate_close_price'].max()):,}")

st.markdown("___")

# --- INTERACTIVE CHARTS ---
st.markdown("### 📈 Data Visualization")

chart1, chart2 = st.columns(2)

with chart1:
    score_chart = alt.Chart(appraisal_df).mark_bar().encode(
        x=alt.X('rank:O', title="Rank"),
        y=alt.Y('score:Q', title="Score"),
        tooltip=['candidate_address', 'score']
    ).properties(title="Candidate Scores by Rank", width=350)
    st.altair_chart(score_chart, use_container_width=True)

with chart2:
    price_chart = alt.Chart(appraisal_df).mark_bar().encode(
        x=alt.X('candidate_close_price:Q', bin=True, title="Close Price"),
        y='count()',
        tooltip=['count()']
    ).properties(title="Candidate Price Distribution", width=350)
    st.altair_chart(price_chart, use_container_width=True)

# --- DISPLAY EACH CANDIDATE ---
st.markdown("### 🏘️ Candidate Comparisons")

feedback_records = []
valid_prices = []

def format_int(val):
    try:
        return int(round(float(val)))
    except:
        return "N/A"

def format_price(val):
    try:
        return f"${int(round(float(val))):,}"
    except:
        return "N/A"

for _, row in appraisal_df.iterrows():
    with st.expander(f"🏡 Rank {int(row['rank'])} | Score: {row['score']:.2f} | {row['candidate_address']}"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Explanation:** {row['explanation']}")
        with col2:
            st.markdown(f"**Price:** {format_price(row['candidate_close_price'])}")

        st.markdown("#### 🔍 Feature Comparison")
        comp_df = pd.DataFrame({
            "Feature": ["Bedrooms", "Bathrooms (Full)", "Bathrooms (Half)", "GLA (sq ft)", "Lot Size", "Type"],
            "Subject": [
                format_int(row["subject_bedrooms"]),
                format_int(row["subject_num_full_baths"]),
                format_int(row["subject_num_half_baths"]),
                format_int(row["subject_gla"]),
                format_int(row["subject_lot_size_sf"]),
                row.get("subject_property_type", "N/A")
            ],
            "Candidate": [
                format_int(row["candidate_bedrooms"]),
                format_int(row["candidate_num_full_baths"]),
                format_int(row["candidate_num_half_baths"]),
                format_int(row["candidate_gla"]),
                format_int(row["candidate_lot_size_sf"]),
                row.get("candidate_property_type", "N/A")
            ]
        })
        st.dataframe(comp_df, use_container_width=True)

        key = f"feedback_{row['orderID']}_{row['rank']}"
        feedback = st.radio("💬 Do you agree it's a good comp?", ["👍 Yes", "👎 No"], key=key)
        feedback_records.append({
            "orderID": row["orderID"],
            "rank": row["rank"],
            "candidate_address": row["candidate_address"],
            "subject_address": row["subject_address"],
            "score": row["score"],
            "is_comp": row["is_comp"],
            "user_feedback": 1 if feedback == "👍 Yes" else 0
        })

        try:
            valid_prices.append(float(row["candidate_close_price"]))
        except:
            pass

# --- SUGGESTED VALUE ESTIMATE ---
st.markdown("___")
st.markdown("### 💰 Suggested Estimate Based on Top-3")

if valid_prices:
    avg_price = sum(valid_prices) / len(valid_prices)
    min_price = min(valid_prices)
    max_price = max(valid_prices)
    mid_point = min_price + ((max_price - min_price) / 2)

    st.success(f"**Average of Valid Close Prices:** {format_price(avg_price)}")
    st.info(f"**Range:** {format_price(min_price)} - {format_price(max_price)}")
    st.warning(f"**Midpoint Estimate:** {format_price(mid_point)}")
else:
    st.error("⚠️ No valid close price data available.")


#     # --- FEATURE IMPORTANCE SECTION ---
# st.markdown("### 🧠 Feature Importance")

# try:
#     feat_df = pd.read_csv("feature_importance.csv")
#     chart = alt.Chart(feat_df).mark_bar().encode(
#         x=alt.X('importance:Q', title="Importance"),
#         y=alt.Y('feature:N', sort='-x', title="Feature"),
#         color=alt.value('#69D385'),
#         tooltip=['feature', 'importance']
#     ).properties(width=600, title="🔍 Model Feature Impact")
#     st.altair_chart(chart, use_container_width=True)

# except Exception as e:
#     st.warning(f"Feature importance data not available. Error: {e}")


# --- FEEDBACK SUBMISSION ---
st.markdown("---")
st.markdown("### 📥 Submit Feedback & Retrain Model")

if st.button("✅ Submit Feedback"):
    feedback_df = pd.DataFrame(feedback_records)
    if os.path.exists(FEEDBACK_FILE):
        try:
            existing = pd.read_csv(FEEDBACK_FILE)
            combined = pd.concat([existing, feedback_df]).drop_duplicates(
                subset=["orderID", "candidate_address"], keep="last"
            )
            combined.to_csv(FEEDBACK_FILE, index=False)
        except pd.errors.EmptyDataError:
            feedback_df.to_csv(FEEDBACK_FILE, index=False)
    else:
        feedback_df.to_csv(FEEDBACK_FILE, index=False)

    st.success("✅ Feedback saved. Model retraining...")
    subprocess.run(["python3", "training_data.py"])
    subprocess.run(["python3", "train_model.py"])
    subprocess.run(["python3", "top3_explanations.py"])
    st.success("🎉 Model updated!")
    st.rerun()

# --- RESET OPTION ---
if st.button("🗑️ Reset Feedback + Rebuild"):
    if os.path.exists(FEEDBACK_FILE):

        os.remove(FEEDBACK_FILE)
    subprocess.run(["python3", "data_pipeline.py"])
    st.success("Model reset to original state.")
    st.rerun()
