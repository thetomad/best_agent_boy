"""
Document related tools. Those will be mainly used for general purpose documentation.

Later we might change this to encompese client-specific tools.

"""

import os


def read_internal_documents(
    directory: str = "./assistant/data/public", allowed_extensions=(".txt", ".md")
):
    """
    Function for reading internal documents.

    A function that will read from the internal documents and return all the information.
    The directory by default will be in the data section of the project.
    It is a testing tool function to be removed in later versions.

    Parameters
    ----------
    directory : str, default="../../data/public"
        Location of internal documents.
    allowed_extensions : tuple, default="(".txt", ".md")"
        Tuple of extensions allowed to be read by this function from the specified directory.

    Returns
    -------
    str
        Content of read files from specified directory with specific allowed extensions.

    Raises
    ------
    FileNotFoundError
        Raised when the directory specified does not exist or it is not a directory.

    """
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
