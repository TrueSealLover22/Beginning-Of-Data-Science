"""Explore student dropout risk data and save summary visualizations."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


DATA_DIR = Path(__file__).resolve().parent / "data"
# create the file based on input from /data
OUTPUT_DIR = Path(__file__).resolve().parent / "plots"
OUTPUT_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")
df = pd.read_csv(DATA_DIR / "student_dropout_risk_2026.csv")
target = "dropout"
numeric = df.select_dtypes(include=np.number)
features = [c for c in ["attendance_rate", "assignments_submitted_rate", "gpa_semester_1",
                         "gpa_semester_2", "units_failed", "missed_deadlines",
                         "weekly_work_hours", "sleep_hours", "stress_level",
                         "satisfaction_score", "commute_time_mins"] if c in df]

print("STUDENT DROPOUT DATASET")
print(f"Rows: {len(df):,} | Columns: {df.shape[1]} | Duplicate rows: {df.duplicated().sum():,}")
print("Missing values by column:")
missing = df.isna().sum()
print(missing[missing.gt(0)].to_string() if missing.gt(0).any() else "None")
print("\nColumn types and unique values:")
print(pd.DataFrame({"dtype": df.dtypes.astype(str), "unique": df.nunique()}).to_string())

counts = df[target].value_counts().sort_index()
rates = df.groupby(target)[features].mean().T
rates.columns = [f"dropout={c}" for c in rates.columns]
print("\nDropout counts and rates:")
print(pd.DataFrame({"count": counts, "percent": counts / len(df) * 100}).round(2))
print("\nFeature means by dropout status:")
print(rates.round(2).to_string())
print("\nNumeric correlations with dropout (association, not causation):")
print(numeric.corr()[target].drop(target).sort_values().round(3).to_string())

categorical = [c for c in ["study_mode", "course_type", "family_income_level", "gender"] if c in df]
for col in categorical:
    print(f"\nDropout rate (%) by {col}:")
    print((df.groupby(col, observed=True)[target].mean().mul(100).sort_values(ascending=False)).round(2).to_string())

if {"gpa_semester_1", "gpa_semester_2"}.issubset(df.columns):
    df["gpa_change"] = df["gpa_semester_2"] - df["gpa_semester_1"]
    print("\nGPA change by dropout status:")
    print(df.groupby(target)["gpa_change"].agg(["mean", "median"]).round(3).to_string())

# Dashboard: class balance, academic/behavioral comparisons, correlation, and group rates.
fig, axes = plt.subplots(2, 2, figsize=(16, 11))
ax = axes[0, 0]
labels = ["Stayed enrolled" if i == 0 else "Dropped out" for i in counts.index]
bars = ax.bar(labels, counts.values, color=["#4C78A8", "#F58518"][:len(counts)])
ax.set_title("Student counts by dropout status")
ax.set_ylabel("Students")
for bar, count in zip(bars, counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{count:,}\n({count/len(df):.1%})", ha="center", va="bottom")

ax = axes[0, 1]
box_features = [c for c in ["attendance_rate", "gpa_semester_2", "units_failed", "stress_level"] if c in df]
long = df.melt(id_vars=target, value_vars=box_features, var_name="Measure", value_name="Value")
sns.boxplot(data=long, x="Measure", y="Value", hue=target, ax=ax, showfliers=False)
ax.set_title("Academic and wellbeing measures by dropout status")
ax.set_xlabel("")
ax.tick_params(axis="x", rotation=18)
ax.legend(title="Dropout")

ax = axes[1, 0]
corr = numeric.corr()[target].drop(target).sort_values()
colors = ["#E45756" if v < 0 else "#54A24B" for v in corr.values]
ax.barh(corr.index, corr.values, color=colors)
ax.axvline(0, color="black", linewidth=.8)
ax.set_title("Numeric feature correlations with dropout")
ax.set_xlabel("Pearson correlation")

ax = axes[1, 1]
group_col = "study_mode" if "study_mode" in df else categorical[0]
group_rate = df.groupby(group_col, observed=True)[target].mean().mul(100).sort_values()
ax.barh(group_rate.index.astype(str), group_rate.values, color="#72B7B2")
ax.set_title(f"Dropout rate by {group_col}")
ax.set_xlabel("Dropout rate (%)")

fig.suptitle("Student Dropout Risk: Dataset Overview", fontsize=17, fontweight="bold")
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "student_dropout_dashboard.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# Standalone detail charts for sharing or further inspection.
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(x=group_rate.values, y=group_rate.index.astype(str), ax=ax, color="#72B7B2")
ax.set(title=f"Dropout rate by {group_col}", xlabel="Dropout rate (%)", ylabel=group_col)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "dropout_rate_by_study_mode.png", dpi=180)
plt.close(fig)

if "gpa_change" in df:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x=target, y="gpa_change", ax=ax, showfliers=False)
    ax.set(title="Semester GPA change by dropout status", xlabel="Dropout (0 = no, 1 = yes)", ylabel="Semester 2 GPA − Semester 1 GPA")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "gpa_change_by_dropout.png", dpi=180)
    plt.close(fig)

print(f"\nCharts saved to: {OUTPUT_DIR}")
