import re

"""
INSTRUCTION -> /train PARAMS
         | /infer PARAMS
         | /share PARAMS

PARAMS -> --key=value PARAMS
        | ε
"""

class ParsedInstruction:
    def __init__(self, instruction_type, params):
        self.instruction_type = instruction_type
        self.params = params

    def isTrain(self):
        return self.instruction_type == "/train"

    def isInfer(self):
        return self.instruction_type == "/infer"

    def isShare(self):
        return self.instruction_type == "/share"
    
    def __str__(self):
        params_str = ", ".join(f"{key}={value}" for key, value in self.params.items())
        return f"Instruction Type: {self.instruction_type}, Parameters: {params_str}"

class InstructionParser:
    def __init__(self, instruction):
        self.instruction = instruction
        self.position = 0

    def parse(self):
        if self.instruction.startswith("/train"):
            return self.parse_instruction("/train")
        elif self.instruction.startswith("/infer"):
            return self.parse_instruction("/infer")
        elif self.instruction.startswith("/share"):
            return self.parse_instruction("/share")
        else:
            raise ValueError("Invalid instruction format")

    def parse_instruction(self, instruction_type):
        self.position += len(instruction_type)
        params = self.parse_params()
        return ParsedInstruction(instruction_type, params)

    def parse_params(self):
        params = {}
        while self.position < len(self.instruction):
            match = re.match(r"\s+--(\w+)=(\w+)", self.instruction[self.position:])
            if match:
                key, value = match.groups()
                params[key] = value
                self.position += match.end()
            else:
                break
        return params

# 사용 예시
# parser = InstructionParser("/train --data_cid=data123 --model_cid=model456")
# parsed_instruction = parser.parse()

# print("Is Train:", parsed_instruction.isTrain())
# print("Is Infer:", parsed_instruction.isInfer())
# print("Is Share:", parsed_instruction.isShare())
# print("Parameters:", parsed_instruction.params)

