from flask import Flask, render_template, request, jsonify, send_file
from chatbot.logic import get_bot_response
from chatbot.chart_gen import generate_chart
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    response, chart_paths = get_bot_response(user_msg)

    chart_urls = []
    for path in chart_paths:
        chart_urls.append(f"/chart/{os.path.basename(path)}")

    return jsonify({"response": response, "charts": chart_urls})

@app.route('/chart/<filename>')
def serve_chart(filename):
    return send_file(f"static/charts/{filename}", mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
