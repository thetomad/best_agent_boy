import os 


def read_internal_documents(directory: str = "./info", allowed_extensions=(".txt", ".md")):
    directory = os.path.abspath(directory)

    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory does not exists: {directory}")
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Not a directory: {directory}")

    documents = {}

    for root, _, files in os.walk(directory):
        for filename in files:
            if not filename.endswith(allowed_extensions):
                continue

            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, directory)

            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                documents[relative_path] = f.read()

    return documents


# Tools - lista de tooluri folosite

TOOLS= [
        {
            "name": "read_internal_documents",
            "description": "Get form internal documents all information about the company."
        }
    ]


# Formatare dinamica a toolurilor
TOOLS_FORMATED = [
            {
                "type": "function",
                "function": {
                    "name": tool.get("name"),
                    "description": tool.get("description"),
                    "parameters": {
                        "type": "object",
                        "properties": tool.get("properties"),
                        "required": tool.get("required")
                    }
                }
            }
            for tool in TOOLS
        ]

# Implementarea toolurilor. 
TOOLS_IMPLS = {
        tool["function"].get("name"): globals()[tool["function"].get("name")]
        for tool in TOOLS_FORMATED
    }
