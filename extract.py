import json
import re

lyrx_path = "ll.lyrx"
qml_path = "q.qml"
output_qml_path = "q_updated.qml"

with open(lyrx_path, "r", encoding="utf-8") as f:
    lyrx_data = json.load(f)

classes = lyrx_data["layerDefinitions"][0]["colorizer"]["groups"][0]["classes"]

label_map = {}
color_label_map = {}

def rgba_to_hex(rgba):
    return "#{:02x}{:02x}{:02x}".format(*rgba[:3])

for cls in classes:
    values = cls["values"]
    label = cls["label"]
    rgba = cls["color"]["values"]
    hex_color = rgba_to_hex(rgba)
    for val in values:
        label_map[val] = label
    if hex_color not in color_label_map:
        color_label_map[hex_color] = label

with open(qml_path, "r", encoding="utf-8") as f:
    qml_lines = f.readlines()

updated_lines = []
label_pattern = re.compile(r'label="(.*?)"')
value_pattern = re.compile(r'value="(\d+)"')
color_pattern = re.compile(r'color="(#(?:[0-9a-fA-F]{6}))"')

for line in qml_lines:
    if "<paletteEntry" in line:
        value_match = value_pattern.search(line)
        color_match = color_pattern.search(line)
        if value_match:
            value = value_match.group(1)
            if value in label_map:
                label = label_map[value]
                line = re.sub(label_pattern, f'label="{label}"', line)
            elif color_match:
                color = color_match.group(1).lower()
                if color in color_label_map:
                    label = color_label_map[color]
                    line = re.sub(label_pattern, f'label="{label}"', line)
    updated_lines.append(line)

with open(output_qml_path, "w", encoding="utf-8") as f:
    f.writelines(updated_lines)
