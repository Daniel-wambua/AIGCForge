from .base import Analyzer

class RawContainerAnalyzer(Analyzer):
    """
    Scans raw byte findings for embedded JSON or AIGC markers.
    """
    def analyze(self, metadata, raw_findings):
        findings = []
        for item in raw_findings:
            if item.get("type") == "embedded_json":
                findings.append({
                    "type": "raw_embedded_json",
                    "json": item["json"]
                })
            elif item.get("type") == "raw_marker":
                findings.append({
                    "type": "raw_marker",
                    "marker": item["marker"]
                })
            elif item.get("type") == "error":
                findings.append({
                    "type": "scan_error",
                    "error": item["error"]
                })
        return findings
