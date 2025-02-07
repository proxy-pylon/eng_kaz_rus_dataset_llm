import os
import json
import shutil

relative_paths = [r'AudioTime-train\train5000_duration', r'AudioTime-train\train5000_frequency', r'AudioTime-train\train5000_ordering', r'AudioTime-train\train5000_timestamp']
jsonl_names = [r'formatted_audio_data', r'formatted_audio_data', r'formatted_audio_data', r'formatted_audio_data']
combined_relative_path = r'AudioTime-combined'
combined_json_name = 'AudioTime_en'
current_directory = os.path.dirname(__file__)

combined_folder_path = os.path.join(current_directory, combined_relative_path)
combined_audio_path = os.path.join(combined_folder_path, 'audios')
combined_json_path = os.path.join(combined_folder_path, combined_json_name +'.jsonl')

if not os.path.exists(combined_folder_path):
    os.makedirs(combined_folder_path)

if not os.path.exists(combined_audio_path):
    os.makedirs(combined_audio_path)

for folder in relative_paths:
    audio_folder = os.path.join(folder, 'audio')
    for filename in os.listdir(audio_folder):
        src_file = os.path.join(audio_folder, filename)
        dst_file = os.path.join(combined_audio_path, filename)
        shutil.copy(src_file, dst_file)

with open(combined_json_path, 'w') as outfile:
    for json_name, folder in zip(jsonl_names, relative_paths):
        jsonl_path = os.path.join(folder, f'{json_name}.jsonl')
        with open(jsonl_path, 'r') as infile:
            for line in infile:
                data = json.loads(line)
                json.dump(data, outfile)
                outfile.write('\n')

