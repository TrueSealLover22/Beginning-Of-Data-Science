# House Price Prediction (Ames Housing)

Exploratory analysis of the Ames housing training data. `main.py` prints a
summary report of the target variable (`SalePrice`), missing values, and the
numeric features most correlated with sale price. A plotting block for saving
charts is included but currently commented out.

## Project structure

```
House-Price-Prediction/
├── main.py                    # EDA + plotting script
├── data/
│   ├── train.csv              # training data (includes SalePrice)
│   ├── test.csv               # test data (no SalePrice)
│   ├── sample_submission.csv  # submission format
│   └── data_description.txt   # column documentation
├── plots/                     # generated output
├── notebook/                  # exploratory notebook
└── README.md
```

## Requirements

- Python 3.9+
- `pandas`, `numpy`, `matplotlib`, `seaborn`

## Usage

From the `House-Price-Prediction` directory:

```bash
python main.py
```

## What `main.py` does

### 1. Setup

```python
DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "plots"
sns.set_theme(style="whitegrid", context="notebook")
```

Paths are resolved relative to the script so it runs from any working
directory, and the Seaborn `whitegrid`/`notebook` theme is applied globally.
All analysis lives in a `main()` function, guarded by
`if __name__ == "__main__":`.

### 2. Load the data

Reads `data/train.csv` and `data/test.csv` into DataFrames and sets the target
to `SalePrice`.

### 3. Dataset overview

- Prints the shape (rows/columns) of both the training and test sets.
- Counts duplicate rows in the training data.

### 4. Target summary

- Prints descriptive statistics for `SalePrice` (count, mean, std, min,
  quartiles, max).
- Prints the skewness of the sale price distribution. A strongly positive
  value (1.883 here) indicates a long right tail, which is why a log
  transform is often applied before modelling.

### 5. Missing-value report

Sums missing values per column across the training data, prints the total
number of missing cells, then lists the 15 columns with the most missing
values (columns with zero missing values are excluded).

### 6. Correlation analysis

- Keeps only the numeric columns of the training data.
- Computes Pearson correlations of every numeric column with `SalePrice`,
  sorted descending.
- Prints the 10 strongest positive correlations (led by `OverallQual` and
  `GrLivArea`) and the 5 most negative ones.
- Like all correlations, these show association only, not causation.

### 7. Plotting block (currently commented out)

The commented section creates `plots/` and generates two figures:

- `saleprice_exploration.png` – a 2×2 dashboard with:
  - raw `SalePrice` histogram with KDE
  - `log1p(SalePrice)` histogram with KDE (shows the log transform reducing
    skew)
  - box plot of `SalePrice` to expose spread and potential outliers
  - scatter plot of `GrLivArea` vs `SalePrice`
- `saleprice_correlations.png` – heatmap of correlations between `SalePrice`
  and the 10 strongest numeric features.

Both are saved at 160 dpi with `bbox_inches="tight"` and shown with
`plt.show()`. Uncomment this block to regenerate the charts.

## Outputs

| File | Description |
|------|-------------|
| Console report | Shapes, duplicates, target stats, missing values, top correlations |
| `plots/saleprice_exploration.png` | Target distribution, log transform, outliers, GrLivArea scatter *(plotted block disabled)* |
| `plots/saleprice_correlations.png` | Correlation heatmap *(plotted block disabled)* |

## Notes and limitations

- The input filenames (`train.csv`, `test.csv`) are hardcoded in `DATA_DIR`.
- The plotting code is commented out, so running the script currently only
  prints the text report; the existing PNGs in `plots/` came from an earlier
  run.
- Analysis is descriptive EDA only — no model has been fitted yet.