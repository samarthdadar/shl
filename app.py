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
