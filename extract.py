import json
import re

lyrx_path = "ll.lyrx"
qml_path = "q.qml"
output_qml_path = "q_updated.qml"

with open(lyrx_path, "r", encoding="utf-8") as f:
    lyrx_data = json.load(f)

classes = lyrx_data["layerDefinitions"][0]["colorizer"]["groups"][0]["classes"]
label_map = {}
for cls in classes:
    values = cls["values"]
    label = cls["label"]
    for val in values:
        label_map[val] = label

with open(qml_path, "r", encoding="utf-8") as f:
    qml_lines = f.readlines()

updated_lines = []
pattern = re.compile(r'label="(.*?)"')
for line in qml_lines:
    if "<paletteEntry" in line:
        value_match = re.search(r'value="(\d+)"', line)
        if value_match:
            value = value_match.group(1)
            new_label = label_map.get(value, "Other uses")
            line = re.sub(pattern, f'label="{new_label}"', line)
    updated_lines.append(line)

with open(output_qml_path, "w", encoding="utf-8") as f:
    f.writelines(updated_lines)
