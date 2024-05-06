"""
Use hard-coded values for the sketch2prototype website
"""
import os
import base64
import json

def encode_image_to_b64_json(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image_bytes = base64.b64encode(image_file.read())
        encoded_image_str = encoded_image_bytes.decode('utf-8')
        b64_json = json.dumps({"image_base64": encoded_image_str})
        return encoded_image_str
    
base_dir = "assets/images"
def text_to_image_hardcode(id : str):
    images = os.listdir(f"{base_dir}/{id}")
    return [encode_image_to_b64_json(f"{base_dir}/{id}/{image}") for image in images]


def image_to_3d_hardcode(image_ref, image_id):
    with open(f"assets/prototypes/{image_ref}/image_{image_id}.ply", 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

if __name__ == "__main__":
    text_to_image_hardcode("1")