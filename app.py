from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# Route hiển thị giao diện chính
@app.route('/')
def home():
    return render_template('index.html')


# Route xử lý dữ liệu khi người dùng bấm nút "Analyze"
@app.route('/analyze', methods=['POST'])
def analyze_skills():
    data = request.get_json()
    user_skills = data.get('skills', '').upper()

    # Logic xử lý cơ bản (Sau này sẽ thay bằng module Recommendation của SP3)
    if not user_skills:
        return jsonify({"error": "Vui lòng nhập kỹ năng!"}), 400

    match_rate = "50%"
    missing_skill = "SystemVerilog, UVM"

    if "VERILOG" in user_skills:
        match_rate = "75%"
        missing_skill = "SystemVerilog"

    if "SYSTEMVERILOG" in user_skills:
        match_rate = "95%"
        missing_skill = "Thực hành dự án thực tế"

    # Trả kết quả về cho giao diện Web
    return jsonify({
        "match_rate": match_rate,
        "missing_skill": missing_skill
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)