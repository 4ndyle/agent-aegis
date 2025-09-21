import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content

def main():
    print("Hello from agent-41!")
    
    # check if prompt is provided 
    user_prompt = ""
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents

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
            schema_get_file_content
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
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print("Response: ")
        print(prompt_answer.text)


if __name__ == "__main__":
    main()
