"""
Assignment 2: Job Search Website
    1. Job search bar and return
    2. Create new job listing and add to database
"""

from flask import Flask, render_template, request
from flask_cors import CORS

from model_generator import df, ft_model, scaler, search_jobs

app = Flask(__name__)

CORS(app)


@app.route("/")
def index():
    return render_template("search_job.html", message="Received backend message!")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    keyword = data["keyword"]
    print("Keyword: ", keyword)
    results = fetchSimilarJobs(keyword)
    print(results)
    return results


def fetchSimilarJobs(keyword):
    results = search_jobs(keyword, df, ft_model, scaler)

    print(f"Found {len(results)} matching job advertisements:")
    for result in results:
        print(f"Title: {result[1]}, Similarity: {result[2]}")

    def display_job_details(job_id, df):
        job = df.iloc[job_id]
        print(f"Title: {job['Title']}")
        print(f"Company: {job['Company']}")
        print(f"Location: {job['Location']}")
        print(f"ContractType: {job['ContractType']}")
        print(f"Category: {job['Category']}")
        print(f"Salary: {job['Salary']}")
        print(f"OpenDate: {job['OpenDate']}")
        print(f"CloseDate: {job['CloseDate']}")

    if results:
        display_job_details(results[0][0], df)

    return results


@app.route("/add_job")
def indexAddJob():
    return render_template("add_job.html", message="Received backend message!")


# @app.route("/addingJob", methods=["POST"])
# def addJob():
#     """
#     Testing category recommendation using linear regression model
#     """
#
#     def recommend_categories(description, ft_model, lr_model):
#         description_vector = get_vector(description, ft_model).reshape(1, -1)
#         predicted_category = lr_model.predict(description_vector)
#         return predicted_category[0]
#
#     # Example of creating a new job listing
#     new_job = {
#         "Title": "Software Engineer",
#         "Description": "We are looking for a skilled software engineer...",
#         "Salary": 90000,
#         "Location": "Sydney",
#         "ContractType": "full_time",
#         "OpenDate": "2024-06-01 00:00:00",
#         "CloseDate": "2024-07-01 00:00:00",
#     }
#
#     new_job["Category"] = recommend_categories(
#         new_job["Description"], ft_model, lr_model
#     )
#
#     print(f"Recommended Category: {new_job['Category']}")
#
#
# # # Adding new job listing
# # def add_job_listing(df, job_listing):
# #     new_job_df = pd.DataFrame([job_listing])
# #     df = pd.concat([df, new_job_df], ignore_index=True)
# #     return df
# #
# # df = add_job_listing(df, new_job)
# # df.to_csv("cleaned_job_listings_with_new.csv", index=False)
#
#
if __name__ == "__main__":
    app.run(debug=True)
