# Imports
import os
import json
import shutil
import pydub
from pydub.utils import mediainfo

# Docstring
'''
1) get into each folder (duration, freq, order, timestamp)
1.1) in each folder, edit each json entry and rename the audio file to avoid conflicts. 
1.1.1) edit the jsons to follow Vlad's format
1.2) combine all folders into one large one, according to Vlad's template
1.3) Create russian and kazakh translations
'''

# Configurations
relative_path = r'AudioTime-train\train5000_duration'
json_name = r'duration_captions'
audiofile_extension = r'.wav'
user_prompts = [
    'summarize this audio',
    'what is happening in this audio?',
    'what is the audio about?',
    'provide an analysis of this audio',
    'can you identify the main message of this audio?'
    'describe the audio in a few sentences'
]

# Function Declarations
def get_duration(audio_path):
    audio_info = mediainfo(audio_path)
    duration = float(audio_info['duration'])
    return duration

# Main Execution Block
def main():
    current_directory = os.path.dirname(__file__)
    folder_path = os.path.join(current_directory, relative_path)
    audio_path = os.path.join(folder_path, r'audio')
    json_path = os.path.join(folder_path, json_name+'.json')

    with open(json_path, 'r') as f:
        data = json.load(f)

    json_with_needed_format = []

    counter = 0
    for audio_data in data:
        old_name = audio_data
        new_name = old_name + json_name
        old_file_path = os.path.join(audio_path, old_name + audiofile_extension)
        new_file_path = os.path.join(audio_path, new_name + audiofile_extension)

        os.rename(old_file_path, new_file_path)
        # print(f"Renamed: {old_name} -> {new_name}")

        duration = get_duration(new_file_path)

        prompt_id = counter % len(user_prompts)
        prompt = user_prompts[prompt_id]

        caption = data[audio_data]['caption']

        entry = {
            "id": counter,
            "audio": f"audios/{new_name}{audiofile_extension}",
            "audio_length_seconds": duration,
            "conversations": [
                {"from": "human", "value": f"<audio>\n{prompt}"},
                {"from": "gpt", "value": caption}
            ]
        }

        json_with_needed_format.append(entry)

        counter += 1

    output_json_path = os.path.join(current_directory, 'formatted_audio_data.json')
    with open(output_json_path, 'w', encoding='utf-8') as jsn:
        json.dump(json_with_needed_format, jsn, ensure_ascii=False)

    print("Finished")

if __name__ == "__main__":
    main()