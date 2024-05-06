
import os
from PIL import Image
import torch
import tempfile
import io
import base64
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
xm = load_model('transmitter', device=device)
model = load_model('text300M', device=device)
diffusion = diffusion_from_config(load_config('diffusion'))



def image_to_prototype(image, filename):
    """ 
    Image is a PIL image 
    Returns b64 encoded data of the mesh data
    """
    batch_size = 1
    guidance_scale = 3.0
    latents = sample_latents(
        batch_size=batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=guidance_scale,
        model_kwargs=dict(images=[image] * batch_size),
        progress=True,
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=64,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=0,
    )
    for i, latent in enumerate(latents):
        with open(filename, 'wb') as f:
            decode_latent_mesh(xm, latent).tri_mesh().write_ply(f)

def save_prototype(image_path):
    image = Image.open(image_path)
    image_ref = image_path.split("/")[-2]
    image_id = image_path.split("/")[-1]
    image_to_prototype(image, f"assets/prototypes/{image_ref}/{image_id}.ply")


def list_files_with_subdirectories(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            full_path = os.path.join(root, filename)
            file_list.append(full_path)
    return file_list

if __name__ == "__main__":
    images = list_files_with_subdirectories("assets/images")
    print("images",images)
    for image in images:
        save_prototype(f"{image}")