import os
from nexa.gguf.sd import stable_diffusion
from utils import download_model

# Constants
STABLE_DIFFUSION_URL = "https://huggingface.co/second-state/stable-diffusion-v-1-4-GGUF/resolve/main/stable-diffusion-v1-4-Q4_0.gguf"
IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
OUTPUT_DIR = os.getcwd()
MODEL_PATH = download_model(STABLE_DIFFUSION_URL, OUTPUT_DIR)
IMAGE_PATH = download_model(IMAGE_URL, OUTPUT_DIR)

# Print the model path
print("Model downloaded to:", MODEL_PATH)
print("Image downloaded to:", IMAGE_PATH)

# Helper function for Stable Diffusion initialization
def init_stable_diffusion():
    return stable_diffusion.StableDiffusion(
        model_path=MODEL_PATH,
        wtype="q4_0"  # Weight type (options: default, f32, f16, q4_0, q4_1, q5_0, q5_1, q8_0)
    )

# Test text-to-image generation
def test_txt_to_img():
    sd = init_stable_diffusion()
    output = sd.txt_to_img("a lovely cat", sample_steps=4)
    output[0].save("output_txt_to_img.png")

# Test image-to-image generation
def test_img_to_img():
    sd = init_stable_diffusion()
    output = sd.img_to_img(
        image="test.png",  
        prompt="blue sky",  
        negative_prompt="black soil",
        sample_steps=4
    )
    output[0].save("output_img_to_img.png")

# Main execution
if __name__ == "__main__":
    test_txt_to_img()
    test_img_to_img()
