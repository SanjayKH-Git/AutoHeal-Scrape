from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def original_page():
    return render_template("original.html")

@app.route("/updated")
def updated_page():
    return render_template("updated.html")

if __name__ == "__main__":
    app.run(debug=True)
    