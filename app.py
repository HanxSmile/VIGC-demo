import vigc.common.download_models
import gradio as gr
import os
from vigc.common.demo_tools import inference, parse_arguments, prepare_models

EXAMPLE_ROOT = os.path.join(os.path.dirname(__file__), "examples")
ARTICLE = r"""
If VIGC is helpful, please help to ⭐ the <a href='https://github.com/opendatalab/VIGC' target='_blank'>Github Repo</a>. Thanks!
[![GitHub Stars](https://img.shields.io/github/stars/opendatalab/VIGC?style=social)](https://github.com/opendatalab/VIGC)

---

"""
if __name__ == '__main__':
    args = parse_arguments()
    all_models = prepare_models(args)
    inference = inference(all_models)

    with gr.Blocks() as demo:
        with gr.Column():
            empty_text_box = gr.Textbox(visible=False)
            with gr.Row().style(equal_height=False):
                with gr.Column():
                    model_type = gr.Radio(
                        choices=["MiniGPT4+", "InstructBlip"],
                        value="MiniGPT4+",
                        label="Model Type",
                        interactive=True,
                    )
                    image_input = gr.Image(type="pil")
                    with gr.Accordion("Parameters:", open=False):
                        with gr.Row().style(equal_height=True):
                            in_section = gr.Radio(
                                choices=["In Paragraph", "In Sentence"],
                                value="In Sentence",
                                label="Generate Style",
                                interactive=True
                            )

                            answer_length = gr.Slider(
                                minimum=1,
                                maximum=10,
                                value=4,
                                step=1,
                                interactive=True,
                                label="VIGC Iterations"
                            )

                        with gr.Row():
                            min_len = gr.Slider(
                                minimum=1,
                                maximum=50,
                                value=1,
                                step=1,
                                interactive=True,
                                label="Min Length",
                            )

                            max_len = gr.Slider(
                                minimum=10,
                                maximum=500,
                                value=250,
                                step=5,
                                interactive=True,
                                label="Max Length",
                            )
                        with gr.Row():
                            temperature = gr.Slider(
                                minimum=0.1,
                                maximum=1.0,
                                value=1.0,
                                step=0.1,
                                interactive=True,
                                label="Temperature",
                            )

                            beam_size = gr.Slider(
                                minimum=1,
                                maximum=10,
                                value=5,
                                step=1,
                                interactive=True,
                                label="Beam Size",
                            )
                    with gr.Accordion("Examples:"):
                        gr.Examples(
                            examples=[os.path.join(EXAMPLE_ROOT, _) for _ in os.listdir(EXAMPLE_ROOT) if
                                      _.startswith("example_")],
                            inputs=image_input,
                        )

                with gr.Column():
                    with gr.Column():
                        task = gr.Radio(
                            choices=["complex reasoning", "conversation", "detail description"],
                            value="conversation",
                            label="Task",
                            interactive=True,
                        )
                        gen_qa_button = gr.Button("Generate QA-pairs", variant="primary", size="sm")

                    text_output = gr.Textbox(label="Output:", lines=10)

            gr.Markdown(ARTICLE)
            gen_qa_button.click(
                fn=inference,
                inputs=[image_input, empty_text_box, task, min_len, max_len, beam_size, temperature,
                        answer_length, in_section, model_type],
                outputs=text_output
            )

    demo.launch(share=True, enable_queue=True, server_name="0.0.0.0", debug=True)
