import os
import subprocess
from openai import completions

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes using python the given python file at file_path with the give arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of the file to execute",
                },
                "args": {
                    "type": "list[string]",
                    "description": "List of arguments to the python file",
                },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        # Gets full path
        path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(path, file_path))
        valid_target_dir = os.path.commonpath([path, full_path]) == path
        # print("checking if valid target")
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        # print("checking if dir")
        # print(full_path)
        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", full_path]
        if args != None:
            command.extend(args)
        completed_process = subprocess.run(command, capture_output=True, timeout=30, text=True, cwd=path)
        output = ""
        if completed_process.returncode != 0:
            output += "Process exited with code " + completed_process.returncode + "\n"
        if completed_process.stdout == "" and completed_process.stderr == "":
            output += "No output produced\n"
        else:
            output += "STDOUT: " + completed_process.stdout
            output += "STDERR: " + completed_process.stderr
        return output
    except Exception as e:
        return f"Error: exectuting Python file: {e}"