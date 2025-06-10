import json
import logging
from pathlib import Path
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_conversation(conversation):
    """Convert a single conversation to the required format."""
    messages = []
    for msg in conversation["conversations"]:
        if msg["role"] == "user":
            # Extract instruction and input from the content
            content = msg["content"]
            if "instruction:" in content and "input:" in content:
                instruction, input_text = content.split("input:", 1)
                instruction = instruction.replace("instruction:", "").strip()
                input_text = input_text.strip()
                
                messages.append({
                    "role": "user",
                    "content": f"Instruction: {instruction}\nInput: {input_text}"
                })
            else:
                messages.append({
                    "role": "user",
                    "content": content
                })
        else:
            messages.append({
                "role": "assistant",
                "content": msg["content"]
            })
    return messages

def process_file(input_file, output_file):
    """Process the input file and write the converted data to the output file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        converted_data = []
        for conversation in data:
            messages = convert_conversation(conversation)
            if messages:
                converted_data.append({
                    "messages": messages
                })
        
        # Write the converted data
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in converted_data:
                f.write(json.dumps(item) + '\n')
        
        logger.info(f"Successfully converted {len(converted_data)} conversations")
        logger.info(f"Output written to {output_file}")
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Convert training data to the required format')
    parser.add_argument('--input-file', type=str, required=True, help='Path to input JSON file')
    parser.add_argument('--output-file', type=str, required=True, help='Path to output JSONL file')
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    output_path = Path(args.output_file)
    
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        return
    
    process_file(input_path, output_path)

if __name__ == '__main__':
    main() 