from flask import Flask, render_template_string
from threading import Thread

app = Flask(__name__)


@app.route('/')
def root():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LimitlessLumos</title>
        <link href="https://fonts.googleapis.com/css2?family=MedievalSharp:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {
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
            }

            .box {
                width: 120px;
                height: 120px;
                background: radial-gradient(circle, #f0f0f0, #a0a0a0);
                border-radius: 20px;
                animation: float 3s ease-in-out infinite;
                box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
            }

            @keyframes float {
                0%, 100% {
                    transform: translateY(0);
                }
                50% {
                    transform: translateY(-20px);
                }
            }

            .status {
                margin: 20px;
                font-size: 22px;
                color: #f0c674;
                cursor: pointer;
                transition: color 0.3s ease, text-shadow 0.3s ease;
            }

            .status:hover {
                color: #ffcc00;
                text-shadow: 0 0 15px rgba(255, 255, 255, 0.6);
            }

            .copyright {
                position: absolute;
                bottom: 20px;
                text-align: center;
                width: 100%;
                font-size: 14px;
                color: #b0b0b0;
                text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
            }
        </style>
    </head>
    <body>
        <div class="box"></div>
        <div class="status" onclick="window.location.href='https://traxdinosaur.github.io';">
            Server is running
        </div>
        <div class="copyright">
            &copy;2024 TraxDinosaur. All rights reserved.
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)


def run():
    app.run(host='0.0.0.0')


def lumosServer():
    t = Thread(target=run)
    t.start()


if __name__ == '__main__':
    lumosServer()
