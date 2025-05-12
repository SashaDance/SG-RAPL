import gradio as gr
import os
import json
from PIL import Image

# Move box 998 from shelf 1 to free shelf

EXAMPLE_IMAGE_PATH = "data/wp0.png"
EXAMPLE_SEG_JSON_PATH =  "data/wp0.json"
EXAMPLE_PLANNER_JSON_PATH = "data/planner_output.json"
WIDTH = 720
HEIGHT = 540 

def create_placeholder_image():
    if os.path.exists(EXAMPLE_IMAGE_PATH):
        image = Image.open(EXAMPLE_IMAGE_PATH).convert("RGB")
        image = image.resize((WIDTH, HEIGHT))  # Resize for display
    else:
        image = Image.new("RGB", (WIDTH, HEIGHT), color="lightgray")
    return image

def update_actual_state():
    with open(EXAMPLE_SEG_JSON_PATH) as f:
        json_data = json.load(f)
        boxes_output = json_data['boxes_output']
    output = "Boxes state:"
    for box_output in boxes_output:
        output += "\n"
        output += f"{box_output}"
    return output

def run_planner_list(command, state):
    with open(EXAMPLE_PLANNER_JSON_PATH) as f:
        json_data = json.load(f)
        plan = json_data['plan']
    if command.strip() == "":
        return []
    table_data = []
    for step in plan:
        table_data.append([step["name"], str(step["args"])])
    return table_data

with gr.Blocks(title="Robot Pipeline Demo") as demo:
    gr.Markdown("## Robot Pipeline Demo")
    
    with gr.Row():
        perception_image = gr.Image(
            value=create_placeholder_image(),
            label="Perception Module Output",
            interactive=False,
            show_label=True,
            width=WIDTH,
            height=HEIGHT
        )
    
    with gr.Row():
        update_btn = gr.Button("Update Actual State")
        state_output = gr.Textbox(label="Current Actual State", interactive=False)
    
    with gr.Row():
        command_input = gr.Textbox(
            label="Enter Text Command",
            placeholder="e.g., 'Pick up box 215 from shelf 1 and drop it on shelf 4'"
        )
    
    with gr.Row():
        planner_output = gr.Dataframe(
            headers=["Command", "Arguments"],
            label="Planner Module Output",
            interactive=False,
            wrap=True
        )
    
    update_btn.click(fn=update_actual_state, inputs=None, outputs=state_output)
    command_input.submit(fn=run_planner_list, inputs=[command_input, state_output], outputs=planner_output)

demo.launch()
