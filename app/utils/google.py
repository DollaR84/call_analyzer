import re


def extract_folder_id(url_or_id: str) -> str:
    match = re.search(r'(?:folders|d)/([a-zA-Z0-9-_]+)', url_or_id)
    if match:
        return match.group(1)

    if re.match(r'^[a-zA-Z0-9-_]+$', url_or_id):
        return url_or_id

    raise ValueError(f"Incorrect Google Folder ID or link format: '{url_or_id}'")
