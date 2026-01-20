"""
Normalize ExifTool metadata into a consistent JSON schema.
Preserves all tags and values, does not filter or drop unknowns.
"""

def normalize_metadata(metadata):
    """
    Accepts ExifTool JSON output (list of dicts), returns normalized dict.
    """
    if not metadata or not isinstance(metadata, list):
        return {}
    # ExifTool -j -a -u -g1 returns a list, usually with one dict per file
    # We flatten groupings, preserve all tags
    result = {}
    for entry in metadata:
        for k, v in entry.items():
            if k not in result:
                result[k] = v
            else:
                # If duplicate, store as list
                if not isinstance(result[k], list):
                    result[k] = [result[k]]
                result[k].append(v)
    return result
