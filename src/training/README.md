# Model Training Guide

This guide explains how to fine-tune the model for the Polkanomics Chat application.

## Prerequisites

1. Install Ollama:
   ```bash
   curl https://ollama.ai/install.sh | sh
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Training Data Preparation

1. Organize your training data according to the format specified in `data_format.md`
2. Place your training data files in the `training_data` directory
3. Run the data preparation script:
   ```bash
   python prepare_data.py --input-dir training_data --output-file prepared_data.jsonl
   ```

## Fine-tuning with Ollama

1. Start the fine-tuning process:
   ```bash
   python fine_tune_ollama.py --training-file prepared_data.jsonl --model mistral
   ```

   Options:
   - `--model`: Base model to fine-tune (default: mistral)
   - `--training-file`: Path to prepared training data

2. Monitor the training progress in the logs
3. The fine-tuned model will be available as `polkanomics-mistral` in Ollama

## Using the Fine-tuned Model

1. Update the model name in `src/services/chatService.ts`:
   ```typescript
   body: JSON.stringify({
     model: 'polkanomics-mistral',  // Use your fine-tuned model
     prompt: fullPrompt,
     // ...
   })
   ```

2. Restart the application to use the new model

## Training Data Guidelines

1. **Quality**:
   - Ensure responses are accurate and up-to-date
   - Include specific numbers and data where relevant
   - Maintain professional tone
   - Keep responses concise but informative

2. **Categories**:
   - Economics
   - Game Theory
   - Tokenomics
   - Staking
   - Governance

3. **Difficulty Levels**:
   - Beginner
   - Intermediate
   - Advanced

4. **Sources**:
   - Web3 Foundation
   - Polkadot Wiki
   - Polkadot Blockchain Academy
   - Academic papers
   - Technical documentation

## Troubleshooting

1. **Training Data Issues**:
   - Check the data format using `prepare_data.py`
   - Ensure all required fields are present
   - Validate categories and difficulty levels

2. **Fine-tuning Issues**:
   - Check Ollama logs for errors
   - Verify model compatibility
   - Ensure sufficient system resources

3. **Model Performance**:
   - Test with various question types
   - Monitor response quality
   - Adjust parameters if needed

## Best Practices

1. **Data Collection**:
   - Gather diverse examples
   - Include edge cases
   - Balance difficulty levels
   - Use multiple sources

2. **Training Process**:
   - Start with a small dataset
   - Validate results
   - Iterate and improve
   - Document changes

3. **Model Evaluation**:
   - Test with real users
   - Collect feedback
   - Monitor performance
   - Update regularly 