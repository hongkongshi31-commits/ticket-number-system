from flask import Flask, render_template_string, redirect
import os

app = Flask(__name__)

COUNTER_FILE = "counter.txt"
LIST_FILE = "list.txt"

# 初期化（ファイルが無ければ作る）
if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

if not os.path.exists(LIST_FILE):
    with open(LIST_FILE, "w") as f:
        f.write("")

# 番号を読み書きする関数
def read_counter():
    with open(COUNTER_FILE, "r") as f:
        return int(f.read().strip())

def write_counter(value):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(value))

def add_to_list(value):
    with open(LIST_FILE, "a") as f:
        f.write(str(value) + "\n")

def read_list():
    with open(LIST_FILE, "r") as f:
        return f.read().splitlines()

# -----------------------------
# ① 番号表示ページ（/entry）
# -----------------------------
@app.route("/entry")
def entry():
    number = read_counter()
    html = """
    <html>
    <head>
        <title>番号表示</title>
        <style>
            body {
                background-image: url('https://i.imgur.com/8QfQx7Z.jpeg');
                background-size: cover;
                background-position: center;
                text-align: center;
                color: black;
                font-family: Arial, sans-serif;
            }
            .number {
                font-size: 200px;
                font-weight: bold;
                margin-top: 150px;
            }
            .title {
                font-size: 40px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="title">3年3組　怪盗グルーのミニオン大救出</div>
        <div class="number">{{ num }}</div>
    </body>
    </html>
    """
    return render_template_string(html, num=number)

# -----------------------------
# ② 番号を進めるページ（/status）
# -----------------------------
@app.route("/status")
def status():
    number = read_counter() + 1
    write_counter(number)
    add_to_list(number)
    return redirect("/entry")

# -----------------------------
# ③ 番号リセット（/reset）
# -----------------------------
@app.route("/reset")
def reset():
    write_counter(0)
    with open(LIST_FILE, "w") as f:
        f.write("")
    return "番号をリセットしました！"

# -----------------------------
# ④ 番号一覧（/list）
# -----------------------------
@app.route("/list")
def list_page():
    numbers = read_list()
    html = """
    <html>
    <head>
        <title>番号一覧</title>
        <style>
            body {
                background-color: #f0f0f0;
                font-family: Arial;
                padding: 20px;
            }
            .box {
                background: white;
                padding: 20px;
                border-radius: 10px;
                width: 300px;
                margin: auto;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>番号一覧</h2>
            {% for n in nums %}
                <div>{{ n }}</div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, nums=numbers)

# -----------------------------
# Render 用
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

    app.run()
