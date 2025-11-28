from groq import Groq

client = Groq(api_key="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")  # Attach your API key here

def generate_code(description, top, down, solution):
    output = ""  # Initialize an empty string to collect the output
    completion = client.chat.completions.create(
        model="qwen-2.5-32b",
        messages=[
            {
                "role": "system",
                "content": "Give the missing code only!response format should be <code: , Don't provide unnecessary explanations or extra information."
            },
            {
                "role": "user",
                "content": f'"Description section": "{description}", "top section": "{top}", "bottom section": "{down}", "solution section": "{solution}"'
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in completion:
        output += chunk.choices[0].delta.content or ""  # Append content to the output string
    
    return output  # Return the output


# Example function call
description = """Java-H001 Primitive Data Types/Operators/Conditional Flow Statements
continue statement

The continue statement skips the remaining statements in the current iteration of a for, while, or do-while loop.
In the below program we use continue statement to print only the even numbers from 1 to 10.

public class Hello {

    public static void main(String[] args) {
       for(int counter=1;counter<=10;counter++){
           if(counter%2 == 1){
               //DO NOT PRINT ODD NUMBERS
               continue;
           }
           
           System.out.println(counter);
       }
    }
}

ProgramID- 71
SKILLRACK

continue statement

Use continue statement in the program below to ensure only the numbers divisible by 5 from 1 to 25 are printed.
"""

top = """public class Hello {

    public static void main(String[] args) {
        for (int counter = 1; counter <= 25; counter++) {
"""

down = """


         System.out.println(counter);
        }
    }
}"""

solution = """if (counter % 5 != 0) {
    continue;
}"""

# Get the generated code and store it in a variable
generated_code = generate_code(description, top, down, solution)
print(generated_code)  # Output the returned result
