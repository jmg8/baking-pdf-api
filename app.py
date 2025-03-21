from flask import Flask, request, send_file
from flask_cors import CORS
import tempfile
import requests

app = Flask(__name__)
CORS(app, origins=["https://bakingcalculator.net"])

TEX_TEMPLATE = r"""
\documentclass{article}
\usepackage{booktabs}
\begin{document}
\section*{Bread Recipe}
\begin{tabular}{lr}
\toprule
Total Dough Mass & {{totalMass}} g \\
Hydration & {{hydration}} \% \\
\bottomrule
\end{tabular}
\end{document}
"""

@app.route("/generate", methods=["POST"])
def generate_pdf():
    print("🟢 Endpoint hit")
    data = request.get_json()

    try:
        total_mass = data.get("totalMass")
        hydration = data.get("hydration")
        print(f"🧪 Received input: totalMass={total_mass}, hydration={hydration}")
    except Exception as e:
        print("🔴 Error parsing input:", e)
        return {"error": "Invalid input"}, 400

    try:
        print("📄 Writing fake PDF to temp file")
        import tempfile
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_pdf.write(b"%PDF-1.4\n% Fake PDF content\n%%EOF")
        temp_pdf.close()

        print("✅ Returning fake PDF")
        return send_file(temp_pdf.name, mimetype="application/pdf", as_attachment=True, download_name="test.pdf")
    except Exception as e:
        print("🔥 Failed to simulate PDF:", e)
        return {"error": "PDF simulation failed"}, 500
