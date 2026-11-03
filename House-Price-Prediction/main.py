"""Exploratory analysis for the Ames house price training data."""

# Import library
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# create a png file that contain graphic analyse for the data 
# get input from /data
DATA_DIR = Path(__file__).resolve().parent / "data"
# create the file based on input from /data
OUTPUT_DIR = Path(__file__).resolve().parent / "plots"
# set the theme as white background
sns.set_theme(style="whitegrid", context="notebook")

# EDA
def main():
    # get the data from /data
    train = pd.read_csv(DATA_DIR / "train.csv")
    test = pd.read_csv(DATA_DIR / "test.csv")
    # the target we are looking for is the sale price
    target = "SalePrice"

    # display the amount of columns and rows
    print(f"Training rows/columns: {train.shape}; test rows/columns: {test.shape}")
    # display the amount of duplicate data
    print(f"Duplicate training rows: {train.duplicated().sum()}")
    # the summary of sale price
    print("\nTarget summary:")
    # a description about about the sale price 
    print(train[target].describe().round(2).to_string())
    # asymmetry of the price distribution
    print(f"Skewness: {train[target].skew():.3f}")

    # search for a missing data
    missing = train.isna().sum().sort_values(ascending=False)
    print(f"\nAmount of missing data: {missing.sum()}")
    # display each columns from the most missing data
    print("\nColumns with most missing training values:")
    # display 15 columns along with its missing data exclude the columns without missing data 
    print(missing[missing.gt(0)].head(15).to_string() if missing.gt(0).any() else "None")

    # find data with only numeric type
    numeric = train.select_dtypes(include="number")
    # find the correlation between sale price and other data
    correlations = numeric.corr()[target].drop(target).sort_values(ascending=False)
    print("\nStrongest numeric correlations with SalePrice:")
    # display 10 columns with high correlation 
    print(correlations.head(10).round(3).to_string())
    print("\nMost negative numeric correlations with SalePrice:")
    # display 5 columns with little correlation
    print(correlations.tail(5).round(3).to_string())

#     # create folder for graph
#     OUTPUT_DIR.mkdir(exist_ok=True)
#     # create 4 graphs
#     fig, axes = plt.subplots(2, 2, figsize=(14, 10))
#     sns.histplot(train[target], bins=35, kde=True, ax=axes[0, 0], color="#3977a8")
#     axes[0, 0].set(title="SalePrice distribution (raw)", xlabel="Sale price ($)", ylabel="Homes")
#     sns.histplot(np.log1p(train[target]), bins=35, kde=True, ax=axes[0, 1], color="#4d9a75")
#     axes[0, 1].set(title="SalePrice distribution (log1p)", xlabel="log(1 + sale price)", ylabel="Homes")
#     sns.boxplot(x=train[target], ax=axes[1, 0], color="#e6a45b")
#     axes[1, 0].set(title="SalePrice spread and potential outliers", xlabel="Sale price ($)")
#     sns.scatterplot(data=train, x="GrLivArea", y=target, alpha=.55, ax=axes[1, 1], color="#805a9e")
#     axes[1, 1].set(title="Above-ground living area vs SalePrice", xlabel="Living area (sq ft)", ylabel="Sale price ($)")
#     fig.suptitle("Ames Housing: target exploration", fontsize=16)
#     fig.tight_layout()
#     fig.savefig(OUTPUT_DIR / "saleprice_exploration.png", dpi=160, bbox_inches="tight")
#     plt.show()
# 
#     top = correlations.head(10).index.tolist()
#     plt.figure(figsize=(11, 8))
#     sns.heatmap(train[top + [target]].corr(), annot=True, fmt=".2f", cmap="vlag", center=0, square=True)
#     plt.title("Correlations among SalePrice and strongest numeric features")
#     plt.tight_layout()
#     plt.savefig(OUTPUT_DIR / "saleprice_correlations.png", dpi=160, bbox_inches="tight")
#     plt.show()


if __name__ == "__main__":
    main()
