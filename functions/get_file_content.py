import os

from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the contents of a file at the given file path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to list the contents of, relative to the working directory",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(path, file_path))
        valid_target_file = os.path.commonpath([path, full_path]) == path
        # print(path)
        # print(full_path)
        if not valid_target_file:
            # print(f'    Error: Cannot list "{file_path}" as it is outside the permitted working directory')
            return f'    Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(full_path):
            # print(f'    Error: "{directory}" is not a directory')
            return f'Error: File not found or is not a regular file: "{file_path}"'
        # Create file
        content = ""
        with open(full_path, "r") as f:
            content += f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
        # Read 10k characters
    except Exception as e:
            return f"Error: {e}"