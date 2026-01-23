import os
import uuid

def save_file(file_obj, base_folder, subfolder):
    if not file_obj or file_obj.filename == "":
        return None

    folder = os.path.join(base_folder, subfolder)
    os.makedirs(folder, exist_ok=True)

    ext = os.path.splitext(file_obj.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(folder, filename)

    file_obj.save(path)

    return path.replace("\\", "/")
