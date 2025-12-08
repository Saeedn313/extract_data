import mammoth
from pathlib import Path

files = [file for file in Path(".").glob("*.docx")]     

file = files[1]
with open(file, "rb") as file:
    result = mammoth.convert_to_html(file)
    html_data = result.value

print(html_data)