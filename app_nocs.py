import json
import os
import functools
import numpy as np
from PIL import Image
import gradio as gr
from render import render, Model
import math
import tempfile
from pathlib import Path
import open3d as o3d

class NOCSVisualizer:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()

    def render_axis(self, rotation_matrix, translation_vector, image_size=(512, 512)):
        # Use the render function to draw the axis
        euler_angles = cv2.RQDecomp3x3(rotation_matrix)[0]
        phi = math.radians(euler_angles[2])
        theta = math.radians(euler_angles[1])
        gamma = math.radians(euler_angles[0])

        height, width = image_size
        img = render(
            self.axis_model,
            height=height,
            width=width,
            filename="tmp_render.png",
            cam_loc=[-240 * math.cos(phi), 
                     -240 * math.tan(theta), 
                      240 * math.sin(phi)]
        )

        img = img.rotate(math.degrees(gamma))
        return img

def load_metadata(metadata_path: str):
    """Load the metadata from JSON file."""
    with open(metadata_path, 'r') as file:
        metadata = json.load(file)
    return metadata

def process_image_from_metadata(metadata, image_base_path, nocs_visualizer):
    """Process each entry in metadata and generate 3D axis."""
    result_paths = []
    for i, entry in enumerate(metadata[:5]):  # Process first 5 entries
        image_name = entry["image_name"]
        rotation_matrix = np.array(entry["objects"][0]["rotation"])
        translation_vector = np.array(entry["objects"][0]["translation"])

        # Construct image path
        image_path = os.path.join(image_base_path, f"{image_name}.png")
        input_image = Image.open(image_path)

        # Render the 3D axis
        axis_image = nocs_visualizer.render_axis(rotation_matrix, translation_vector, image_size=input_image.size)

        # Composite the result with the original image
        result_image = Image.alpha_composite(input_image.convert('RGBA'), axis_image)
        
        result_path = f"/tmp/result_{i}.png"
        result_image.save(result_path)
        result_paths.append(result_path)

    return result_paths

def create_demo():
    # Paths for metadata and images
    metadata_path = "/baai-cwm-1/baai_cwm_ml/algorithm/chongjie.ye/data/OmniNOCS/annotations/v1_0/omninocs_release_objectron/objectron_train_metadata.json"
    image_base_path = "/baai-cwm-1/baai_cwm_ml/algorithm/chongjie.ye/data/OmniNOCS/OmniNOCS_Objectron/train/book/batch-1/20/img"

    # Load metadata and setup NOCS visualizer
    metadata = load_metadata(metadata_path)
    nocs_visualizer = NOCSVisualizer()

    # Create Gradio interface
    demo = gr.Blocks(
        title="Stable Nocs Estimation with Predefined Metadata",
        css="""
            .slider .inner { width: 5px; background: #FFF; }
            .viewport { aspect-ratio: 4/3; }
            .tabs button.selected { font-size: 20px !important; color: crimson !important; }
            h1, h2, h3 { text-align: center; display: block; }
            .md_feedback li { margin-bottom: 0px !important; }
        """
    )

    with demo:
        gr.Markdown("""This demo shows rendered 3D axes on the first 5 images from metadata.""")

        with gr.Tabs() as tabs:
            with gr.Tab("3D Axis Rendering"):
                with gr.Row():
                    with gr.Column():
                        submit_btn = gr.Button("Render Axes for First 5 Images", variant="primary")
                    with gr.Column():
                        result_output = gr.Gallery(label="Rendered Axes", type="image", show_label=False)

                submit_btn.click(
                    fn=lambda: process_image_from_metadata(metadata, image_base_path, nocs_visualizer),
                    outputs=[result_output]
                )

    return demo

def main():
    demo = create_demo()
    demo.queue(api_open=False).launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )

if __name__ == "__main__":
    main()
