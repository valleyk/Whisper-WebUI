import gradio as gr
from modules.whisper_Inference import WhisperInference
from modules.nllb_inference import NLLBInference
import os
from ui.htmls import *
from modules.youtube_manager import get_ytmetas
import argparse

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--share', type=bool, default=False, nargs='?', const=True,
                    help='Share value')
args = parser.parse_args()


def open_folder(folder_path):
    if os.path.exists(folder_path):
        os.system(f"start {folder_path}")
    else:
        print(f"The folder {folder_path} does not exist.")


def on_change_models(model_size):
    translatable_model = ["large", "large-v1", "large-v2"]
    if model_size not in translatable_model:
        return gr.Checkbox.update(visible=False, value=False, interactive=False)
    else:
        return gr.Checkbox.update(visible=True, value=False, label="Translate to English?", interactive=True)


whisper_inf = WhisperInference()
nllb_inf = NLLBInference()
block = gr.Blocks(css=CSS).queue(api_open=False)

with block:
    with gr.Row():
        with gr.Column():
            gr.Markdown(MARKDOWN, elem_id="md_project")
    with gr.Tabs():
        with gr.TabItem("File"):  # tab1
            with gr.Row():
                input_file = gr.Files(type="file", label="Upload File here")
            with gr.Row():
                dd_model = gr.Dropdown(choices=whisper_inf.available_models, value="large-v2", label="Model")
                # dd_model = gr.Dropdown(choices=whisper_inf.available_models, value="medium", label="Model")
                dd_lang = gr.Dropdown(choices=["Automatic Detection"] + whisper_inf.available_langs,
                                      value="Automatic Detection", label="Language")
                dd_subformat = gr.Dropdown(["SRT", "WebVTT"], value="SRT", label="Subtitle Format")
            with gr.Row():
                cb_translate = gr.Checkbox(value=False, label="Translate to English?", interactive=True)
            with gr.Row():
                btn_run = gr.Button("GENERATE SUBTITLE FILE", variant="primary")
            with gr.Row():
                tb_indicator = gr.Textbox(label="Output")
                btn_openfolder = gr.Button('📂').style(full_width=False)

            btn_run.click(fn=whisper_inf.transcribe_file,
                          inputs=[input_file, dd_model, dd_lang, dd_subformat, cb_translate], outputs=[tb_indicator])
            btn_openfolder.click(fn=lambda: open_folder("outputs"), inputs=None, outputs=None)
            dd_model.change(fn=on_change_models, inputs=[dd_model], outputs=[cb_translate])

        with gr.TabItem("Youtube"):  # tab2
            with gr.Row():
                tb_youtubelink = gr.Textbox(label="Youtube Link")
            with gr.Row().style(equal_height=True):
                with gr.Column():
                    img_thumbnail = gr.Image(label="Youtube Thumbnail")
                with gr.Column():
                    tb_title = gr.Label(label="Youtube Title")
                    tb_description = gr.Textbox(label="Youtube Description", max_lines=15)
            with gr.Row():
                dd_model = gr.Dropdown(choices=whisper_inf.available_models, value="large-v2", label="Model")
                dd_lang = gr.Dropdown(choices=["Automatic Detection"] + whisper_inf.available_langs,
                                      value="Automatic Detection", label="Language")
                dd_subformat = gr.Dropdown(choices=["SRT", "WebVTT"], value="SRT", label="Subtitle Format")
            with gr.Row():
                cb_translate = gr.Checkbox(value=False, label="Translate to English?", interactive=True)
            with gr.Row():
                btn_run = gr.Button("GENERATE SUBTITLE FILE", variant="primary")
            with gr.Row():
                tb_indicator = gr.Textbox(label="Output")
                btn_openfolder = gr.Button('📂').style(full_width=False)

            btn_run.click(fn=whisper_inf.transcribe_youtube,
                          inputs=[tb_youtubelink, dd_model, dd_lang, dd_subformat, cb_translate],
                          outputs=[tb_indicator])
            tb_youtubelink.change(get_ytmetas, inputs=[tb_youtubelink],
                                  outputs=[img_thumbnail, tb_title, tb_description])
            btn_openfolder.click(fn=lambda: open_folder("outputs"), inputs=None, outputs=None)
            dd_model.change(fn=on_change_models, inputs=[dd_model], outputs=[cb_translate])

        with gr.TabItem("Mic"):  # tab3
            with gr.Row():
                mic_input = gr.Microphone(label="Record with Mic", type="filepath", interactive=True)
            with gr.Row():
                dd_model = gr.Dropdown(choices=whisper_inf.available_models, value="large-v2", label="Model")
                dd_lang = gr.Dropdown(choices=["Automatic Detection"] + whisper_inf.available_langs,
                                      value="Automatic Detection", label="Language")
                dd_subformat = gr.Dropdown(["SRT", "WebVTT"], value="SRT", label="Subtitle Format")
            with gr.Row():
                cb_translate = gr.Checkbox(value=False, label="Translate to English?", interactive=True)
            with gr.Row():
                btn_run = gr.Button("GENERATE SUBTITLE FILE", variant="primary")
            with gr.Row():
                tb_indicator = gr.Textbox(label="Output")
                btn_openfolder = gr.Button('📂').style(full_width=False)

            btn_run.click(fn=whisper_inf.transcribe_mic,
                          inputs=[mic_input, dd_model, dd_lang, dd_subformat, cb_translate], outputs=[tb_indicator])
            btn_openfolder.click(fn=lambda: open_folder("outputs"), inputs=None, outputs=None)
            dd_model.change(fn=on_change_models, inputs=[dd_model], outputs=[cb_translate])

        with gr.TabItem("T2T Translation"):  # tab 4
            with gr.Row():
                file_subs = gr.Files(type="file", label="Upload Subtitle Files to translate here",
                                     file_types=['.vtt', '.srt'])

            with gr.TabItem("NLLB"):  # sub tab1
                with gr.Row():
                    dd_nllb_model = gr.Dropdown(label="Model", value=nllb_inf.default_model_size,
                                                choices=nllb_inf.available_models)
                    dd_nllb_sourcelang = gr.Dropdown(label="Source Language", choices=nllb_inf.available_source_langs)
                    dd_nllb_targetlang = gr.Dropdown(label="Target Language", choices=nllb_inf.available_target_langs)
                with gr.Row():
                    btn_run = gr.Button("TRANSLATE SUBTITLE FILE", variant="primary")
                with gr.Row():
                    tb_indicator = gr.Textbox(label="Output")
                    btn_openfolder = gr.Button('📂').style(full_width=False)
                with gr.Column():
                    md_vram_table = gr.HTML(NLLB_VRAM_TABLE, elem_id="md_nllb_vram_table")

            btn_run.click(fn=nllb_inf.translate_file,
                          inputs=[file_subs, dd_nllb_model, dd_nllb_sourcelang, dd_nllb_targetlang],
                          outputs=[tb_indicator])
            btn_openfolder.click(fn=lambda: open_folder("outputs\\translations"), inputs=None, outputs=None)

if args.share:
    block.launch(share=True)
else:
    block.launch(server_name="0.0.0.0", show_error=True, enable_queue=True, server_port=7860)
