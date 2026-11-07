# Student Dropout Risk Analysis

An exploratory data analysis of a synthetic-style student dataset (100,000 rows,
34 columns) that looks at which academic, behavioural, and wellbeing factors are
associated with a student dropping out. `main.py` prints a full text report to
the console and saves a dashboard plus two standalone charts as PNG files.

## Project structure

```
Student-Dropout/
├── main.py                                  # analysis + plotting script
├── data/
│   └── student_dropout_risk_2026.csv        # input dataset
├── plots/                                   # generated output (created on run)
├── notebook/
│   └── csv-analysis.ipynb                   # exploratory notebook
└── README.md
```

## Dataset

`data/student_dropout_risk_2026.csv` contains one row per student. The target
column is `dropout` (`0` = stayed enrolled, `1` = dropped out). Other columns
cover:

- **Demographics** – `age`, `gender`, `nationality`, `family_income_level`,
  `first_generation`, `disability_status`, `international_student`
- **Enrolment** – `course_type`, `study_mode`, `semester`, `scholarship_holder`,
  `tuition_up_to_date`, `part_time_job`, `weekly_work_hours`
- **Academic performance** – `admission_grade`, `previous_qualification_grade`,
  `units_enrolled`, `units_passed`, `units_failed`, `gpa_semester_1`,
  `gpa_semester_2`
- **Behaviour** – `attendance_rate`, `assignments_submitted_rate`,
  `library_visits_per_month`, `lms_logins_per_week`, `missed_deadlines`,
  `extracurricular_activities`
- **Wellbeing** – `stress_level`, `sleep_hours`, `satisfaction_score`,
  `commute_time_mins`, `mental_health_support`

## Requirements

- Python 3.9+
- `pandas`, `numpy`, `matplotlib`, `seaborn`

## Usage

From the `Student-Dropout` directory:

```bash
python main.py
```

The script reads the CSV from `data/`, writes charts to `plots/`, and prints its
findings to the terminal.

## What `main.py` does

### 1. Setup

```python
DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "plots"
OUTPUT_DIR.mkdir(exist_ok=True)
```

Paths are resolved relative to the script, so it can be run from any working
directory. `plots/` is created if it does not exist, and the Seaborn
`whitegrid`/`deep` theme is applied globally.

### 2. Load the data and pick features

The CSV is read into a DataFrame with `pd.read_csv`, the target is set to
`"dropout"`, and `numeric` keeps every numeric column for later correlation
work. The `features` list is a curated subset of academic/behavioural measures
(attendance, assignments submitted, both semester GPAs, failed units, missed
deadlines, work hours, sleep, stress, satisfaction, commute). Only columns that
actually exist in the DataFrame are kept, so the script tolerates a slightly
different column set.

### 3. Data quality report

Prints the row/column counts, the number of duplicate rows, any columns with
missing values, and a table of each column's dtype and number of unique values.
This is a quick sanity check before looking at results.

### 4. Comparison by dropout status

- `counts` – number of students in each dropout class (`value_counts`).
- `rates` – mean of every curated feature grouped by `dropout`. Columns are
  renamed to `dropout=0` / `dropout=1` so the two groups can be compared
  side by side.
- Prints class counts with percentages, the feature-mean table, and the Pearson
  correlation of every numeric column with `dropout` (sorted ascending so the
  strongest negative relationships appear first).
- Correlations are labelled as **association, not causation**.

### 5. Categorical breakdowns

For each of `study_mode`, `course_type`, `family_income_level`, and `gender`
(if present), prints the dropout rate (percentage) per category, sorted from
highest to lowest. This shows which groups drop out at a higher rate.

### 6. GPA change feature

If both semester GPA columns exist, a derived column
`gpa_change = gpa_semester_2 - gpa_semester_1` is added, and its mean and
median are compared between students who stayed and students who dropped out.
The derived column is also used by one of the saved charts.

### 7. Dashboard (`plots/student_dropout_dashboard.png`)

A 2×2 figure (`figsize=(16, 11)`) with four panels:

| Panel | Chart | Purpose |
|-------|-------|---------|
| Top-left | Bar chart of student counts by dropout status, with count and percentage labels | Shows class balance |
| Top-right | Box plot of attendance, semester-2 GPA, failed units, and stress level, split by dropout | Compares distributions (outliers hidden) |
| Bottom-left | Horizontal bar chart of correlations with dropout (red = negative, green = positive) | Ranks numeric predictors |
| Bottom-right | Horizontal bar chart of dropout rate by `study_mode` (or the first available categorical column) | Highlights differences between study modes |

The figure is saved at 180 dpi with `bbox_inches="tight"` and closed afterwards
to free memory.

### 8. Standalone charts

- `plots/dropout_rate_by_study_mode.png` – a larger, shareable version of the
  dropout-rate-by-group panel (Seaborn `barplot`).
- `plots/gpa_change_by_dropout.png` – box plot of `gpa_change` split by dropout
  status (only created when the GPA columns were available).

Finally the script prints the output directory path.

## Outputs

| File | Description |
|------|-------------|
| `plots/student_dropout_dashboard.png` | 4-panel overview dashboard |
| `plots/dropout_rate_by_study_mode.png` | Dropout rate by study mode |
| `plots/gpa_change_by_dropout.png` | GPA change distribution by dropout status |

## Notes and limitations

- The input filename (`student_dropout_risk_2026.csv`) is hardcoded, so a new
  data file must either use the same name or the path in `main.py` must be
  updated.
- The bottom-right dashboard panel falls back to `categorical[0]`, so at least
  one of the four categorical columns must exist in the data.
- The second standalone chart is always written as
  `dropout_rate_by_study_mode.png`, even if a different grouping column was
  used.
- All results are descriptive. Correlations and group differences show
  association only and do not establish that a factor causes dropout.
