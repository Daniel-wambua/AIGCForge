from .base import Analyzer
import os
import json

# Load known AI vendor signatures
SIG_PATH = os.path.join(os.path.dirname(__file__), "..", "signatures", "ai_vendors.json")
try:
    with open(SIG_PATH, "r", encoding="utf-8") as f:
        AI_SIGNATURES = json.load(f)
except Exception:
    AI_SIGNATURES = {}

class AIMetadataAnalyzer(Analyzer):
    """
    Flags AI provenance based on explicit metadata evidence only.
    """
    def analyze(self, metadata, raw_findings):
        findings = []
        if not metadata:
            return findings
        for vendor, sigs in AI_SIGNATURES.items():
            evidence = []
            for tag, expected in sigs.get("tags", {}).items():
                if tag in metadata and (
                    (isinstance(expected, list) and metadata[tag] in expected) or
                    (isinstance(expected, str) and metadata[tag] == expected)
                ):
                    evidence.append(f"{tag}={metadata[tag]}")
            for block in sigs.get("blocks", []):
                if block in str(metadata):
                    evidence.append(f"{block} block found")
            if evidence:
                findings.append({
                    "type": "ai_metadata",
                    "confidence": "high",
                    "vendor": vendor,
                    "evidence": evidence
                })
        return findings
