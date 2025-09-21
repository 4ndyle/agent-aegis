import os 
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    working_directory_abs_path = os.path.abspath(working_directory)
    full_abs_path = os.path.abspath(full_path)    
    
    if not full_abs_path.startswith(working_directory_abs_path):
        return f"Error: Cannot write to '{file_path} as it is outside the permitted working directory"
    
    try:         
        directory_name = os.path.dirname(full_abs_path)
        
        # create file_path if it does not exist 
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            
        # overwrite into the file 
        with open(full_abs_path, "w") as f:
            f.write(content)
            
        return f"Successfully wrote to '{file_path}' ({len(content)} characters written)"
        
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Write content to the file that is specified.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be written to. If file does not exist, no file will be written to."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file spceificed as file_path."
            )
        }
    )
)