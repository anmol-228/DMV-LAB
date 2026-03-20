import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = {
    "Name": ["A", "B", "C", "D", "E"],
    "Age": [20, np.nan, 22, np.nan, 25],
    "Marks": [85, 90, np.nan, 88, np.nan]
}

df = pd.DataFrame(data)

print("Original Data:\n", df)

print("\nMissing Values Count:\n", df.isnull().sum())

df["Age"] = df["Age"].fillna(df["Age"].mean())
df["Marks"] = df["Marks"].fillna(df["Marks"].median())

print("\nAfter Handling Missing Values:\n", df)

plt.figure(figsize=(6, 3))
plt.imshow(pd.DataFrame(data).isnull(), cmap="Reds", aspect="auto")
plt.yticks(range(len(df)), df["Name"])
plt.xticks(range(2), ["Age", "Marks"])
plt.title("Missing Values Heatmap (Before Handling)")
plt.show()

plt.figure(figsize=(6, 3))
plt.imshow(df.isnull(), cmap="Greens", aspect="auto")
plt.yticks(range(len(df)), df["Name"])
plt.xticks(range(2), ["Age", "Marks"])
plt.title("Missing Values Heatmap (After Handling)")
plt.show()
