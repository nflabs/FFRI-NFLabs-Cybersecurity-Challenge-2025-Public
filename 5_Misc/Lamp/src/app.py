import unicodedata
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

CORRECT_PIN = "24"
FLAG = "flag{pico_gpio_master}"

def normalize_input(pin: str) -> str:
    if not pin:
        return ""
    # 前後の空白を削除
    pin = pin.strip()
    # 全角文字を半角に正規化
    pin = unicodedata.normalize("NFKC", pin)
    # 中に含まれるスペース（全角/半角とも）を削除
    pin = pin.replace(" ", "").replace("　", "")
    return pin

@app.route("/", methods=["GET", "POST"])
def index():
    if "attempts" not in session:
        session["attempts"] = 0
        session["locked"] = False
        session["solved"] = False

    result = ""
    led_on = False

    if session.get("solved"):
        led_on = True
        result = f"正解済み！FLAG: {FLAG}"

    elif request.method == "POST":
        if session["locked"]:
            result = "回答回数の上限に達しました。"
        else:
            raw_pin = request.form.get("pin")
            pin = normalize_input(raw_pin)   # ← 入力を正規化

            session["attempts"] += 1
            if pin == CORRECT_PIN:
                led_on = True
                result = f"正解！FLAG: {FLAG}"
                session["solved"] = True
            else:
                if session["attempts"] >= 3:
                    session["locked"] = True
                    result = "回答回数の上限に達しました。"
                else:
                    remaining = 3 - session["attempts"]
                    result = f"不正解です。残り試行回数: {remaining} 回"

    return render_template("index.html", result=result, led_on=led_on)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)