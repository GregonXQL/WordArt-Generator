from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from diffusers.utils import load_image
import torch
from transformers import CLIPTextModel, CLIPTextModelWithProjection, PreTrainedModel, PreTrainedTokenizer

def load_model(
        base_model_path= "runwayml/stable-diffusion-v1-5",
        controlnet_path = "lllyasviel/control_v11f1p_sd15_depth"
    ):
    controlnet = ControlNetModel.from_pretrained(controlnet_path, torch_dtype=torch.float16, use_safetensors=True)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        base_model_path, controlnet=controlnet, torch_dtype=torch.float16, use_safetensors=True
    )
    return pipe

def infer(
        #图片
        control_image_path=None,
        #文本
        prompt=None,
        negative_prompt=None,
        seed=0,
        num_inference_steps=20,
        guidance_scale=7.5,
        height = 512,
        width = 512,
        controlnet_conditioning_scale=1.0,
        base_model_path="runwayml/stable-diffusion-v1-5",
        controlnet_path="lllyasviel/control_v11f1p_sd15_depth",
    ):
    pipe = load_model(
        base_model_path=base_model_path,
        controlnet_path=controlnet_path
    )
    # speed up diffusion process with faster scheduler and memory optimization
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    # remove following line if xformers is not installed
    pipe.enable_xformers_memory_efficient_attention()

    pipe.enable_model_cpu_offload()

    # generate image
    generator = torch.manual_seed(seed)

    control_image= load_image(control_image_path)
    image = pipe(prompt, negative_prompt=negative_prompt,num_inference_steps=num_inference_steps, generator=generator, image=control_image,
                guidance_scale=guidance_scale,height=height,width=width,controlnet_conditioning_scale=controlnet_conditioning_scale
                 ).images[0]

    image.save("./output.png")
    return image