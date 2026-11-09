import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

def main():
    # print("Hello from boot-ai-agent!")
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None: 
        raise RuntimeError("API key failed to load")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt
    verbose = args.verbose

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    final_response = ""
    for _ in range(20):
            
        response = client.chat.completions.create(
            model="openrouter/free",
            tools=available_functions,
            messages=messages,
        )
        if response.usage is None:
            raise RuntimeError("response.Usage is not present")
        message = response.choices[0].message
        # First append message
        messages.append(message)
        print(message.content)
        # Append each tool call
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                # print(f"Calling function: {tool_call.function.name}({function_args})")
                result_message = call_function(tool_call, verbose)
                # print(result_message)
                if result_message["content"] == "":
                    raise Exception("Content should be non empty")
                if verbose:
                    print(f"-> {result_message['content']}")
                # print("content:", result_message['content'])
                messages.append(result_message)
        else:
            print(message.content)
            final_response = message.content
            break

        if args.verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            print("Response:")
    if final_response == "":
        print("The agent could not reach a final response")
        os._exit(1)

if __name__ == "__main__":
    main()
