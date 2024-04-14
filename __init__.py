from rembg import remove
from PIL import Image
import torch
import numpy as np

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# Convert PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class ImageToSticker:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "remove_background"
    CATEGORY = "image"

    def remove_background(self, image):
        image = pil2tensor(remove(tensor2pil(image)))
        # 创建一个黑色背景的同样大小的图像
        black_bg = Image.new('RGB', image.size, color = (0, 0, 0))
        # 将原始图像粘贴到黑色背景上
        black_bg.paste(image, image.size, image)
        return (black_bg,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Image To Sticker": ImageToSticker
}
