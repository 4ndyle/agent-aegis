import os
from config import max_chars
from path_validation import validate_path
from google.genai import types

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    working_directory_abs_path = os.path.abspath(working_directory)
    full_abs_path = os.path.abspath(full_path)
    
    if not full_abs_path.startswith(working_directory_abs_path):
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
    
    if not os.path.isfile(full_abs_path):
        return f"Error: File not found or is not a regular file: '{file_path}'"
    
    full_path = os.path.join(working_directory, file_path)
    full_abs_path = os.path.abspath(full_path)
    
    # read the contents of the file 
    try:
        with open(full_abs_path, "r") as f:
            file_contents = f.read(max_chars)
            
            if len(file_contents) > max_chars:
                file_contents += f"[...File '{file_path}' trauncated at 10000 characters]."
            
            return file_contents
    except Exception as error:
        return f"Error: {error}"
    
schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description="Read the content of a specific file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to list the contents of. If not provided, there will be no content listed since the file does not exist."
            )
        }
    )
)