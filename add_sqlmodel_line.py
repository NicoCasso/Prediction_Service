import os

folder_path = 'alembic/versions'
folder_content = os.listdir(folder_path)

files = [f for f in folder_content if os.path.isfile(os.path.join(folder_path , f))]

selected_filename = max(files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
selected_filename = os.path.join(folder_path , selected_filename)

with open(selected_filename, 'r') as file:
    old_content = file.readlines()

line_to_add  = 'import sqlmodel\n'
with open(selected_filename, 'w') as file:
    file.write(line_to_add)
    file.writelines(old_content)
