from groq import Groq

client = Groq(api_key="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")  # Attach your API key here




def generate_code(description, top, down, solution,language):
    Ai_solution = ""  # Initialize an empty string to collect the output
    completion = client.chat.completions.create(
        model="qwen-2.5-32b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Return **only** the missing lines of code. "
                    "Do NOT include explanations, comments, or unnecessary formatting. "
                    "Do NOT include already provided code. "
                    "Do NOT wrap the response in triple quotes, brackets, or special characters. "
                    "The response should contain **only the required missing lines** as they should appear in the program."
                ),
            },
            {
                "role": "user",
                "content": f'Programming Language: {language}\n'
                           f'Description section: {description}\n'
                           f'Top section: {top}\n'
                           f'Bottom section: {down}\n'
                           f'Solution section: {solution}\n'
                           f'**Provide ONLY the missing code lines as the exact output. No extra words or formatting.**'
            }
        ],
        temperature=0.5,
        max_completion_tokens=2024,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in completion:
        Ai_solution += chunk.choices[0].delta.content or ""  # Append content to the output string

    Ai_solution = "\n".join(line.lstrip() for line in Ai_solution.split("\n"))
    return Ai_solution  # Return the output

