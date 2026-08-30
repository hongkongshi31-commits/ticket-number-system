from flask import Flask, render_template_string, jsonify, redirect, request, url_for

app = Flask(__name__)

# -------------------------
# メモリ上で数値を管理（DBを使わないので超軽量・高速）
# -------------------------
current_number = 0  # 現在呼び出し中の番号

# -------------------------
# 客側ページ（/entry）
# -------------------------
@app.route("/entry")
def entry():
    html = """
    <html>
    <head>
        <title>番号表示</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                background-color: #FFF4A8;
                text-align: center;
                font-family: Arial, sans-serif;
                padding: 40px 20px;
            }
            .title {
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            .box {
                background: white;
                width: 90%;
                max-width: 350px;
                margin: 0 auto;
                padding: 30px 10px;
                border-radius: 30px;
                box-shadow: 0px 0px 20px rgba(0,0,0,0.15);
            }
            .num {
                font-size: 90px;
                font-weight: bold;
                color: #ff5722;
                margin: 10px 0;
            }
            .info {
                margin-top: 20px;
                font-size: 14px;
                color: #666;
                line-height: 1.6;
            }
        </style>
    </head>
    <body>
        <div class="title">3年3組<br>怪盗グルーのミニオン大救出</div>

        <div class="box">
            <div style="font-size: 18px; font-weight: bold;">現在呼び出し中</div>
            <div class="num" id="current">{{ num }}番</div>
        </div>

        <div class="info">
            手元の「紙の整理券」の番号が<br>
            <strong>この番号以下</strong>になったら受付へお越しください。<br>
            <br>
            <span style="font-size: 12px; color: #999;">※15秒ごとに自動で最新の状態に更新されます。</span>
        </div>

        <script>
        // サーバーへの負荷を下げるため、15秒に1回自動リロードする仕様に変更
        setTimeout(() => {
            window.location.reload();
        }, 15000);
        </script>

    </body>
    </html>
    """
    return render_template_string(html, num=current_number)

# -------------------------
# スタッフ用ページ（URLを変更して一般人のアクセスを防止）
# -------------------------
@app.route("/status-secret-333", methods=["GET", "POST"])
def status_page():
    global current_number
    
    if request.method == "POST":
        if "next" in request.form:
            current_number += 1
        elif "back" in request.form and current_number > 0:
            current_number -= 1
        elif "reset" in request.form:
            current_number = 0
        return redirect(url_for('status_page'))

    html = """
    <html>
    <head>
        <title>スタッフ用ページ</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                background-color: #F7E600;
                text-align: center;
                font-family: Arial, sans-serif;
                padding-top: 30px;
            }
            .number {
                font-size: 40px;
                font-weight: bold;
                margin-bottom: 20px;
            }
         .btn {
          background: #ffffff;      /* 白背景 */
          color: #000000;           /* 黒文字 */
          border: 3px solid #000000;
          padding: 20px;
          font-size: 30px;
          font-weight: bold;
          text-decoration: none;
          display: block;           /* ← これで縦に並ぶ */
          width: 300px;
          margin: 20px auto;
          text-align: center;
          border-radius: 10px;
        }



            .btn-danger {
                background: #ffcdd2;
                font-size: 16px;
                padding: 10px;
            }
        </style>
    </head>
    <body>
        <div class="number">現在の番号：{{ num }}</div>

        <form method="POST">
            <button class="btn" type="submit" name="next">次の番号へ進む (+1)</button>
            <button class="btn" type="submit" name="back" style="font-size:16px; padding:10px;">1つ戻す (-1)</button>
            <hr style="margin: 40px auto; width: 80%;">
            <button class="btn btn-danger" type="submit" name="reset" onclick="return confirm('本当にリセットしますか？');">番号を 0 にリセット</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html, num=current_number)

# -------------------------
# 旧URLを踏んだ人を自動転送
# -------------------------
@app.route("/status")
def old_status():
    return "このURLは使用されていません。スタッフ用ページは専用の隠しURLを開いてください。"

# -------------------------
# Render 用
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
