import os
import json
import shutil

# Root directories
root_dir = "/mnt/data/OmniNOCS"
image_root = os.path.join(root_dir, "extracted_frames")  # Root directory for image_name
nocs_root = os.path.join(root_dir, "annotations/v1_0/omninocs_release_objectron")  # Root directory for omninocs_name and metadata files
output_root = os.path.join(root_dir, "OmniNOCS_Objectron")  # Root directory for output

# Metadata files for train, test, and val
metadata_files = {
    "train": os.path.join(nocs_root, "objectron_train_metadata.json"),
    "test": os.path.join(nocs_root, "objectron_test_metadata.json"),
    "val": os.path.join(nocs_root, "objectron_val_metadata.json")
}

# Create the output root directory and subfolders for train, test, and val
for split in metadata_files.keys():
    os.makedirs(os.path.join(output_root, split), exist_ok=True)

# Process each metadata file
for split, metadata_file in metadata_files.items():
    # Read the metadata file
    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    # Iterate through each entry in the metadata
    for entry in metadata:
        # Get image_name and omninocs_name
        image_name = entry["image_name"]
        omninocs_name = entry["omninocs_name"]

        # Build the full paths for the image, NOCS map, and instance map
        image_path = os.path.join(image_root, f"{image_name}.png")
        nocs_map_path = os.path.join(nocs_root, f"{omninocs_name}_nocs.png")
        instance_map_path = os.path.join(nocs_root, f"{omninocs_name}_instances.png")

        # Build the target folder paths under the corresponding split folder
        base_folder = os.path.join(output_root, split, os.path.dirname(image_name))
        img_folder = os.path.join(base_folder, "img")
        nocs_map_folder = os.path.join(base_folder, "nocs_map")
        instance_folder = os.path.join(base_folder, "instances")

        # Create the target folders
        os.makedirs(img_folder, exist_ok=True)
        os.makedirs(nocs_map_folder, exist_ok=True)
        os.makedirs(instance_folder, exist_ok=True)

        # Build the target file paths
        img_target_path = os.path.join(img_folder, os.path.basename(image_path))
        nocs_map_target_path = os.path.join(nocs_map_folder, os.path.basename(nocs_map_path))
        instance_target_path = os.path.join(instance_folder, os.path.basename(instance_map_path))

        # Copy the image, NOCS map, and instance map to the target folders
        if os.path.exists(image_path):
            shutil.copy(image_path, img_target_path)
            print(f"Copied image: {image_path} -> {img_target_path}")
        else:
            print(f"Image file does not exist: {image_path}")

        if os.path.exists(nocs_map_path):
            shutil.copy(nocs_map_path, nocs_map_target_path)
            print(f"Copied NOCS map: {nocs_map_path} -> {nocs_map_target_path}")
        else:
            print(f"NOCS map file does not exist: {nocs_map_path}")

        if os.path.exists(instance_map_path):
            shutil.copy(instance_map_path, instance_target_path)
            print(f"Copied instance map: {instance_map_path} -> {instance_target_path}")
        else:
            print(f"Instance map file does not exist: {instance_map_path}")

print("Processing complete!")