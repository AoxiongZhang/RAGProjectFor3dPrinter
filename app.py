import gradio as gr
from service import Service

def printer_bot(message, history):
    service = Service()
    return service.answer(message, history)

css = '''
.gradio-container { max-width: 850px !important; margin: 20px auto !important;}
.message { padding: 10px !important; font-size: 14px !important;}
'''

demo = gr.ChatInterface(
    fn=printer_bot,
    title='3D Printer Handbook Assistant',
    theme=gr.themes.Default(spacing_size='sm', radius_size='sm'),
    examples=[
        "What is stringing in 3D printing?",
        "How can I reduce oozing on my prints?",
        "What are the main causes of stringing?",
    ],
    chatbot=gr.Chatbot(height=400, type='messages'),  # type='messages' is recommended
    textbox=gr.Textbox(placeholder="Type your 3D printer question here...", container=False, scale=7),
#    submit_btn=gr.Button('Submit', variant='primary'),
#    clear_btn=gr.Button('Clear History', variant='secondary'),
    css=css
)

if __name__ == '__main__':
    demo.launch(share=True)

