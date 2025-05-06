from flask import Flask, request, jsonify
import language_tool_python

app = Flask(__name__)

# استخدام الخادم العام لـ LanguageTool
tool = language_tool_python.LanguageToolPublicAPI('fr')

@app.route('/correct', methods=['POST'])
def correct_text():
    data = request.get_json()
    text = data.get("text", "")

    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)

    return jsonify({
        "original": text,
        "corrected": corrected_text,
        "errors": len(matches)
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
