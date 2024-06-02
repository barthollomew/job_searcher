"""
Assignment 2: Job Search Website
    1. Job search bar and return
    2. Create new job listing and add to database
"""

import pandas as pd
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from model_generator import df, ft_model, get_vector, lr_model, scaler, search_jobs

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("search_job.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    keyword = data["keyword"]
    results = fetchSimilarJobs(keyword)
    return jsonify(results)


def fetchSimilarJobs(keyword):
    results = search_jobs(keyword, df, ft_model, scaler)
    output = []
    for result in results:
        job = df.iloc[result[0]]
        output.append(
            {
                "Title": job["Title"],
                "Company": job["Company"],
                "Location": job["Location"],
                "ContractType": job["ContractType"],
                "Category": job["Category"],
                "Salary": job["Salary"],
                "OpenDate": job["OpenDate"],
                "CloseDate": job["CloseDate"],
            }
        )
    return output


@app.route("/add_job")
def indexAddJob():
    return render_template("add_job.html")


@app.route("/addingJob", methods=["POST"])
def addJob():
    data = request.get_json()
    new_job = {
        "Title": data["title"],
        "Company": "Company",
        "Salary": data["salary"],
        "Location": data["location"],
        "ContractType": data["contract_type"],
        "Category": data["category"],
        "OpenDate": "2024-06-01 00:00:00",
        "CloseDate": "2024-07-01 00:00:00",
    }

    global df
    df = add_job_listing(df, new_job)
    df.to_csv("cleaned_job_listings_with_new.csv", index=False)

    return jsonify(new_job)


@app.route("/recommendCategory", methods=["POST"])
def recommendCategory():
    data = request.get_json()
    description = data["description"]
    recommended_category = recommend_categories(description, ft_model, lr_model)
    return jsonify({"recommended_category": recommended_category})


def recommend_categories(description, ft_model, lr_model):
    description_vector = get_vector(description, ft_model).reshape(1, -1)
    predicted_category = lr_model.predict(description_vector)
    return predicted_category[0]


def add_job_listing(df, job_listing):
    new_job_df = pd.DataFrame([job_listing])
    df = pd.concat([df, new_job_df], ignore_index=True)
    return df


if __name__ == "__main__":
    app.run(debug=True)
