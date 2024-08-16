from flask import Flask, render_template_string
from threading import Thread
from typing import Optional
import time
import sys
import os

app = Flask(__name__)
start_time = time.time()


@app.route('/')
def root() -> str:
    """
    Route handler for the root URL. Returns a simple HTML page with a floating box
    animation, a status message, and details about the running script and runtime.
    """
    # Get the filename of the running script
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

    # Calculate the runtime
    runtime = time.time() - start_time

    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LimitlessLumos</title>
        <link href="https://fonts.googleapis.com/css2?family=MedievalSharp:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: 'MedievalSharp', serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(135deg, #0a0a0a, #1e1e1e);
                color: #f0f0f0;
                overflow: hidden;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
            }}

            .box {{
                width: 120px;
                height: 120px;
                background: radial-gradient(circle, #f0f0f0, #a0a0a0);
                border-radius: 20px;
                animation: float 3s ease-in-out infinite;
                box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
            }}

            @keyframes float {{
                0%, 100% {{
                    transform: translateY(0);
                }}
                50% {{
                    transform: translateY(-20px);
                }}
            }}

            .status {{
                margin: 20px;
                font-size: 22px;
                color: #f0c674;
                cursor: pointer;
                transition: color 0.3s ease, text-shadow 0.3s ease;
            }}

            .status:hover {{
                color: #ffcc00;
                text-shadow: 0 0 15px rgba(255, 255, 255, 0.6);
            }}

            .info {{
                margin: 10px;
                font-size: 18px;
                color: #e0e0e0;
            }}

            .copyright {{
                position: absolute;
                bottom: 20px;
                text-align: center;
                width: 100%;
                font-size: 14px;
                color: #b0b0b0;
                text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
            }}
        </style>
    </head>
    <body>
        <div class="box"></div>
        <div class="status" onclick="window.location.href='https://traxdinosaur.github.io';">
            Server is running
        </div>
        <div class="info">
            Running File: <strong>{script_name}</strong><br>
            Runtime: <strong id="runtime"></strong>
        </div>
        <div class="copyright">
            &copy;2024 TraxDinosaur. All rights reserved.
        </div>

        <script>
            // Initial runtime passed from the server in seconds
            let runtime = {int(runtime)};

            // Function to format time
            function formatTime(seconds) {{
                let hours = Math.floor(seconds / 3600);
                let minutes = Math.floor((seconds % 3600) / 60);
                let secs = Math.floor(seconds % 60);
                let timeStr = '';
                if (hours > 0) {{
                    timeStr += hours + ' hours ';
                }}
                if (minutes > 0 || hours > 0) {{
                    timeStr += minutes + ' minutes ';
                }}
                timeStr += secs + ' seconds';
                return timeStr;
            }}

            // Update the runtime every second
            function updateRuntime() {{
                runtime += 1;
                document.getElementById('runtime').innerText = formatTime(runtime);
            }}

            // Start the timer
            setInterval(updateRuntime, 1000);

            // Initialize the timer with the initial runtime
            document.getElementById('runtime').innerText = formatTime(runtime);
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)


def run(host: str = '127.0.0.1', port: Optional[int] = None) -> None:
    """
    Starts the Flask application on the specified host and port.

    Args:
        host (str): The hostname to listen on (default is '127.0.0.1').
        port (Optional[int]): The port to listen on (default is None, which uses the Flask default).
    """
    app.run(host=host, port=port)


def lumosServer(host: Optional[str] = None, port: Optional[int] = None) -> None:
    """
    Initializes and starts the Flask server on a separate thread.

    Args:
        host (Optional[str]): The hostname to listen on. Use 'All' or 'all' to listen on all network interfaces.
        port (Optional[int]): The port to listen on. If None, the default port is used.
    """
    if host is None and port is None:
        t = Thread(target=run)
        t.start()
    elif host == 'All' or host == 'all':
        t = Thread(target=run, args=('0.0.0.0', None))
        t.start()
    else:
        t = Thread(target=run, args=(host, port))
        t.start()


if __name__ == '__main__':
    lumosServer()
