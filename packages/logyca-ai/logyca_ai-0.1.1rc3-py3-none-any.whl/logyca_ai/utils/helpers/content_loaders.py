import base64
import os
import requests

def file_to_base64(image_full_path):
  with open(image_full_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_base64_from_file(image_full_path):
  with open(image_full_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def save_base64_to_file(base64_string: str, output_folder: str, filename: str):
    binary_data = base64.b64decode(base64_string)
    output_path = os.path.join(output_folder, filename)
    with open(output_path, 'wb') as file:
        file.write(binary_data)

def save_file_from_url(url: str, output_folder: str, filename: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el archivo: {e}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
