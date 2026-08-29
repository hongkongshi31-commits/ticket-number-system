from flask import Flask, render_template_string, jsonify, redirect
import sqlite3

app = Flask(__name__)

# -------------------------
# DB 接続
# -------------------------
def get_db():
    conn = sqlite3.connect('queue.db')
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------
# DB 初期化
# -------------------------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    # 受付番号テーブル
    cur.execute('''
        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 呼び出し番号テーブル（1行だけ）
    cur.execute('''
        CREATE TABLE IF NOT EXISTS current_number (
            number INTEGER
        )
    ''')

    # 初期値がなければ 0 を入れる
    cur.execute('SELECT COUNT(*) FROM current_number')
    if cur.fetchone()[0] == 0:
        cur.execute('INSERT INTO current_number (number) VALUES (0)')

    conn.commit()
    conn.close()

init_db()

# -------------------------
# QR読み込み → 番号発行
# -------------------------
@app.route('/get_number')
def get_number():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('INSERT INTO queue DEFAULT VALUES')
    conn.commit()

    new_id = cur.lastrowid

    conn.close()
    return jsonify({"number": new_id})

# -------------------------
# 客側ページ
# -------------------------
@app.route("/entry")
def entry():
    html = """
    <html>
    <head>
        <title>番号表示</title>
        <style>
            body {
                background-color: #FFF4A8;
                text-align: center;
                font-family: Arial, sans-serif;
                padding-top: 80px;
            }
            .title {
                font-size: 40px;
                font-weight: bold;
                margin-bottom: 30px;
            }
            .box {
                background: white;
                width: 300px;
                margin: 0 auto;
                padding: 40px;
                border-radius: 30px;
                box-shadow: 0px 0px 20px rgba(0,0,0,0.15);
            }
            .num {
                font-size: 150px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="title">3年3組　怪盗グルーのミニオン大救出</div>

        <div class="box">
            <div>あなたの番号</div>
            <div class="num" id="myNumber"></div>
        </div>

        <div class="box" style="margin-top:40px;">
            <div>現在呼び出し中</div>
            <div class="num" id="current"></div>
        </div>

        <div style="margin-top:30px; font-size:30px;">
            あと <span id="diff"></span> 人であなたの番です
        </div>

        <script>
        let my = localStorage.getItem('myNumber');

        if (!my) {
            fetch('/get_number')
              .then(res => res.json())
              .then(data => {
                localStorage.setItem('myNumber', data.number);
                document.getElementById('myNumber').innerText = data.number;
              });
        } else {
            document.getElementById('myNumber').innerText = my;
        }

        setInterval(() => {
          fetch('/current')
            .then(res => res.json())
            .then(data => {
              document.getElementById('current').innerText = data.current;

              const my = localStorage.getItem('myNumber');
              if (my) {
                const diff = my - data.current;
                document.getElementById('diff').innerText = diff;
              }
            });
        }, 2000);
        </script>

    </body>
    </html>
    """
    return render_template_string(html)

# -------------------------
# 現在呼び出し番号（JSON）
# -------------------------
@app.route('/current')
def current():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('SELECT number FROM current_number')
    current = cur.fetchone()['number']

    conn.close()
    return jsonify({"current": current})

# -------------------------
# スタッフ用ページ
# -------------------------
@app.route("/status")
def status_page():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('SELECT number FROM current_number')
    number = cur.fetchone()['number']

    cur.execute('SELECT COUNT(*) AS total FROM queue')
    total = cur.fetchone()['total']

    conn.close()

    html = """
    <html>
    <head>
        <title>スタッフ用ページ</title>
        <style>
            body {
                background-color: #F7E600;
                text-align: center;
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
                text-decoration: none;
                color: black;
            }
        </style>
    </head>
    <body>
        <div class="number">現在の番号：{{ num }}</div>
        <div class="number">受付済み人数：{{ total }}人</div>

        <a class="btn" href="/status/next">次の番号へ進む</a>
        <a class="btn" href="/reset">番号をリセット</a>
    </body>
    </html>
    """
    return render_template_string(html, num=number, total=total)

# -------------------------
# 次へ進む
# -------------------------
@app.route("/status/next")
def status_next():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('UPDATE current_number SET number = number + 1')
    conn.commit()

    conn.close()
    return redirect("/status")

# -------------------------
# リセット
# -------------------------
@app.route("/reset")
def reset():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('UPDATE current_number SET number = 0')
    conn.commit()

    cur.execute('DELETE FROM queue')
    conn.commit()

    conn.close()
    return """
番号をリセットしました！
<br><br>
<a href="/status">スタッフ画面に戻る</a>
"""

# -------------------------
# Render 用
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

