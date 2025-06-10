import json

input_path = "Fine Tuning Data/converted_data.jsonl"
output_path = "Fine Tuning Data/ollama_ready_data.json"

data = []
with open(input_path, "r", encoding="utf-8") as infile:
    for line in infile:
        obj = json.loads(line)
        # Wrap messages as conversations
        data.append({"conversations": obj["messages"]})

with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=2)

print(f"Converted {len(data)} conversations to {output_path}") 