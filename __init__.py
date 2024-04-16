from rembg import remove
from PIL import Image, ImageDraw
import torch
import numpy as np

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# Convert PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
    
# 白色描边处理
def add_white_stroke(image, stroke_width=20):
    """
    给透明底的PNG图片内容主体添加白色描边。
    
    :param input_image_path: 输入图片的路径
    :param output_image_path: 输出图片的路径
    :param stroke_width: 描边的宽度，默认为2像素
    """
    
    # 创建一个新的图片，背景为透明
    output_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
    
    # 创建一个可以在上面绘制的对象
    draw = ImageDraw.Draw(output_image)
    
    # 获取图片的宽度和高度
    width, height = image.size
    
    # 遍历图片的每一个像素，检查边缘并描边
    for x in range(width):
        for y in range(height):
            # 只在图片内部进行操作
            if x > 0 and x < width - 1 and y > 0 and y < height - 1:
                # 获取当前像素及其上下左右四个邻居的颜色
                current_pixel = image.getpixel((x, y))
                top_pixel = image.getpixel((x, y - 1))
                bottom_pixel = image.getpixel((x, y + 1))
                left_pixel = image.getpixel((x - 1, y))
                right_pixel = image.getpixel((x + 1, y))
                
                # 检查当前像素是否与邻居像素不同，即是否为边缘
                if (current_pixel != top_pixel) or (current_pixel != bottom_pixel) or \
                   (current_pixel != left_pixel) or (current_pixel != right_pixel):
                    # 如果是边缘，添加白色描边
                    draw.line([x, y, x + 1, y], fill=(255, 255, 255, 255), width=stroke_width)
    
    # 将原图与描边后的图合并，保留原图的主体内容
    output_image.paste(image, (0, 0), image)
    
    # 保存输出图片
    return output_image

class ImageToSticker:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "stroke_width": ("INT", {
                    "default": 0, 
                    "min": 0, #Minimum value
                    "max": 64, #Maximum value
                    "step": 1, #Slider's step
                    "display": "number" # Cosmetic only: display as "number" or "slider"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "remove_background"
    CATEGORY = "image"

    def remove_background(self, image, stroke_width):
        pure_image = remove(tensor2pil(image))
        if stroke_width == 0
            image = pil2tensor(pure_image.convert('RGB'))
        else
            white_storke_image = add_white_stroke(pure_image, stroke_width)
            image = pil2tensor(white_storke_image.convert('RGB'))
        return (image,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Image To Sticker": ImageToSticker
}
