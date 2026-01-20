class Analyzer:
    """
    Base interface for all analyzers.
    """
    def analyze(self, metadata, raw_findings):
        """
        Accepts normalized metadata and raw byte findings.
        Returns a list of evidence dicts.
        """
        raise NotImplementedError
