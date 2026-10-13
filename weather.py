import pandas as pd
import matplotlib.pyplot as plt

dates = [f"2026-03-{d:02d}" for d in range(1, 16)]
raw = pd.DataFrame({
    "Date": dates,
    "City": [" islamabad", "ISLAMABAD ", "Islamabad"] * 5,
    "Temperature": ["32C", "29C", "24C", "33C", "31C", "26C", "34C", "30C",
                    "23C", "35C", "32C", "28C", "25C", "33C", "31C"],
    "Humidity": [45, 70, None, 40, 50, None, 38, 55, 80, None, 48, 65, None, 42, 52],
    "Condition": ["sunny", " Rainy", "CLOUDY ", "Sunny", "SUNNY", "cloudy", "Sunny",
                  " sunny", "rainy", "Sunny ", "Cloudy", "CLOUDY", "RAINY", "sunny",
                  "Cloudy "],
})

# add one duplicated row
df = pd.concat([raw, raw.iloc[[4]]], ignore_index=True)
print("Raw rows:", len(df))

# (a) cleaning
df["City"] = df["City"].str.strip().str.title()
df["Condition"] = df["Condition"].str.strip().str.title()
df["Temperature"] = df["Temperature"].str.replace("C", "", regex=False).astype(float)
df["Date"] = pd.to_datetime(df["Date"])
df = df.drop_duplicates()
print("Rows after dropping duplicates:", len(df))

median_h = df["Humidity"].median()
df["Humidity"] = df["Humidity"].fillna(median_h)
print("Missing Humidity filled with median:", median_h)

# (b) one-hot encoding
encoded = pd.get_dummies(df, columns=["Condition"], dtype=int)
print(encoded.filter(like="Condition_").head())

# (d) correlation
corr = df["Temperature"].corr(df["Humidity"])
print("Correlation (Temperature, Humidity):", round(corr, 2))

counts = df["Condition"].value_counts()
print("Condition counts:")
print(counts)

# (c, e, f) 2x2 dashboard
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

axes[0, 0].plot(df["Date"], df["Temperature"], marker="o", color="tomato")
axes[0, 0].set_title("Temperature over Time")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Temperature (°C)")
axes[0, 0].tick_params(axis="x", rotation=45)

axes[0, 1].scatter(df["Temperature"], df["Humidity"], color="darkorange", s=60)
axes[0, 1].set_title("Temperature vs. Humidity")
axes[0, 1].set_xlabel("Temperature (°C)")
axes[0, 1].set_ylabel("Humidity (%)")

axes[1, 0].pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
axes[1, 0].set_title("Days per Condition")

axes[1, 1].hist(df["Temperature"], bins=5, color="seagreen", edgecolor="white")
axes[1, 1].set_title("Temperature Distribution")
axes[1, 1].set_xlabel("Temperature (°C)")
axes[1, 1].set_ylabel("Number of Days")

fig.suptitle("Weather Overview", fontsize=16)
plt.tight_layout()
plt.savefig("weather_dashboard.png")
plt.show()
print("Saved weather_dashboard.png")
