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
                background-color: #FFF4A8;   /* ふんわり黄色 */
                text-align: center;
                font-family: 'Arial', sans-serif;
                padding-top: 80px;
            }

            .title {
                font-size: 40px;
                font-weight: bold;
                color: #333;
                margin-bottom: 30px;
            }

            .number-box {
                background: white;
                width: 300px;
                margin: 0 auto;
                padding: 40px;
                border-radius: 30px;
                box-shadow: 0px 0px 20px rgba(0,0,0,0.15);
            }

            .number {
                font-size: 180px;
                font-weight: bold;
                color: #000;
                line-height: 1;
            }
        </style>
    </head>
    <body>
        <div class="title">3年3組　怪盗グルーのミニオン大救出</div>

        <div class="number-box">
            <div class="number">{{ num }}</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, num=number)


# -----------------------------
# ② 番号を進めるページ（/status）
# -----------------------------
@app.route("/status")
def status_page():
    number = read_counter()
    html = """
    <html>
    <head>
        <title>スタッフ用ページ</title>
        <style>
            body {
                background-color: #F7E600;
                text-align: center;
                color: black;
                font-family: Arial, sans-serif;
                padding-top: 50px;
            }
            .number {
                font-size: 80px;
                font-weight: bold;
                margin-bottom: 40px;
            }
            .btn {
                display: block;
                width: 300px;
                margin: 20px auto;
                padding: 20px;
                font-size: 30px;
                font-weight: bold;
                background: white;
                border: 3px solid black;
                border-radius: 10px;
                color: black;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="number">現在の番号：{{ num }}</div>

        <a class="btn" href="/status/next">次の番号へ進む</a>
        <a class="btn" href="/reset">番号をリセット</a>
        <a class="btn" href="/list">番号一覧を見る</a>
    </body>
    </html>
    """
    return render_template_string(html, num=number)

@app.route("/status/next")
def status_next():
    number = read_counter() + 1
    write_counter(number)
    add_to_list(number)
    return redirect("/status")

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
    background-color: #F7E600;   /* ミニオンの黄色 */
    text-align: center;
    color: black;
    font-family: Arial, sans-serif;
}

.number {
    font-size: 200px;
    font-weight: bold;
    margin-top: 150px;
    color: black;
}

.title {
    font-size: 40px;
    margin-top: 20px;
    color: black;
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
