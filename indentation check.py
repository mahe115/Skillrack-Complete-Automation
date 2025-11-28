def fix_indentation(text):
    lines = text.splitlines()
    corrected_lines = []
    base_indent = None  # Track the base indentation level
    current_function_indent = None  # Track indentation of the current function

    for line in lines:
        if not line.strip():  
            corrected_lines.append("")  # Preserve blank lines
            continue

        leading_spaces = len(line) - len(line.lstrip())  # Measure leading spaces
        stripped = line.lstrip()

        # Detect the base indentation level from the first non-empty line
        if base_indent is None:
            base_indent = leading_spaces

        # If a function starts, reset indentation and store its level
        if stripped.startswith(("def ", "class ")):
            current_function_indent = base_indent  # Functions start at base level
            corrected_lines.append(" " * base_indent + stripped)
        elif stripped.startswith(("for ", "while ", "if ", "elif ", "else:")):
            corrected_lines.append(" " * current_function_indent + stripped)
        else:
            # If inside a function, keep relative indentation
            if current_function_indent is not None and leading_spaces > current_function_indent:
                corrected_lines.append(" " * leading_spaces + stripped)
            else:
                # Outermost level statements stay aligned to base level
                corrected_lines.append(" " * base_indent + stripped)

    return "\n".join(corrected_lines)

# Define the test cases
test_cases = {
    "Test 1: Simple Functions": """  
def func1():
    print("Hello, World!")

def func2():
    print("Goodbye, World!")

func1()
func2()
""",
    "Test 2: Misaligned Function Definitions": """  
def func1():
    print("Hello, World!")

    def func2():
        print("Goodbye, World!")

    func2()

func1()
""",
    "Test 3: Function with If Statement": """  
def func1():
    print("Hello, World!")
    x = 10
if x > 5:
        print("x is large")

def func2():
    print("Goodbye, World!")
    x = 100  
    print(x)

func1()
func2()
""",
    "Test 4: Loop Inside Function": """  
def loop_example():
    for i in range(5):
        print(i)

    while i < 10:
        print("Still in loop")
        i += 1

print("This is outside the function")
loop_example()
""",
    "Test 5: Mixed Functions and Statements": """  
x = 50  # Should remain outside

def func1():
    print("Inside func1")
    y = 20

def func2():
    print("Inside func2")
    if y > 10:
        print("Y is large")

print("Standalone print")
func1()
func2()
"""
}

# Run the tests
test_results = {name: fix_indentation(code) for name, code in test_cases.items()}
test_results
