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



def image_to_prototype(image):
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
    tmp = tempfile.NamedTemporaryFile(suffix='.ply')
    for i, latent in enumerate(latents):
        with open(tmp.name, 'wb') as f:
            decode_latent_mesh(xm, latent).tri_mesh().write_ply(f)
        with open(tmp.name, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')

"""
with open('test.ply', 'wb') as f:
    f.write(base64.b64decode(a))
"""
def image_to_3d_mock(image):
    with open("assets/example_mesh_0.ply", 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

if __name__ == "__main__":
    from PIL import Image
    test_image = Image.open("assets/image_0.png")
    test = image_to_3d(test_image)
    with open('test.glb', 'wb') as f:
        f.write(base64.b64decode(test))