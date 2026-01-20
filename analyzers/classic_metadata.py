from .base import Analyzer

class ClassicMetadataAnalyzer(Analyzer):
    """
    Extracts classic metadata evidence: camera, timestamps, software, etc.
    """
    def analyze(self, metadata, raw_findings):
        findings = []
        if not metadata:
            return findings
        # Camera make/model
        for tag in ("Make", "Model", "CameraModelName"):
            if tag in metadata:
                findings.append({
                    "type": "classic_metadata",
                    "field": tag,
                    "value": metadata[tag]
                })
        # Timestamps
        for tag in ("CreateDate", "ModifyDate", "DateTimeOriginal"):
            if tag in metadata:
                findings.append({
                    "type": "classic_metadata",
                    "field": tag,
                    "value": metadata[tag]
                })
        # Software
        for tag in ("Software", "ProcessingSoftware", "ApplicationRecordVersion"):
            if tag in metadata:
                findings.append({
                    "type": "classic_metadata",
                    "field": tag,
                    "value": metadata[tag]
                })
        return findings
