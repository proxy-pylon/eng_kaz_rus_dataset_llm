import json
import csv


def extract_dialogue_to_csv(jsonl_path, csv_path):
    """Extract only 'value' fields from 'conversations', removing '<audio>\n' from human messages."""
    with open(jsonl_path, 'r', encoding='utf-8') as jsonl_file, open(csv_path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        writer.writerow(["human", "gpt"])  # No "id" in the CSV

        for line in jsonl_file:
            entry = json.loads(line)
            human_conversation = entry["conversations"][0]["value"].replace("<audio>\n", "").strip()
            gpt_conversation = entry["conversations"][1]["value"].strip()
            writer.writerow([human_conversation, gpt_conversation])

def reconstruct_jsonl_from_csv(csv_path, jsonl_path, jsonl_reference_path):
    """Reconstruct JSONL from translated CSV while preserving original metadata."""
    # Load reference JSONL structure (to restore metadata)
    reference_entries = []
    with open(jsonl_reference_path, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            reference_entries.append(json.loads(line))  # Keep order intact

    # Read translated CSV
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        translated_dialogues = list(reader)  # Load translations in order

    # Replace conversations while keeping original metadata
    for entry, translated in zip(reference_entries, translated_dialogues):
        entry["conversations"][0]["value"] = f"<audio>\n{translated['human'].strip()}"
        entry["conversations"][1]["value"] = translated["gpt"].strip()

    # Write back to JSONL
    with open(jsonl_path, 'w', encoding='utf-8') as jsonl_file:
        for entry in reference_entries:
            jsonl_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

# extract_dialogue_to_csv(r"./AudioTime-combined/AudioTime_en.jsonl", r"./AudioTime-combined/AudioTime_en.csv")
# After manual translation
reconstruct_jsonl_from_csv(r"AudioTime-combined/AudioTime_ru.csv", r"AudioTime-combined/AudioTime_ru.jsonl", r"./AudioTime-combined/AudioTime_en.jsonl")