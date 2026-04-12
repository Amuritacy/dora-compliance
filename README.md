# DORA Compliance Checker

Assesses ICT risk management controls against the **Digital Operational Resilience Act** (EU 2022/2554), covering all five chapters and 77 individual requirements.

## Coverage

| Chapter | Article Range | Controls |
|---------|--------------|----------|
| ICT Risk Management | Art. 5–16 | 46 |
| ICT Incident Reporting | Art. 17–23 | 11 |
| Digital Resilience Testing | Art. 24–27 | 12 |
| ICT Third-Party Risk | Art. 28–44 | 16 |
| Information Sharing | Art. 45 | 2 |

## Maturity Scale

| Level | Label | Description |
|-------|-------|-------------|
| 0 | Not Implemented | No control in place |
| 1 | Ad Hoc | Exists informally, undocumented |
| 2 | Defined | Documented policy/process |
| 3 | Optimised | Regularly tested, improved, evidenced |

## Usage

```bash
python dora_checker.py
```

## Output

```
outputs/
  dora_compliance_YYYY-MM-DD.csv    # Full control register with evidence
  dora_compliance_YYYY-MM-DD.txt    # Executive report with gap analysis
```

## Adapting to Your Organisation

Edit the `SAMPLE_CONTROLS` dictionary in `dora_checker.py`:

```python
SAMPLE_CONTROLS = {
    "Management body accountable for ICT risk": (True, 3, "Board CISO appointed", ""),
    #                                            ^impl ^maturity ^evidence       ^gap
}
```

---
*Author: Amra Gadzo · [LinkedIn](https://linkedin.com/in/amra-gadzo-98447533) · [GitHub](https://github.com/Amuritacy)*/amra-gadzo-98447533) · [GitHub](https://github.com/Amuritacy)*
