import pandas as pd

file_path = 'data/issues.csv'

try:
    df = pd.read_csv(file_path)
    print("Successfully loaded the new dataset!")
    print("-" * 50)
    print("Dataset Info:")
    print(f"Total number of issues: {len(df)}")
    print("\nDistribution of labels:")
    print(df['label'].value_counts())
    print("-" * 50)
    print("Looks like a great, balanced dataset. Ready for Phase 2!")

except FileNotFoundError:
    print(f"Error: The file was not found at {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")