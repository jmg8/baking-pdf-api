from flask import Flask, request, send_file
from flask_cors import CORS
import tempfile
import requests

app = Flask(__name__)
CORS(app, origins=["https://bakingcalculator.net"])  # ✅ CORS is working now

@app.route("/generate", methods=["POST"])
def generate_pdf():
    print("🟢 /generate endpoint hit")
    data = request.get_json()

    try:
        total_mass = data.get("totalMass")
        hydration = data.get("hydration")
        print(f"🧪 Received: totalMass={total_mass}, hydration={hydration}")
    except Exception as e:
        print("🔴 Error parsing input:", e)
        return {"error": "Invalid input"}, 400

    # 🔧 Step 1: Fill in a basic LaTeX template
    latex_content = rf"""
    \documentclass{{article}}
    \begin{{document}}
    \section*{{Basic Bread Recipe}}
    Total dough mass: {total_mass} g\\
    Hydration: {hydration}\%\\
    \end{{document}}
    """

    try:
        # 🔧 Step 2: Write the LaTeX content to a temp .tex file
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".tex", delete=False) as tex_file:
            tex_file.write(latex_content)
            tex_file_path = tex_file.name

        # 🔧 Step 3: Compile with LaTeX.Online
        print("📤 Sending LaTeX to compiler...")
        with open(tex_file_path, "rb") as f:
            response = requests.post(
                "https://latexonline.cc/data",
                files={"file": ("document.tex", f)},
                data={"compiler": "pdflatex"},
                timeout=25
            )
            response.raise_for_status()

        # 🔧 Step 4: Save compiled PDF
        print("📥 Saving compiled PDF...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
            pdf_file.write(response.content)
            pdf_path = pdf_file.name

        print("✅ PDF ready, sending to user")
        return send_file(pdf_path, mimetype="application/pdf", as_attachment=True, download_name="bread-recipe.pdf")

    except Exception as e:
        print("🔥 PDF generation error:", e)
        return {"error": "PDF generation failed"}, 500
