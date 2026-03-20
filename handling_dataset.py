from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATASET_PATH = Path(__file__).resolve().parent / "data" / "updated_dataset.csv"

df = pd.read_csv(DATASET_PATH)
print("Loaded dataset from:", DATASET_PATH)

print("Missing Values Before:\n", df.isnull().sum())

df["title"] = df["title"].fillna(df["title"].mode()[0])

numeric_cols = ["episodes", "score", "scored_by", "rank"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].mean())

outlier_count = 0

for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]
    outlier_count += len(outliers)

    df[col] = np.where((df[col] < lower) | (df[col] > upper),
                       df[col].median(), df[col])

print("\nMissing Values After:\n", df.isnull().sum())
print("\nTotal Outliers Fixed:", outlier_count)


df_small = df.head(10).copy()


df_small["short_title"] = df_small["title"].str.slice(0, 15)

# BAR CHART
plt.figure(figsize=(12,6))
plt.bar(df_small["short_title"], df_small["score"])

plt.title("Top 10 Anime Scores")
plt.xlabel("Anime Title")
plt.ylabel("Score")

plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()

# 6. PIE CHART
plt.figure(figsize=(8,8))

plt.pie(df_small["episodes"],
        labels=df_small["short_title"],
        autopct='%1.1f%%')

plt.title("Episodes Distribution (Top 10 Anime)")
plt.show()

# 7. STEP (STAIR) CHART
plt.figure(figsize=(12,6))

plt.step(df_small["short_title"], df_small["score"], where='mid')

plt.title("Score Trend (Top 10 Anime)")
plt.xlabel("Anime Title")
plt.ylabel("Score")

plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()
