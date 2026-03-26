# ESG Regulatory Gap Analysis Tool

Maps corporate ESG disclosures against three major EU regulatory frameworks — **CSRD**, **EU Taxonomy**, and **SFDR** — and produces prioritised gap analysis reports.

## Frameworks Covered

| Framework | Scope | Key Output |
|-----------|-------|------------|
| **CSRD** (EU 2022/2464) | All ESRS topics (E1–E5, S1–S4, G1) | Disclosure rate, quality score by ESRS topic |
| **EU Taxonomy** (EU 2020/852) | 6 environmental objectives, KPI metrics | Taxonomy-alignment gaps by objective |
| **SFDR** (EU 2019/2088) | Entity-level + 14 mandatory PAI indicators | PAI coverage and quality |

## Features

- Scores each disclosure on a **0–3 quality scale** (Missing → Best Practice)
- Prioritises gaps as **Critical / High / Medium**
- Exports structured **CSV** for Power BI / Excel analysis
- Generates a formatted **executive text report**

## Usage

```bash
# Install dependencies (none beyond stdlib)
python main.py

# With custom company name
python main.py --company "Your Company AG"
```

## Output

```
outputs/
  esg_gap_analysis_YYYY-MM-DD.csv   # Full gap register
reports/
  esg_report_YYYY-MM-DD.txt         # Executive summary report
```

## Adapting to Your Company

Edit `sample_data.py` to reflect your company's actual disclosures:

```python
CSRD_DISCLOSURES = {
    "GHG emissions (Scope 1, 2, 3)": (True, 2, "Scope 1&2 reported; Scope 3 partial"),
    #                                  ^disclosed ^quality(0-3) ^notes
}
```

## Project Structure

```
esg-gap-analysis/
├── main.py          # Entry point
├── frameworks.py    # CSRD / EU Taxonomy / SFDR requirement definitions
├── analyzer.py      # Gap scoring engine
├── reporter.py      # CSV and text report generation
└── sample_data.py   # Sample corporate disclosure data
```

---
*Author: Amra Gadzo · [LinkedIn](https://linkedin.com/in/amra-gadzo-98447533) · [GitHub](https://github.com/Amuritacy)*
