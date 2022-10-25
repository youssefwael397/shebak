import os
import uuid


def save_logo(logo, file_name):
    logo.save(f"static/users/logo/{file_name}")


def delete_logo(logo):
    if logo and os.path.exists(f"static/users/logo/{logo}"):
        os.remove(f"static/users/logo/{logo}")

def save_file(file, file_name, path):
    file.save(f"{path}/{file_name}")


def delete_file(file_name, path):
    if file_name and os.path.exists(f"{path}/{file_name}"):
        os.remove(f"{path}/{file_name}")
