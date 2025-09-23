import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

def main():
    print("Hello from agent-41!")
    
    # check if prompt is provided 
    user_prompt = ""
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Write or overwrite files
    - Execute Python files with optional arguments

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    containsVerbose = "--verbose" in sys.argv
    
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else:
        print("Prompt cannot be empty. Please provide a prompt after the script")
        print("Example: How can I improve my skills in python")
        sys.exit(1)
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    if containsVerbose:
        print(f"User prompt: {user_prompt}")
    
    # load api key 
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # get list of available functions the LLM can use 
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    client = genai.Client(api_key=api_key)
    generate_content(client, messages, system_prompt, containsVerbose, available_functions)

def generate_content(client, messages, system_prompt, containsVerbose, available_functions):
    prompt_answer = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        )
    )
    
    if containsVerbose:
        print(f"Prompt tokens: {prompt_answer.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {prompt_answer.usage_metadata.candidates_token_count}")
    
    function_call_part = prompt_answer.function_calls
    
    if function_call_part:
        for function_call in function_call_part:
            # print(function_call_part)
            res = call_function(function_call, containsVerbose)
            
            if not res.parts[0].function_response.response:
                Exception("No Response from Agent found.")
            else:
                if containsVerbose:
                    print(f"-> {res.parts[0].function_response.response}")
    else:
        print("Response: ")
        print(prompt_answer.text)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    # determine the correct function to use
    functionDict = {
        "get_file_content" : get_file_content,
        "get_files_info" : get_files_info,
        "run_python_file" : run_python_file,
        "write_file" : write_file
    }
    
    if function_call_part.name in functionDict:
        function_to_use = functionDict[function_call_part.name]
        
        # add default working directory of ./calculator to args (which is a dict)
        function_call_part.args["working_directory"] = "./calculator"
        
        res = function_to_use(**function_call_part.args)
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": res},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

if __name__ == "__main__":
    main()
