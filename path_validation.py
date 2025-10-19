import os 

def validate_path(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    working_directory_abs_path = os.path.abspath(working_directory)
    full_abs_path = os.path.abspath(full_path)
    
    if not full_abs_path.startswith(working_directory_abs_path):
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
    
    if not os.path.isfile(full_abs_path):
        return f"Error: File not found or is not a regular file: '{file_path}'"