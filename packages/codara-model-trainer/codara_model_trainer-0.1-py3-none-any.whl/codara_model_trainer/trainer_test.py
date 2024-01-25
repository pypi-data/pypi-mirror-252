import os
import json
from codara_model_trainer.trainer import FineTuningDataCreator


class TestFineTuningDataCreator:
    def setup_method(self):
        """Setup for test methods."""
        self.creator = FineTuningDataCreator()
        self.test_dir = 'test-model-training'
        self.test_file = f'{self.test_dir}/fine-tune-data-set.jsonl'
        self.creator.filepath = self.test_file

    def teardown_method(self):
        """Teardown for test methods."""
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_agent_instructions(self):
        test_content = "Test agent instruction."
        self.creator.agent_instructions(test_content)
        assert self.creator.system_content == test_content

    def test_training_prompt(self):
        test_prompt = "Test prompt."
        self.creator.training_prompt(test_prompt)
        assert self.creator.prompt == test_prompt

    def test_generative_response(self):
        test_response = "Test response."
        self.creator.generative_response(test_response)
        assert self.creator.response == test_response

    def test_create_data_set(self):
        self.creator.agent_instructions("Test instructions.")
        self.creator.training_prompt("Test prompt.")
        self.creator.generative_response("Test response.")
        self.creator.create_data_set()

        assert os.path.exists(self.test_file)
        with open(self.test_file, 'r') as file:
            data = json.loads(file.readline())
            assert data == {
                "messages": [
                    {"role": "system", "content": "Test instructions."},
                    {"role": "user", "content": "Test prompt."},
                    {"role": "assistant", "content": "Test response."}
                ]
            }

    def test_create_data_set_directory_exists(self):
        os.makedirs(self.test_dir, exist_ok=True)
        assert os.path.exists(self.test_dir)  # Ensure directory exists
        self.creator.create_data_set()
        assert os.path.exists(self.test_file)  # Check if file is created

    def test_create_data_set_file_exists(self):
        os.makedirs(self.test_dir, exist_ok=True)
        # Create an empty file
        with open(self.test_file, 'w') as file:
            file.write("")

        assert os.path.exists(self.test_file)  # Ensure file exists

        self.creator.agent_instructions("Test instructions.")
        self.creator.training_prompt("Test prompt.")
        self.creator.generative_response("Test response.")
        self.creator.create_data_set()

        # Read the file for the data
        with open(self.test_file, 'r') as file:
            lines = file.readlines()

            # If file was initially empty, the data should be on the first line
            line_to_check = lines[0] if len(lines) == 1 else lines[-1]
            data = json.loads(line_to_check)
            assert data["messages"][0]["content"] == "Test instructions."

