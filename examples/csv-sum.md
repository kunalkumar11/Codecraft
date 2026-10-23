# CSV Sum

**Task:** "Write Python code that reads sales.csv and sums the 'amount' column."

Adapted from an upstream benchmark comparison, Claude Haiku 4.5, no-skill arm vs Ponytail arm, temperature 1. The short example below adds safe file cleanup; it is not a verbatim benchmark output. Reproduce the original benchmark with `npx promptfoo@latest eval -c benchmarks/promptfooconfig.yaml`.

This is an inherited benchmark illustration, not a current project recommendation. For an ordinary CSV sum, the standard-library example is the smaller dependency-free option. Its file handling below uses a context manager so the file closes even if parsing fails.

## Without Ponytail, 20 lines of code

# Python code to read sales.csv and sum the 'amount' column

```python
import pandas as pd

# Read the CSV file
df = pd.read_csv('sales.csv')

# Sum the 'amount' column
total_amount = df['amount'].sum()

# Print the result
print(f"Total amount: ${total_amount:,.2f}")
```

## Alternative methods:

**Using CSV module (without pandas):**
```python
import csv

with open('sales.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    total_amount = sum(float(row['amount']) for row in reader)

print(f"Total amount: ${total_amount:,.2f}")
```

**Using pandas with error handling:**
```python
import pandas as pd

try:
    df = pd.read_csv('sales.csv')
    total_amount = df['amount'].sum()
    print(f"Total amount: ${total_amount:,.2f}")
except FileNotFoundError:
    print("Error: sales.csv not found")
except KeyError:
    print("Error: 'amount' column not found")
```

Pandas is useful when a project already depends on it or needs broader data-analysis features. For one CSV sum, the standard library avoids a new dependency; either implementation still needs explicit validation when malformed rows or missing columns are expected.

## With CodeCraft, explicit file handling

```python
import csv

with open('sales.csv', newline='', encoding='utf-8') as file:
    total = sum(float(row['amount']) for row in csv.DictReader(file))

print(total)
```

Skipped: pandas and explicit malformed-row handling. Add validation when the CSV is not trusted or needs broader analysis.

**20 → 4 lines of code**, same task, with explicit file cleanup.
