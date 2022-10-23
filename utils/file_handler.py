import os
import uuid


def save_logo(logo, file_name):
    logo.save(f"static/users/logo/{file_name}")


def delete_logo(logo):
    if logo and os.path.exists(f"static/users/logo/{logo}"):
        os.remove(f"static/users/logo/{logo}")