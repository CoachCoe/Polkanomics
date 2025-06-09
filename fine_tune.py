import logging
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import torch

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model configuration
model_name = "microsoft/phi-2"
output_dir = "fine_tuned_model"

def prepare_model():
    """Prepare the model and tokenizer for training."""
    try:
        logger.info("Loading model and tokenizer...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        # Add padding token if it doesn't exist
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Configure LoRA
        lora_config = LoraConfig(
            r=16,  # rank
            lora_alpha=32,
            target_modules=["q_proj", "k_proj", "v_proj", "dense"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        # Prepare model for training
        model = prepare_model_for_kbit_training(model)
        model = get_peft_model(model, lora_config)
        
        return model, tokenizer
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

def prepare_dataset(tokenizer):
    """Prepare the dataset for training."""
    try:
        logger.info("Loading and preparing dataset...")
        dataset = load_dataset("json", data_files="training_data.jsonl")
        
        def tokenize_function(examples):
            tokens = tokenizer(
                examples["text"],
                padding="max_length",
                truncation=True,
                max_length=512
            )
            tokens["labels"] = tokens["input_ids"].copy()
            return tokens
        
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset["train"].column_names
        )
        
        return tokenized_dataset
    except Exception as e:
        logger.error(f"Error preparing dataset: {str(e)}")
        raise

def train():
    """Main training function."""
    try:
        # Prepare model and dataset
        model, tokenizer = prepare_model()
        dataset = prepare_dataset(tokenizer)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            learning_rate=2e-4,
            weight_decay=0.01,
            warmup_steps=100,
            logging_steps=10,
            save_strategy="epoch"
        )
        
        # Initialize trainer
        data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset["train"],
            tokenizer=tokenizer,
            data_collator=data_collator
        )
        
        # Start training
        logger.info("Starting training...")
        trainer.train()
        
        # Save the model
        logger.info("Saving model...")
        trainer.save_model()
        tokenizer.save_pretrained(output_dir)
        
        logger.info("Training completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during training: {str(e)}")
        raise

if __name__ == "__main__":
    train() 