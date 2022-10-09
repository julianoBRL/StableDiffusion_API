import os
import torch
from time import time
from random import randint
from torch import autocast
from slugify import slugify
from src.services.Server import server
from src.objects.ImageModel import ImageDB
from diffusers import StableDiffusionPipeline
from src.services.SystemManager import image_grid, devices_verification

TOKEN = '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'
DEFAULT_IMG_QTD = 4

class StableDiffusion:
    
    #Always direct the job to the gpu that has more memory available
    def gpu_loadbalance(self):
        list_available_memory = []
        for i in range(torch.cuda.device_count()):
            list_available_memory.append(round(torch.cuda.memory_reserved(i)/1024**3,1))
        min_mem = min(list_available_memory)
        mim_mem_index = list_available_memory.index(min_mem)
        print("redirecting process to GPU-"+str(mim_mem_index)+" with "+str(min_mem)+"GB free.")
        return mim_mem_index

        
    def initialize_model(self,mode=0):
        model = ''
        if "stable-diffusion-v1-4" in os.listdir("models"):
            model = StableDiffusionPipeline.from_pretrained('models/stable-diffusion-v1-4')
        else:
            model = StableDiffusionPipeline.from_pretrained(
                'CompVis/stable-diffusion-v1-4',
                use_auth_token=TOKEN,
                revision='fp16',
                torch_dtype=torch.float16,
            )
            model.save_pretrained('models/stable-diffusion-v1-4')

        # you can set the device on 0 ou 1, create LoadBalancer
        device = torch.device("cuda:"+str(self.gpu_loadbalance()) if torch.cuda.is_available() else "cpu")
        model.to(device)
        if mode == 1: model.enable_attention_slicing()
        model.device
        print("Model loaded!!!")
        return model
    
    def generate(self,prompt,job_id, queue, ar="512x512"):
        print(f'generating {DEFAULT_IMG_QTD} new images for prompt: {prompt}')
        resolution_s = ar.split('x')
        image_set_names = [];
        image_set = []
        model_intern = self.initialize_model()
        with autocast('cuda'):
            for r in range(DEFAULT_IMG_QTD):
                output = model_intern(
                    prompt,
                    num_inference_steps=100,           # diffusion iterations default 50
                    guidance_scale=7.5,               # adherence to text, default 7.5
                    width=int(resolution_s[0]),       # image width, default 512
                    height=int(resolution_s[1])       # image height, default 512
                )

                image = output['sample'][0]
                image_name = f'{time()}_{slugify(prompt[:100])}.png'
                image.save(f'images/{image_name}')
                image_set_names.append(image_name)
                image_set.append(image)
                server.db.session.add(ImageDB(image_name,prompt,image_name,job_id))
                server.db.session.commit()
        image_name = f'{time()}_{slugify(prompt[:100])}_grid.png'
        image_grid(image_set,2,2).save(f'images/{image_name}')
        server.db.session.add(ImageDB(image_name,prompt,image_name,job_id))
        server.db.session.commit()
        image_set_names.append(image_name)
        torch.cuda.empty_cache()
        queue.put(image_set_names)
    
stableDiffusion = StableDiffusion()