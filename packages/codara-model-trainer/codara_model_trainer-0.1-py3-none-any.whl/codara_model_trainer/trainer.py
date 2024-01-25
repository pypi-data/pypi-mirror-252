import os
import json

class FineTuningDataCreator:
    def __init__(self):
        self.system_content = ""
        self.prompt = ""
        self.response = ""
        self.filepath = "model-training/fine-tune-data-set.jsonl"

    def agent_instructions(self, content):
        self.system_content = content

    def training_prompt(self, prompt):
        self.prompt = prompt

    def generative_response(self, response):
        self.response = response

    def create_data_set(self):
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        # Create or append to the file
        data = {
            "messages": [
                {"role": "system", "content": self.system_content},
                {"role": "user", "content": self.prompt},
                {"role": "assistant", "content": self.response}
            ]
        }

        with open(self.filepath, 'a') as file:
            file.write(json.dumps(data) + "\n")
