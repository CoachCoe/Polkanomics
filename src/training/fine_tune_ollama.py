import json
import logging
import subprocess
from pathlib import Path
import argparse
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaFineTuner:
    def __init__(self, training_file: str, model_name: str = "mistral"):
        self.training_file = Path(training_file)
        self.model_name = model_name
        self.base_model = f"ollama/{model_name}"
        self.fine_tuned_model = f"polkanomics-{model_name}"

    def prepare_modelfile(self):
        """Create a Modelfile for Ollama fine-tuning."""
        modelfile_content = (
            f"FROM {self.base_model}\n\n"
            "# Set the system prompt\n"
            'SYSTEM "You are an expert economist with deep expertise in economics, '
            'game theory, and Polkadot tokenomics. You provide clear, accurate, '
            'and detailed explanations while maintaining a professional and educational tone."\n\n'
            "# Set parameters\n"
            "PARAMETER temperature 0.7\n"
            "PARAMETER top_p 0.95\n"
            "PARAMETER top_k 40\n"
            "PARAMETER num_ctx 4096\n"
            "PARAMETER repeat_penalty 1.1\n"
        )
        
        modelfile_path = Path("Modelfile")
        with open(modelfile_path, "w") as f:
            f.write(modelfile_content)
        
        return modelfile_path

    def create_training_file(self):
        """Convert JSONL training data to Ollama format."""
        ollama_data = []
        
        with open(self.training_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                # Format: instruction + input (if present) -> output
                prompt = entry['instruction']
                if entry.get('input'):
                    prompt += f"\nContext: {entry['input']}"
                
                ollama_data.append({
                    "prompt": prompt,
                    "completion": entry['output']
                })
        
        # Save in Ollama format
        ollama_file = Path("ollama_training.json")
        with open(ollama_file, 'w') as f:
            json.dump(ollama_data, f, indent=2)
        
        return ollama_file

    def fine_tune(self):
        """Run the fine-tuning process."""
        try:
            # Prepare files
            logger.info("Preparing Modelfile...")
            modelfile_path = self.prepare_modelfile()
            
            logger.info("Converting training data...")
            training_file = self.create_training_file()
            
            # Create the model
            logger.info(f"Creating fine-tuned model: {self.fine_tuned_model}")
            create_cmd = ["ollama", "create", self.fine_tuned_model, "-f", str(modelfile_path)]
            subprocess.run(create_cmd, check=True)
            
            # Fine-tune the model
            logger.info("Starting fine-tuning process...")
            train_cmd = [
                "ollama", "train",
                "--model", self.fine_tuned_model,
                "--data", str(training_file)
            ]
            
            process = subprocess.Popen(
                train_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Monitor training progress
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    logger.info(output.strip())
            
            if process.returncode == 0:
                logger.info("Fine-tuning completed successfully!")
            else:
                error = process.stderr.read()
                logger.error(f"Fine-tuning failed: {error}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error during fine-tuning: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
        finally:
            # Cleanup
            for file in [modelfile_path, training_file]:
                if file.exists():
                    file.unlink()

def main():
    parser = argparse.ArgumentParser(description='Fine-tune Ollama model with custom data')
    parser.add_argument('--training-file', required=True, help='Path to training data file')
    parser.add_argument('--model', default='mistral', help='Base model to fine-tune')
    
    args = parser.parse_args()
    
    tuner = OllamaFineTuner(args.training_file, args.model)
    tuner.fine_tune()

if __name__ == "__main__":
    main() 