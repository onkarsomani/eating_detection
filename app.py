import pandas as pd
import numpy as np

def process_predictions(csv1_path, csv2_path, output_csv_path):
    # Read the CSV files
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)

    # Convert timestamps to pandas datetime for easier handling
    df1['timestamp'] = pd.to_datetime(df1['timestamp'])
    df2['timestamp'] = pd.to_datetime(df2['timestamp'])

    # Round timestamps to the nearest 5-second interval
    df1['rounded_time'] = df1['timestamp'].dt.floor('1S')
    df2['rounded_time'] = df2['timestamp'].dt.floor('1S')

    # Group by the 5-second intervals and calculate the mean predictions
    df1_avg = df1.groupby('rounded_time')['prediction'].mean().reset_index()
    df2_avg = df2.groupby('rounded_time')['prediction'].mean().reset_index()

    # Merge the two datasets on the rounded time
    merged = pd.merge(df1_avg, df2_avg, on='rounded_time', how='outer', suffixes=('_csv1', '_csv2'))

    # Take the average of the two predictions
    merged['final_prediction'] = merged[['prediction_csv1', 'prediction_csv2']].mean(axis=1)

    # Fill missing predictions with 0 if no data exists for a timestamp in one of the files
    merged = merged.fillna(0)

    # Save the results to a new CSV
    merged[['rounded_time', 'final_prediction']].to_csv(output_csv_path, index=False)

    print(f"Processed predictions saved to {output_csv_path}")

# Paths to input and output files
csv1_path = '/Users/onkar/Documents/comding/chomding/eating_detection/Evaluation_Results_TFLite1.csv'
csv2_path = '/Users/onkar/Documents/comding/chomding/eating_detection/full_predictions_more.csv'
output_csv_path = 'final_predictions_more_1_sec_interval.csv'

# Call the function
process_predictions(csv1_path, csv2_path, output_csv_path)
