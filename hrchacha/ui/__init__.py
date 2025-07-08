CUSTOM_THEME = """
        <style>
            /* Right-aligned chat container */
            .main {
                display: flex;
                justify-content: flex-end;
            }
            
            /* Chat window styling */
            .chat-container {
                width: 400px;
                height: 600px;
                position: fixed;
                right: 20px;
                bottom: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
                z-index: 100;
            }
            
            /* Message area */
            .chat-messages {
                flex-grow: 1;
                overflow-y: auto;
                padding: 15px;
            }
            
            /* Input area */
            .chat-input {
                padding: 15px;
                border-top: 1px solid #eee;
            }
        </style>
        """