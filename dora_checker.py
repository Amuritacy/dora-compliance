"""
DORA Compliance Checker
Digital Operational Resilience Act (EU 2022/2554)
Maps ICT risk management practices against DORA requirements.

Author: Amra Gadzo | github.com/Amuritacy
"""

import csv
import os
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional


# ─── DORA Framework ──────────────────────────────────────────────────────────

DORA_REQUIREMENTS = {
    "Chapter II — ICT Risk Management (Art. 5-16)": {
        "Art. 5 — Governance & Organisation": [
            "Management body accountable for ICT risk",
            "ICT risk management framework approved by management body",
            "Annual review of ICT risk management framework",
            "Dedicated ICT risk management function",
            "Clear roles and responsibilities for ICT",
        ],
        "Art. 6 — ICT Risk Management Framework": [
            "ICT risk management policy documented",
            "ICT risk appetite formally defined",
            "ICT risk management integrated into overall risk framework",
            "Business continuity strategy for ICT",
            "ICT risk tolerance limits established",
        ],
        "Art. 8 — Identification": [
            "ICT asset inventory (hardware, software, data)",
            "Business functions mapped to ICT assets",
            "ICT dependencies and interconnections mapped",
            "Identification of single points of failure",
            "Annual ICT risk assessment conducted",
        ],
        "Art. 9 — Protection & Prevention": [
            "Information security policies implemented",
            "Network segmentation and access controls",
            "Data encryption at rest and in transit",
            "Patch and vulnerability management process",
            "ICT change management procedures",
            "Physical and environmental security controls",
        ],
        "Art. 10 — Detection": [
            "ICT-related incident detection mechanisms",
            "Automated alerting for anomalous activity",
            "Log management and monitoring in place",
            "Threat intelligence processes",
        ],
        "Art. 11 — Response & Recovery": [
            "ICT Business Continuity Plan (BCP) documented",
            "ICT Disaster Recovery Plan (DRP) documented",
            "BCP/DRP tested at least annually",
            "RTO and RPO defined for critical functions",
            "Crisis communication procedures",
            "Post-incident review process",
        ],
        "Art. 12 — Backup Policies": [
            "ICT backup policy documented",
            "Backup frequency aligned with criticality",
            "Backup restoration testing conducted",
            "Geographically separated backup storage",
        ],
        "Art. 13 — Learning & Evolving": [
            "Post-incident lessons learned process",
            "Threat intelligence sharing with peers",
            "ICT risk awareness training programme",
            "Annual cybersecurity training for staff",
        ],
        "Art. 14 — Communication": [
            "Internal ICT incident communication plan",
            "External stakeholder communication protocols",
            "Crisis communication testing conducted",
        ],
    },
    "Chapter III — ICT-Related Incident Reporting (Art. 17-23)": {
        "Art. 17 — Incident Classification": [
            "ICT incident classification methodology",
            "Major incident criteria defined",
            "Incident register maintained",
        ],
        "Art. 19 — Reporting Obligations": [
            "Initial notification process (within 4 hours for major incidents)",
            "Intermediate report capability (within 72 hours)",
            "Final report capability (within 1 month)",
            "Designated competent authority for reporting",
        ],
        "Art. 20 — Harmonised Reporting": [
            "Reporting templates aligned with regulatory standards",
            "Centralised incident reporting function",
        ],
    },
    "Chapter IV — Digital Operational Resilience Testing (Art. 24-27)": {
        "Art. 24 — General Requirements": [
            "Resilience testing programme established",
            "Testing covers critical ICT systems",
            "Annual basic testing (vulnerability assessments)",
        ],
        "Art. 26 — TLPT (Significant institutions)": [
            "Threat-Led Penetration Testing (TLPT) programme",
            "TLPT conducted every 3 years",
            "TLPT results shared with competent authority",
        ],
        "Art. 25 — Testing of ICT Tools": [
            "Network security testing",
            "Physical security reviews",
            "Source code reviews (where applicable)",
            "Scenario-based testing",
            "Compatibility testing after changes",
        ],
    },
    "Chapter V — ICT Third-Party Risk (Art. 28-44)": {
        "Art. 28 — General Principles": [
            "ICT third-party risk policy documented",
            "Register of ICT third-party providers maintained",
            "Pre-contract due diligence process",
            "Concentration risk assessment",
        ],
        "Art. 30 — Contractual Provisions": [
            "Audit rights in ICT contracts",
            "Exit strategy and termination clauses",
            "Data security and access provisions",
            "Incident notification obligations for providers",
            "Sub-outsourcing provisions and oversight",
            "SLA definitions and performance monitoring",
        ],
        "Art. 29 — Preliminary Assessment": [
            "Criticality assessment of ICT services",
            "Alternative providers identified for critical services",
            "Business impact analysis for third-party failure",
        ],
    },
    "Chapter VI — Information Sharing (Art. 45)": {
        "Art. 45 — Cyber Threat Information Sharing": [
            "Participation in information-sharing arrangements",
            "Cyber threat intelligence sharing policy",
        ],
    },
}

# ─── Sample entity disclosure data ───────────────────────────────────────────

SAMPLE_ENTITY = {
    "name": "Example Financial AG",
    "type": "Credit Institution",
    "significant_institution": True,
    "assessment_date": str(date.today()),
}

# (implemented: bool, maturity: 0-3, evidence, gap_description)
# Maturity: 0=Not implemented, 1=Ad hoc, 2=Defined, 3=Optimised
SAMPLE_CONTROLS = {
    "Management body accountable for ICT risk":           (True,  3, "Board-level CISO", ""),
    "ICT risk management framework approved by management body": (True, 2, "Approved 2023", "Annual review not documented"),
    "Annual review of ICT risk management framework":     (False, 0, "", "No review cycle established"),
    "Dedicated ICT risk management function":             (True,  2, "ICT Risk team exists", ""),
    "Clear roles and responsibilities for ICT":           (True,  2, "RACI matrix in place", "Not fully updated"),
    "ICT risk management policy documented":              (True,  2, "Policy v2.1", ""),
    "ICT risk appetite formally defined":                 (True,  1, "High-level only", "No quantitative limits"),
    "ICT risk management integrated into overall risk framework": (True, 2, "Partial integration", ""),
    "Business continuity strategy for ICT":               (True,  2, "BCS documented", ""),
    "ICT risk tolerance limits established":              (False, 0, "", "Not yet defined"),
    "ICT asset inventory (hardware, software, data)":     (True,  2, "CMDB in place", "Software inventory incomplete"),
    "Business functions mapped to ICT assets":            (True,  1, "Partial mapping", "Critical functions only"),
    "ICT dependencies and interconnections mapped":       (False, 0, "", "Dependency mapping not conducted"),
    "Identification of single points of failure":         (False, 0, "", "SPOF analysis pending"),
    "Annual ICT risk assessment conducted":               (True,  2, "Completed Q4 2024", ""),
    "Information security policies implemented":          (True,  3, "ISO 27001 aligned", ""),
    "Network segmentation and access controls":           (True,  3, "Zero-trust in progress", ""),
    "Data encryption at rest and in transit":             (True,  3, "AES-256 / TLS 1.3", ""),
    "Patch and vulnerability management process":         (True,  2, "Monthly cycle", "Critical patches: 14-day SLA"),
    "ICT change management procedures":                   (True,  2, "ITIL-based CAB process", ""),
    "Physical and environmental security controls":       (True,  3, "Tier 3 DC standards", ""),
    "ICT-related incident detection mechanisms":          (True,  2, "SIEM deployed", "Coverage gaps in legacy systems"),
    "Automated alerting for anomalous activity":          (True,  2, "UEBA tools in use", ""),
    "Log management and monitoring in place":             (True,  2, "12-month retention", ""),
    "Threat intelligence processes":                      (True,  1, "Ad hoc subscriptions", "No formal TI programme"),
    "ICT Business Continuity Plan (BCP) documented":      (True,  2, "BCP v3.0", ""),
    "ICT Disaster Recovery Plan (DRP) documented":        (True,  2, "DRP v2.0", ""),
    "BCP/DRP tested at least annually":                   (True,  2, "Tested Oct 2024", "Partial test — not full DR"),
    "RTO and RPO defined for critical functions":         (True,  3, "Defined per system tier", ""),
    "Crisis communication procedures":                    (True,  1, "Informal only", "No documented procedures"),
    "Post-incident review process":                       (True,  2, "PIR template in use", ""),
    "ICT backup policy documented":                       (True,  3, "Policy v1.5", ""),
    "Backup frequency aligned with criticality":          (True,  3, "Tiered: hourly to daily", ""),
    "Backup restoration testing conducted":               (True,  2, "Tested quarterly", ""),
    "Geographically separated backup storage":            (True,  3, "Two data centres, 50km apart", ""),
    "Post-incident lessons learned process":              (True,  1, "Informal debrief only", "No tracking of actions"),
    "Threat intelligence sharing with peers":             (False, 0, "", "No participation in sharing groups"),
    "ICT risk awareness training programme":              (True,  2, "Annual e-learning", ""),
    "Annual cybersecurity training for staff":            (True,  2, "Phishing simulations run", ""),
    "Internal ICT incident communication plan":           (True,  2, "Escalation matrix defined", ""),
    "External stakeholder communication protocols":       (False, 0, "", "Not documented"),
    "Crisis communication testing conducted":             (False, 0, "", "Never tested"),
    "ICT incident classification methodology":            (True,  2, "Classification matrix exists", ""),
    "Major incident criteria defined":                    (True,  2, "Aligned with DORA Article 18", ""),
    "Incident register maintained":                       (True,  3, "Ticketing system with full audit trail", ""),
    "Initial notification process (within 4 hours for major incidents)": (True, 1, "Process drafted", "Not yet tested"),
    "Intermediate report capability (within 72 hours)":   (False, 0, "", "Template not created"),
    "Final report capability (within 1 month)":           (False, 0, "", "Template not created"),
    "Designated competent authority for reporting":       (True,  2, "FMA identified", ""),
    "Reporting templates aligned with regulatory standards": (False, 0, "", "Pending EBA template adoption"),
    "Centralised incident reporting function":            (True,  1, "Ad hoc — no dedicated function", ""),
    "Resilience testing programme established":           (True,  1, "Ad hoc testing only", "No formal programme"),
    "Testing covers critical ICT systems":                (True,  1, "Partial coverage", ""),
    "Annual basic testing (vulnerability assessments)":   (True,  2, "Conducted by external party", ""),
    "Threat-Led Penetration Testing (TLPT) programme":   (False, 0, "", "Not yet initiated"),
    "TLPT conducted every 3 years":                       (False, 0, "", "N/A — TLPT not started"),
    "TLPT results shared with competent authority":       (False, 0, "", "N/A"),
    "Network security testing":                           (True,  2, "Annual penetration test", ""),
    "Physical security reviews":                          (True,  2, "Annual review", ""),
    "Source code reviews (where applicable)":             (True,  1, "Ad hoc only", "No SAST tooling"),
    "Scenario-based testing":                             (False, 0, "", "Not conducted"),
    "Compatibility testing after changes":                (True,  2, "Part of change process", ""),
    "ICT third-party risk policy documented":             (True,  2, "Policy v1.0", "Needs DORA-specific update"),
    "Register of ICT third-party providers maintained":   (True,  2, "Register exists", "Criticality ratings incomplete"),
    "Pre-contract due diligence process":                 (True,  2, "Vendor assessment questionnaire", ""),
    "Concentration risk assessment":                      (False, 0, "", "Never conducted"),
    "Audit rights in ICT contracts":                      (True,  2, "Included in standard contracts", "Older contracts need review"),
    "Exit strategy and termination clauses":              (True,  1, "Basic clauses only", "No tested exit plans"),
    "Data security and access provisions":                (True,  3, "Standard data processing agreement", ""),
    "Incident notification obligations for providers":    (True,  1, "Referenced but not detailed", ""),
    "Sub-outsourcing provisions and oversight":           (False, 0, "", "Not addressed in contracts"),
    "SLA definitions and performance monitoring":         (True,  2, "SLAs defined for critical providers", ""),
    "Criticality assessment of ICT services":             (True,  1, "Initial assessment done", "Not reviewed recently"),
    "Alternative providers identified for critical services": (False, 0, "", "Not completed"),
    "Business impact analysis for third-party failure":   (False, 0, "", "Not conducted"),
    "Participation in information-sharing arrangements":  (False, 0, "", "No participation"),
    "Cyber threat intelligence sharing policy":           (False, 0, "", "No policy"),
}

MATURITY_LABELS = {
    0: "Not Implemented",
    1: "Ad Hoc",
    2: "Defined",
    3: "Optimised",
}


# ─── Analysis ─────────────────────────────────────────────────────────────────

@dataclass
class ControlItem:
    article: str
    chapter: str
    requirement: str
    implemented: bool
    maturity: int
    maturity_label: str
    evidence: str
    gap: str
    priority: str

    @property
    def maturity_pct(self) -> float:
        return round((self.maturity / 3) * 100, 1)


@dataclass
class ChapterResult:
    chapter: str
    controls: List[ControlItem] = field(default_factory=list)

    @property
    def implementation_rate(self) -> float:
        if not self.controls:
            return 0.0
        return round(sum(1 for c in self.controls if c.implemented) / len(self.controls) * 100, 1)

    @property
    def avg_maturity(self) -> float:
        if not self.controls:
            return 0.0
        return round(sum(c.maturity for c in self.controls) / (len(self.controls) * 3) * 100, 1)

    @property
    def gaps(self) -> List[ControlItem]:
        return [c for c in self.controls if not c.implemented or c.maturity < 2]


def _priority(implemented: bool, maturity: int) -> str:
    if not implemented:
        return "Critical"
    if maturity == 1:
        return "High"
    return "Medium"


def run_dora_analysis(controls: dict) -> Dict[str, ChapterResult]:
    results = {}

    for chapter, articles in DORA_REQUIREMENTS.items():
        chapter_result = ChapterResult(chapter=chapter)

        for article, requirements in articles.items():
            for req in requirements:
                if req in controls:
                    implemented, maturity, evidence, gap = controls[req]
                else:
                    implemented, maturity, evidence, gap = False, 0, "", "Control not assessed"

                control = ControlItem(
                    article=article,
                    chapter=chapter,
                    requirement=req,
                    implemented=implemented,
                    maturity=maturity,
                    maturity_label=MATURITY_LABELS[maturity],
                    evidence=evidence,
                    gap=gap,
                    priority=_priority(implemented, maturity),
                )
                chapter_result.controls.append(control)

        results[chapter] = chapter_result

    return results


def generate_dora_report(
    results: Dict[str, ChapterResult],
    entity: dict,
    output_dir: str = "outputs",
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    today = date.today()
    filepath = os.path.join(output_dir, f"dora_compliance_{today}.txt")

    all_controls = [c for r in results.values() for c in r.controls]
    total = len(all_controls)
    implemented = sum(1 for c in all_controls if c.implemented)
    critical = [c for c in all_controls if c.priority == "Critical"]

    with open(filepath, "w", encoding="utf-8") as f:
        w = lambda s="": f.write(s + "\n")

        w("=" * 72)
        w("  DORA COMPLIANCE ASSESSMENT")
        w(f"  {entity['name']}  |  {entity['type']}")
        w(f"  Assessment date: {entity['assessment_date']}")
        w("=" * 72)
        w()
        w(f"  Total controls assessed:  {total}")
        w(f"  Controls implemented:     {implemented} ({implemented/total*100:.1f}%)")
        w(f"  Critical gaps:            {len(critical)}")
        w()

        w("CHAPTER SUMMARY")
        w("-" * 72)
        w(f"{'Chapter':<50} {'Impl.':>7} {'Maturity':>9} {'Gaps':>6}")
        w("-" * 72)
        for name, result in results.items():
            short = name[:48]
            w(f"  {short:<48} {result.implementation_rate:>6.1f}% {result.avg_maturity:>8.1f}% {len(result.gaps):>6}")
        w()

        for name, result in results.items():
            w()
            w("─" * 72)
            w(f"  {name}")
            w("─" * 72)
            for control in result.controls:
                status = "✓" if control.implemented else "✗"
                w(f"  {status} [{control.maturity_label}] {control.requirement}")
                if control.gap:
                    w(f"       Gap: {control.gap}")
            w()

        w()
        w("=" * 72)
        w("  CRITICAL GAPS — IMMEDIATE REMEDIATION REQUIRED")
        w("=" * 72)
        for i, c in enumerate(critical, 1):
            w(f"  {i:>2}. {c.requirement}")
            w(f"      Article: {c.article}")
            if c.gap:
                w(f"      Gap:     {c.gap}")
            w()

        w("─" * 72)
        w("DORA Compliance Checker | github.com/Amuritacy")
        w("─" * 72)

    return filepath


def generate_dora_csv(results: Dict[str, ChapterResult], output_dir: str = "outputs") -> str:
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"dora_compliance_{date.today()}.csv")

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Chapter", "Article", "Requirement", "Implemented",
            "Maturity (0-3)", "Maturity Label", "Maturity (%)",
            "Priority", "Evidence", "Gap Description",
        ])
        writer.writeheader()
        for chapter, result in results.items():
            for c in result.controls:
                writer.writerow({
                    "Chapter":          chapter,
                    "Article":          c.article,
                    "Requirement":      c.requirement,
                    "Implemented":      "Yes" if c.implemented else "No",
                    "Maturity (0-3)":   c.maturity,
                    "Maturity Label":   c.maturity_label,
                    "Maturity (%)":     c.maturity_pct,
                    "Priority":         c.priority,
                    "Evidence":         c.evidence,
                    "Gap Description":  c.gap,
                })

    return filepath


def print_dora_summary(results: Dict[str, ChapterResult], entity_name: str) -> None:
    all_controls = [c for r in results.values() for c in r.controls]
    total = len(all_controls)
    implemented = sum(1 for c in all_controls if c.implemented)
    critical = [c for c in all_controls if c.priority == "Critical"]

    print("\n" + "=" * 60)
    print(f"  DORA COMPLIANCE — {entity_name.upper()}")
    print("=" * 60)
    print(f"  Implementation rate: {implemented}/{total} ({implemented/total*100:.1f}%)")
    print(f"  Critical gaps:       {len(critical)}")
    print()
    print("  Chapter Scores:")
    for name, result in results.items():
        short = name.split("(")[0].strip()
        bar = "█" * int(result.avg_maturity / 5) + "░" * (20 - int(result.avg_maturity / 5))
        print(f"    {short[:35]:<35} {bar} {result.avg_maturity:.1f}%")
    print()
    print("  Top Critical Gaps:")
    for c in critical[:5]:
        print(f"    ✗ {c.requirement}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    results = run_dora_analysis(SAMPLE_CONTROLS)
    print_dora_summary(results, SAMPLE_ENTITY["name"])
    csv_path = generate_dora_csv(results)
    report_path = generate_dora_report(results, SAMPLE_ENTITY)
    print(f"  CSV:    {csv_path}")
    print(f"  Report: {report_path}\n")
