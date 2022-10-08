import os
import PIL

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
