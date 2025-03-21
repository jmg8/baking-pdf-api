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

    # Simulate a PDF response for testing without LaTeX
    try:
        print("📄 Simulating fake PDF generation")
        pdf_content = b"%PDF-1.4\n% Fake PDF\n%%EOF"
        pdf_path = "/tmp/fake.pdf"
        with open(pdf_path, "wb") as f:
            f.write(pdf_content)
        return send_file(pdf_path, mimetype="application/pdf", as_attachment=True, download_name="test.pdf")
    except Exception as e:
        print("🔥 Failed to simulate PDF:", e)
        return {"error": "PDF simulation failed"}, 500

