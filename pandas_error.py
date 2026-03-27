import pandas as pd

df = None

try:
    df: pd.DataFrame = pd.read_csv("data.csv")
except pd.errors.EmptyDataError:
    print(f"Error: The CSV file is empty.")
except pd.errors.ParserError:
    print(f"Error parsing CSV file.")
except Exception:
    print(f"Unexpected error.") 

print(df)
