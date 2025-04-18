import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SHL Assessment Recommender")
st.title("🔍 SHL Assessment Recommender")

query = st.text_area("Enter job description or query:")

if st.button("Recommend Assessments"):
    if not query:
        st.warning("Please enter a query to get recommendations.")
    else:
        with st.spinner("Fetching recommendations..."):
            response = requests.post("http://localhost:8000/recommend", json={"query": query})
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                df["name"] = df.apply(lambda row: f"[{row['name']}]({row['url']})", axis=1)
                df = df.drop(columns=["url"])
                st.markdown("### Recommended Assessments:")
                st.write(df.to_markdown(index=False), unsafe_allow_html=True)
            else:
                st.error("Failed to fetch recommendations. Please try again.")

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dummy function to simulate recommendations
def get_recommendations(job_description):
    if "data" in job_description.lower():
        return ["SHL Numerical Reasoning", "SHL Logical Reasoning"]
    elif "manager" in job_description.lower():
        return ["SHL Leadership", "SHL Situational Judgement"]
    else:
        return ["SHL General Aptitude Test"]

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    job_desc = data.get("description", "")
    if not job_desc:
        return jsonify({"error": "No description provided"}), 400

    results = get_recommendations(job_desc)
    return jsonify({"recommendations": results})

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
