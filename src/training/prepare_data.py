import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrainingDataPreparator:
    def __init__(self, input_dir: str, output_file: str):
        self.input_dir = Path(input_dir)
        self.output_file = Path(output_file)
        self.valid_categories = {
            'economics', 'game_theory', 'tokenomics', 
            'staking', 'governance'
        }
        self.valid_difficulties = {
            'beginner', 'intermediate', 'advanced'
        }

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a single training data entry."""
        required_fields = {'instruction', 'output', 'category', 'difficulty'}
        
        # Check required fields
        if not all(field in entry for field in required_fields):
            logger.warning(f"Missing required fields in entry: {entry}")
            return False
        
        # Validate category
        if entry['category'] not in self.valid_categories:
            logger.warning(f"Invalid category in entry: {entry['category']}")
            return False
        
        # Validate difficulty
        if entry['difficulty'] not in self.valid_difficulties:
            logger.warning(f"Invalid difficulty in entry: {entry['difficulty']}")
            return False
        
        return True

    def process_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Process a single training data file."""
        valid_entries = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if self.validate_entry(entry):
                            valid_entries.append(entry)
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON in file {file_path}: {line}")
                        continue
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
        
        return valid_entries

    def prepare_data(self):
        """Prepare and combine all training data."""
        all_entries = []
        
        # Process all JSONL files in the input directory
        for file_path in self.input_dir.glob('**/*.jsonl'):
            logger.info(f"Processing file: {file_path}")
            entries = self.process_file(file_path)
            all_entries.extend(entries)
        
        # Write combined data
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                for entry in all_entries:
                    f.write(json.dumps(entry) + '\n')
            
            logger.info(f"Successfully processed {len(all_entries)} entries")
            logger.info(f"Output written to: {self.output_file}")
            
            # Print statistics
            categories = {}
            difficulties = {}
            for entry in all_entries:
                categories[entry['category']] = categories.get(entry['category'], 0) + 1
                difficulties[entry['difficulty']] = difficulties.get(entry['difficulty'], 0) + 1
            
            logger.info("\nCategory distribution:")
            for category, count in categories.items():
                logger.info(f"{category}: {count}")
            
            logger.info("\nDifficulty distribution:")
            for difficulty, count in difficulties.items():
                logger.info(f"{difficulty}: {count}")
                
        except Exception as e:
            logger.error(f"Error writing output file: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Prepare training data for fine-tuning')
    parser.add_argument('--input-dir', required=True, help='Directory containing training data files')
    parser.add_argument('--output-file', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    preparator = TrainingDataPreparator(args.input_dir, args.output_file)
    preparator.prepare_data()

if __name__ == "__main__":
    main() 