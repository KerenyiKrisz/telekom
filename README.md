# Telco Customer Churn Prediction

A model that predicts which telecom customers are likely to cancel, trained on the IBM Telco Customer Churn dataset. The repo also covers the parts around the model: tests, a CI pipeline, and a serverless deployment to Azure.

## What it does

Churn is expensive, and keeping a customer costs less than finding a new one. The idea here is to flag customers who look likely to leave so a retention team could reach out before they actually cancel.

I used logistic regression rather than something fancier, mostly because it's interpretable. For a retention use case it helps to know *why* someone got flagged, not just that they did. The model currently runs on tenure, monthly charges, and whether the customer has tech support.

## Results

[Drop in your actual numbers, e.g. "Accuracy 80%, recall 73%."]

[One line on what stood out, e.g. "Customers on month-to-month contracts with short tenure were the clearest churn signal."]

Recall is the number I cared about most here, since missing someone who's about to leave is the costly mistake.

## Around the model

Most of the work in this repo isn't the model itself, it's the workflow around it:

- pytest tests that run on every push via GitHub Actions
- reproducible setup with uv and a dev container
- the trained model deployed as an Azure Function that returns a prediction from tenure, monthly charges, and tech-support status
- docs built with MkDocs

## Stack

Python, scikit-learn, pandas, Marimo, pytest, GitHub Actions, Azure Functions, uv, Docker

## What I'd do next

- compare against a random forest or gradient boosting to see if the baseline holds up
- pull in more of the dataset's features instead of just three
- handle class imbalance and check for leakage

---

Started as coursework at ESMT Berlin, cleaned up and extended here.
