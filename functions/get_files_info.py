import os



schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
# Directory is relative path
# Working directly set by us
""" Verifies whether a requested directory is inside the
allowed working directory of the agent.
"""
def get_files_info(working_directory: str, directory: str = ".") -> str:
    dir_title = directory
    if dir_title == ".":
        dir_title = "current"
    else:
        dir_title = f"'{directory}'"
    print(f"Result for {dir_title} directory:")
    try:
        path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(path, directory))
        valid_target_dir = os.path.commonpath([path, full_path]) == path
        # print(valid_target_dir)
        # print(full_path)
        if not valid_target_dir:
            print(f'    Error: Cannot list "{directory}" as it is outside the permitted working directory')
            return f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            print(f'    Error: "{directory}" is not a directory')
            return f'Error: "{directory}" is not a directory'
        file_list = os.listdir(full_path)
        files = {}
        for i in file_list:
            files[i] = {
                "name" : i,
                "file_size" : os.path.getsize(full_path + "/" + i),
                "is_dir" : os.path.isdir(full_path + "/" + i)
            }
        result = ""
        for k in files:
            # print(k)
            # print(files[k])
            result += f"  - {k} file_size={files[k]["file_size"]} bytes, is_dir={files[k]["is_dir"]}\n"
        return result
        # Check wheether
    except Exception as e:
        return f"Error: {e}"