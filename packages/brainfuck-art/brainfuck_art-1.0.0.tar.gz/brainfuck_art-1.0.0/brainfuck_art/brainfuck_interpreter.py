
__all__ = ["execute_bf"]

def execute_bf(code: str, initial_memory_size: int = 3, max_ops: int = 10000, max_number: int = 256) -> tuple[str, list[int]]:
    """
    A Brainfuck interpreter that executes the given code.
    
    :param code: A string containing Brainfuck code.
    :param initial_memory_size: Initial size of the memory tape.
    :param max_ops: Maximum number of operations allowed.
    :return: A tuple containing the output produced by the Brainfuck code and the truncated memory tape.
    """
    memory = [0] * initial_memory_size  # Memory tape initialized to the given size
    pointer = 0  # Memory pointer
    max_pointer = 0  # Track the farthest right position accessed in memory
    code_pointer = 0  # Code pointer
    ops_count = 0  # Operation count
    output = []  # Collected output
    code_length = len(code)
    loop_stack = []

    while code_pointer < code_length:
        if ops_count >= max_ops:
            raise RuntimeError("Exceeded maximum operations limit.")

        command = code[code_pointer]
        ops_count += 1

        if command == '>':
            pointer += 1
            if pointer >= len(memory):
                memory.extend([0] * initial_memory_size)
            max_pointer = max(max_pointer, pointer)
        elif command == '<':
            if pointer == 0:
                raise RuntimeError("Memory pointer moved to a negative index.")
            pointer -= 1
        elif command == '+':
            memory[pointer] = (memory[pointer] + 1) % max_number
        elif command == '-':
            memory[pointer] = (memory[pointer] - 1) % max_number
        elif command == '.':
            output.append(chr(memory[pointer]))
        elif command == '[':
            if memory[pointer] == 0:
                open_brackets = 1
                while open_brackets != 0:
                    code_pointer += 1
                    if code[code_pointer] == '[':
                        open_brackets += 1
                    elif code[code_pointer] == ']':
                        open_brackets -= 1
            else:
                loop_stack.append(code_pointer)
        elif command == ']':
            if memory[pointer] != 0:
                code_pointer = loop_stack[-1]
            else:
                loop_stack.pop()

        code_pointer += 1
    
    # Truncate the memory up to the max_pointer
    truncated_memory = memory[:max_pointer + 1]  

    return ''.join(output), truncated_memory