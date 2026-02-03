import gradio as gr
import json
from typing import Tuple
from services.user_service import UserService

# Global state for managing user sessions
user_service = None
session_username = "default_user"  # Can be replaced with actual user authentication

def launch():
    """Launch the Gradio UI"""
    global user_service
    
    # Initialize user service
    user_service = UserService(session_username)
    initial_message = user_service.get_initial_message()
    
    with gr.Blocks(title="Anton - AI Companion") as demo:
        gr.Markdown("""
        # 🤖 Anton - Your AI Companion
        
        Welcome to Hytribe's Anton chatbot! Complete 7 days of onboarding to help us understand you better.
        """)
        
        with gr.Row():
            with gr.Column(scale=3):
                # Chat interface
                chatbot = gr.Chatbot(
                    value=[{"role": "assistant", "content": initial_message}],
                    label="Chat with Anton",
                    height=500
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Type your message here...",
                        label="Your Message",
                        lines=2
                    )
                
                with gr.Row():
                    send_btn = gr.Button("Send Message", variant="primary", scale=2)
                    mark_day_btn = gr.Button("Mark Day Complete", variant="secondary", scale=1)
                
                with gr.Row():
                    export_btn = gr.Button("Export My Data (JSON)", variant="secondary")
                
                export_output = gr.Textbox(
                    label="Exported Data",
                    interactive=False,
                    visible=False,
                    lines=10
                )
            
            with gr.Column(scale=1):
                # User status panel
                gr.Markdown("### Your Progress")
                
                status_display = gr.Textbox(
                    value=json.dumps(user_service.get_user_status(), indent=2),
                    label="Status",
                    interactive=False,
                    lines=10
                )
                
                progress_slider = gr.Slider(
                    minimum=0,
                    maximum=100,
                    value=0,
                    interactive=False,
                    label="Days Completed (%)"
                )
        
        # Event handlers
        def send_message(user_input, history):
            """Send message handler"""
            if not user_input or user_input.strip() == "":
                status = user_service.get_user_status()
                progress = ((status["onboarding_step"] - 1) / 7 if not status["onboarding_complete"] else 1.0) * 100
                return history, json.dumps(status, indent=2), gr.update(value=progress)
            
            response, show_mark_button = user_service.process_user_message(user_input)
            
            # Format for new Gradio Chatbot format
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
            
            status = user_service.get_user_status()
            progress = ((status["onboarding_step"] - 1) / 7 if not status["onboarding_complete"] else 1.0) * 100
            
            return history, json.dumps(status, indent=2), gr.update(value=progress)
        
        def mark_complete(history):
            """Mark day complete handler"""
            message, is_complete = user_service.mark_day_complete()
            
            # Format for new Gradio Chatbot format
            history.append({"role": "assistant", "content": message})
            
            status = user_service.get_user_status()
            progress = ((status["onboarding_step"] - 1) / 7 if not status["onboarding_complete"] else 1.0) * 100
            
            return history, json.dumps(status, indent=2), gr.update(value=progress)
        
        def export_data():
            """Export data handler"""
            data = user_service.export_user_data()
            return json.dumps(data, indent=2)
        
        # Connect button events
        send_btn.click(
            fn=send_message,
            inputs=[msg, chatbot],
            outputs=[chatbot, status_display, progress_slider]
        ).then(
            lambda: "",
            None,
            msg
        )
        
        mark_day_btn.click(
            fn=mark_complete,
            inputs=[chatbot],
            outputs=[chatbot, status_display, progress_slider]
        )
        
        export_data_output = export_btn.click(
            fn=export_data,
            outputs=[export_output]
        )
        
        export_data_output.then(
            lambda x: gr.update(visible=True),
            export_output,
            export_output
        )
        
        # Allow Enter key to send message
        msg.submit(
            fn=send_message,
            inputs=[msg, chatbot],
            outputs=[chatbot, status_display, progress_slider]
        ).then(
            lambda: "",
            None,
            msg
        )
    
    demo.launch(debug=True, share=True)

if __name__ == "__main__":
    launch()
