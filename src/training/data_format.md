# Training Data Format

## JSONL Format
Each line in the training data should be a JSON object with the following structure:

```json
{
  "instruction": "The user's question or prompt",
  "input": "Optional additional context",
  "output": "The expected response",
  "category": "One of: economics, game_theory, tokenomics, staking, governance",
  "source": "Source of the knowledge (e.g., Web3 Foundation, Polkadot Academy)",
  "difficulty": "One of: beginner, intermediate, advanced"
}
```

## Example Entry
```json
{
  "instruction": "Explain the tokenomics of DOT staking rewards",
  "input": "Consider both nominator and validator perspectives",
  "output": "DOT staking rewards are distributed based on several factors: 1) The total amount of DOT staked in the network, 2) The validator's commission rate, 3) The nominator's stake size relative to the validator's total stake. Rewards are calculated per era (6 hours) and distributed proportionally. The inflation rate is designed to be between 7.5% and 10% annually, with the exact rate determined by the staking ratio.",
  "category": "staking",
  "source": "Polkadot Wiki",
  "difficulty": "intermediate"
}
```

## Data Organization
1. Create separate files for each category
2. Include a mix of difficulty levels
3. Ensure diverse sources of information
4. Include both theoretical and practical examples

## Quality Guidelines
1. Responses should be accurate and up-to-date
2. Include specific numbers and data where relevant
3. Maintain professional tone
4. Keep responses concise but informative
5. Include practical examples when possible 