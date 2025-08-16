"""
Employee Performance Visualization (Marplotlib/Seaborn + HTML export)
Contact: 24f2005847@ds.study.iitm.ac.in
- Generates a 100-row synthetic dataset with required columns (incl. 'Operations')
- Calculates frequency count for 'Operations' department
- Prints the frequency to console
- Creates a histogram (bar chart) of department distribution
- Exports a self-contained HTML (chart + code)
"""

import io
import os
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mpld3

# ------------- 1) Generate dataset (100 rows) -------------
np.random.seed(42)

departments = ["Finance", "R&D", "Marketing", "IT", "Operations", "HR", "Sales"]
regions = ["Asia Pacific", "Europe", "North America", "Latin America", "Middle East & Africa"]

n = 100
employee_id = [f"EMP{str(i+1).zfill(3)}" for i in range(n)]
department = np.random.choice(departments, size=n, p=[0.15,0.15,0.15,0.15,0.25,0.075,0.075])  # ensure Ops appears often
region = np.random.choice(regions, size=n)
performance_score = np.round(np.random.normal(loc=72, scale=8, size=n), 2)
years_experience = np.random.randint(1, 16, size=n)
satisfaction_rating = np.round(np.clip(np.random.normal(loc=3.8, scale=0.7, size=n), 1, 5), 1)

df = pd.DataFrame({
    "employee_id": employee_id,
    "department": department,
    "region": region,
    "performance_score": performance_score,
    "years_experience": years_experience,
    "satisfaction_rating": satisfaction_rating
})

# Also include the exact 5 sample rows stated in the prompt at the top (override first 5 rows)
sample_rows = pd.DataFrame([
    ["EMP001","Finance","Asia Pacific",74.34,7,4.6],
    ["EMP002","R&D","Latin America",67.17,5,4.3],
    ["EMP003","Marketing","North America",71.87,9,3.6],
    ["EMP004","IT","Europe",71.98,5,3.1],
    ["EMP005","Finance","Latin America",82.42,7,3.9],
], columns=df.columns)
df.iloc[:5] = sample_rows

# Save CSV (optional artifact)
df.to_csv("employees.csv", index=False)

# ------------- 2) Calculate frequency count for 'Operations' -------------
ops_count = (df["department"] == "Operations").sum()
print(f"Frequency count for 'Operations' department: {ops_count}")

# ------------- 3) Plot histogram/bar of department distribution -------------
plt.figure(figsize=(8, 5))
ax = sns.countplot(x="department", data=df)
ax.set_title("Department Distribution (n=100)")
ax.set_xlabel("Department")
ax.set_ylabel("Count")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

# Convert matplotlib figure to interactive HTML with mpld3
chart_html = mpld3.fig_to_html(plt.gcf())
plt.close()

# ------------- 4) Embed code + visualization into a single HTML file -------------
with open(__file__, "r", encoding="utf-8") as f:
    code_text = f.read()

html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Employee Performance Visualization</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body {{ font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 24px; }}
    pre {{ background:#f6f8fa; padding:16px; border-radius:8px; overflow:auto; }}
    .meta {{ color:#555; margin-bottom:16px; }}
    .section-title {{ margin-top: 24px; }}
  </style>
</head>
<body>
  <h1>Employee Performance Visualization</h1>
  <div class="meta">
    Contact: <strong>24f2005847@ds.study.iitm.ac.in</strong><br/>
    This page includes the Python code and the generated visualization.
  </div>

  <h2 class="section-title">Visualization: Department Distribution</h2>
  {chart_html}

  <h2 class="section-title">Python Code</h2>
  <pre><code>{textwrap.dedent(code_text)}</code></pre>
</body>
</html>
"""

with open("report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved HTML to report.html")
