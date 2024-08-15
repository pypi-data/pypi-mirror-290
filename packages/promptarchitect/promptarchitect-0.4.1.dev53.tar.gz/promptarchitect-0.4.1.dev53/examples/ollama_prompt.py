from pathlib import Path

from promptarchitect import EngineeredPrompt

prompt_path = Path(__file__).parent / "prompts" / "ollama.prompt"
input_file_path = (
    Path(__file__).parent / "inputs" / "podcast_titels" / "beschrijving.txt"
)

# Initialize the EngineeredPrompt
prompt = EngineeredPrompt(
    prompt_file_path=str(prompt_path), output_path="output_directory"
)

prompt.completion.download_model("gemma2")
# Execute the prompt
response = prompt.execute(input_file=str(input_file_path), cached=False)


print(response)
