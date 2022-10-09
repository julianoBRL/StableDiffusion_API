import os
import PIL
from diffusers import StableDiffusionPipeline
import torch

def devices_verification(self):
    # setting device on GPU if available, else CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    print("########################################")
    print ('Available devices ', torch.cuda.device_count())
    print ('Current cuda device ', torch.cuda.current_device())
    print('GPU Device name:', torch.cuda.get_device_name(torch.cuda.current_device()))
    print("########################################")
    print('Using device:', device)
    print()

    #Additional Info when using cuda
    if device.type == 'cuda':
        print(torch.cuda.get_device_name(0))
        print('Memory Usage:')
        print('Allocated:', round(torch.cuda.memory_allocated(0)/1024**3,1), 'GB')
        print('Cached:   ', round(torch.cuda.memory_reserved(0)/1024**3,1), 'GB')
    print("########################################")

def check_essentials():
    isExistModels = os.path.exists("models")
    if not isExistModels: os.makedirs("models")

    isExistsImages = os.path.exists("images")
    if not isExistsImages: os.makedirs("images")
    
def image_grid(imgs, rows, cols):
    assert len(imgs) == rows*cols

    w, h = imgs[0].size
    grid = PIL.Image.new('RGB', size=(cols*w, rows*h))
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

def download_model():
    if "stable-diffusion-v1.4" not in os.listdir("models"):
        model = StableDiffusionPipeline.from_pretrained(
                'CompVis/stable-diffusion-v1-4',
                use_auth_token=TOKEN,
                revision='fp16',
                torch_dtype=torch.float16,
            )
        model.save_pretrained('models/stable-diffusion-v1.4')