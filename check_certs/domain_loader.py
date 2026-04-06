import json
from pathlib import Path


def load_domains(domains_file: Path) -> list[str]:
    try:
        with domains_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Domains file not found: {domains_file}")
        return []
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in domains file: {e}")
        return []

    if isinstance(data, dict):
        domains = data.get("domains", [])
    elif isinstance(data, list):
        domains = data
    else:
        print("Domains JSON must be a list or an object with a 'domains' list.")
        return []

    if not isinstance(domains, list):
        print("The 'domains' value must be a list.")
        return []

    cleaned_domains = [d.strip() for d in domains if isinstance(d, str) and d.strip()]
    if not cleaned_domains:
        print("No valid domains found in domains file.")
    return cleaned_domains
