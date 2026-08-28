from flask import Flask, render_template_string
import os

app = Flask(__name__)

COUNTER_FILE = "counter.txt"

# 番号ファイルがなければ作成
if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

def get_current_number():
    with open(COUNTER_FILE, "r") as f:
        return int(f.read().strip())

def increment_number():
    num = get_current_number() + 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(num))
    return num

# 番号を大きく表示するHTMLテンプレート
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>番号表示</title>
    <style>
        body {
            background-color: #f7f7f7;
            text-align: center;
            font-family: Arial, sans-serif;
        }
        .number-box {
            margin-top: 120px;
            font-size: 160px;
            font-weight: bold;
            color: #333;
        }
        .label {
            font-size: 40px;
            margin-top: 20px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="label">{{ label }}</div>
    <div class="number-box">{{ number }}</div>
</body>
</html>
"""

@app.route("/entry")
def entry():
    new_number = increment_number()
    return render_template_string(HTML_TEMPLATE, label="あなたの番号", number=new_number)

@app.route("/status")
def status():
    return render_template_string(HTML_TEMPLATE, label="現在の番号", number=get_current_number())

@app.route("/")
def home():
    return "前売り番号発行システム稼働中"

if __name__ == "__main__":
    app.run()
