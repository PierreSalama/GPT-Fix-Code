import sys
import subprocess
from subprocess import TimeoutExpired
import openai

openai.api_key = "ur open ai's api key"

def run_code(file_name):
    try:
        output = subprocess.check_output(["python", file_name], stderr=subprocess.STDOUT, text=True)
        return output, None
    except subprocess.CalledProcessError as e:
        return e.output, e
    except TimeoutExpired as e:
        return "The code took too long to execute and was terminated.", e

def send_to_gpt(file_content, error_message):
    prompt = f"fix this code and print out the full code:\n\n```python\n{file_content}```\n\nError message:\n{error_message}\n\nSuggested fix:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def main():
    if len(sys.argv) != 2:
        print("Usage: python fix_code.py <file_name>")
        exit(1)

    file_name = sys.argv[1]

    while True:
        output, error = run_code(file_name)

        if error is None:
            print("Code ran successfully:")
            print(output)
            break
        else:
            print("Error encountered:")
            print(error.output)

            with open(file_name, "r") as f:
                file_content = f.read()

            suggestion = send_to_gpt(file_content, error.output)

            print("Applying GPT suggestion:")
            print(suggestion)

            with open(file_name, "w") as f:
                f.write(suggestion)

if __name__ == "__main__":
    main()
