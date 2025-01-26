from etils.epath import Path
import json
import torch
from torchvision import transforms
from PIL import Image
import numpy as np

# Enter path to OmniNOCS folder here.
data_root = Path('/mnt/data/OmniNOCS/')
output_dir = Path('/mnt/data/OmniNOCS_output/')  # Define the output directory to save images

# Ensure the output directory exists
output_dir.mkdir(parents=True, exist_ok=True)

def save_image(tensor, path, dtype=torch.uint16):
    """Save tensor to image file."""
    if dtype == torch.uint16:
        # Convert the tensor to a uint16 image (multiply by 65535 to map to range)
        img = tensor.numpy().astype(np.uint16)
        img = Image.fromarray(img)
    elif dtype == torch.float32:
        # Convert to uint8 (scale to [0, 255])
        img = tensor.numpy() * 255
        img = img.astype(np.uint8)
        img = Image.fromarray(img)
    img.save(path)

def get_instance_nocs_images(ds_name, split, num_frames=5):
    all_frames = []
    with (data_root / f'{ds_name}_{split}_metadata.json').open(mode='r') as f:
        frames = json.load(f)

    for i in range(num_frames):
        frame = frames[i]
        instance_img_path = data_root / f'{frame["omninocs_name"]}_instances.png'
        nocs_img_path = data_root / f'{frame["omninocs_name"]}_nocs.png'

        # Load instance image
        instance_img = Image.open(instance_img_path).convert('I')  # 'I' mode for 16-bit images
        instance_img = np.array(instance_img)  # Convert to numpy array
        
        # Load NOCS image
        nocs_img = Image.open(nocs_img_path).convert('I')  # 'I' mode for 16-bit images
        nocs_img = np.array(nocs_img)  # Convert to numpy array

        # Convert NOCS image to float32
        nocs_img = nocs_img.astype(np.float32) / 65535.0  # Normalize to [0, 1]

        # Convert to tensors
        instance_tensor = torch.tensor(instance_img, dtype=torch.uint16)
        nocs_tensor = torch.tensor(nocs_img, dtype=torch.float32)

        # Save the images locally
        save_image(instance_tensor, output_dir / f'{frame["omninocs_name"]}_instances_saved.png', dtype=torch.uint16)
        save_image(nocs_tensor, output_dir / f'{frame["omninocs_name"]}_nocs_saved.png', dtype=torch.float32)

        # Append to all_frames (Optional if you need to process the tensors later)
        all_frames.append((instance_tensor, nocs_tensor))
        
    return all_frames
