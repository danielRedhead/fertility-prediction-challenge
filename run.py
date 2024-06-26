"""
This script calls submission.py. Add your method to submission.py to run your
prediction method.

To test your submission use the following command:

python run.py predict 

For example:

python run.py predict data/PreFer_fake_data.csv

Optionally, you can use the score function to calculate evaluation scores given 
your predictions and the ground truth within the training dataset.

"""

import sys
import argparse
import pandas as pd
import submission

parser = argparse.ArgumentParser(description="Process data.")

parser.add_argument("data_path", help="Path to data data CSV file.")
parser.add_argument(
    "background_data_path", help="Path to background data data CSV file."
)
parser.add_argument("--output", help="Path to prediction output CSV file.")

args = parser.parse_args()


def predict(data_path, background_data_path, output):
    """Predict Score (evaluate) the predictions and write the metrics.

    This function takes the path to an data CSV file containing the data data.
    It calls submission.py clean_df and predict_outcomes writes the predictions
    to a new output CSV file.

    This function should not be modified.
    """

    if output is None:
        output = sys.stdout
    data_df = pd.read_csv(
        data_path, encoding="latin-1", encoding_errors="replace", low_memory=False
    )
    background_data_df = pd.read_csv(
        background_data_path,
        encoding="latin-1",
        encoding_errors="replace",
        low_memory=False,
    )

    predictions = submission.predict_outcomes(data_df, background_data_df)
    assert (
        predictions.shape[1] == 2
    ), "Predictions must have two columns: nomem_encr and prediction"
    # Check for the columns, order does not matter
    assert set(predictions.columns) == set(
        ["nomem_encr", "prediction"]
    ), "Predictions must have two columns: nomem_encr and prediction"

    predictions.to_csv(output, index=False)


def score(prediction_path, ground_truth_path, output):
    """Score (evaluate) the predictions and write the metrics.

    This function takes the path to a CSV file containing predicted outcomes and the
    path to a CSV file containing the ground truth outcomes. It calculates the overall
    prediction accuracy, and precision, recall, and F1 score for having a child
    and writes these scores to a new output CSV file.

    This function should not be modified.
    """

    if output is None:
        output = sys.stdout
    # Load predictions and ground truth into dataframes
    predictions_df = pd.read_csv(prediction_path)
    ground_truth_df = pd.read_csv(ground_truth_path)

    # Merge predictions and ground truth on the 'id' column
    merged_df = pd.merge(predictions_df, ground_truth_df, on="nomem_encr", how="right")

    # Calculate accuracy
    accuracy = len(merged_df[merged_df["prediction"] == merged_df["new_child"]]) / len(
        merged_df
    )

    # Calculate true positives, false positives, and false negatives
    true_positives = len(
        merged_df[(merged_df["prediction"] == 1) & (merged_df["new_child"] == 1)]
    )
    false_positives = len(
        merged_df[(merged_df["prediction"] == 1) & (merged_df["new_child"] == 0)]
    )
    false_negatives = len(
        merged_df[(merged_df["prediction"] == 0) & (merged_df["new_child"] == 1)]
    )

    # Calculate precision, recall, and F1 score
    try:
        precision = true_positives / (true_positives + false_positives)
    except ZeroDivisionError:
        precision = 0
    try:
        recall = true_positives / (true_positives + false_negatives)
    except ZeroDivisionError:
        recall = 0
    try:
        f1_score = 2 * (precision * recall) / (precision + recall)
    except ZeroDivisionError:
        f1_score = 0
    # Write metric output to a new CSV file
    metrics_df = pd.DataFrame(
        {
            "accuracy": [accuracy],
            "precision": [precision],
            "recall": [recall],
            "f1_score": [f1_score],
        }
    )
    metrics_df.to_csv(output, index=False)


if __name__ == "__main__":
    args = parser.parse_args()
    predict(args.data_path, args.background_data_path, args.output)
