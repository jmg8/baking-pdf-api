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
    data = request.get_json()
    total_mass = data.get("totalMass")
    hydration = data.get("hydration")

    # Fill in template
    tex_filled = TEX_TEMPLATE.replace("{{totalMass}}", str(total_mass)).replace("{{hydration}}", str(hydration))

    # Save to temporary .tex file
    with tempfile.NamedTemporaryFile("w+", suffix=".tex", delete=False) as tex_file:
        tex_file.write(tex_filled)
        tex_file_path = tex_file.name

    # Compile with LaTeX.Online
    with open(tex_file_path, "rb") as f:
        try:
            response = requests.post(
                "https://latexonline.cc/data",
                files={"file": ("document.tex", f)},
                data={"compiler": "pdflatex"},
                timeout=10
            )
            response.raise_for_status()
        except Exception as e:
            print("PDF generation error:", e)
            return {"error": "PDF generation failed"}, 500


    if response.status_code == 200:
        pdf_path = tex_file_path.replace(".tex", ".pdf")
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(response.content)
        return send_file(pdf_path, mimetype="application/pdf", as_attachment=True, download_name="bread-recipe.pdf")
    else:
        return {"error": "PDF generation failed"}, 500
