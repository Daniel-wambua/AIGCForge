import json
import os

def generate_json_report(results, outpath=None):
    """
    Write machine-readable JSON report.
    """
    report = {
        "tool": "AIGCForge",
        "version": "1.0",
        "limitations": [
            "AI provenance is based on explicit metadata evidence only.",
            "No probabilistic or ML-based detection is performed.",
            "Only supported vendors with known metadata are flagged."
        ],
        "results": results
    }
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
