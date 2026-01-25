import machitan
import base64
import threading
from flask import Flask, request, render_template, redirect, url_for
import webview
import time

app = Flask(__name__)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Process POST request data
        n = request.files.get("file")
        with open("datastore", "r") as datastore:
            global a 
            a = int(datastore.read())
            outf=f"out_{a}.png"
        with open("datastore", "w") as datastore:
            datastore.truncate(0)
            datastore.write(f"{a + 1}")
            
        machitan.mamboify(n, outf)
        return redirect(url_for('success'))
    else:
        # Serve the form page for a GET request
        with open("mambo.jpg", "rb") as f: encoded = base64.b64encode(f.read()).decode("utf-8")
        return render_template('selection.html', front_image = encoded)

@app.route('/about', methods=['GET'])
def about():
    with open("mambo.jpg", "rb") as f: encoded = base64.b64encode(f.read()).decode("utf-8")
    return render_template('about.html', front_image = encoded)

@app.route('/success', methods=['GET'])
def success():
    time.sleep(0.1)
    with open("mambo.jpg", "rb") as f: encoded = base64.b64encode(f.read()).decode("utf-8")
    return render_template("transition.html", original_file="original.png", final_result = f"out_{a}.png")

def open_browser(): 
    webview.create_window("MamboAlgo v1.0.0", "http://127.0.0.1:5000/about")
    webview.start()

if __name__ == "__main__":
    # Run Flask in a separate thread so it doesn't block the GUI 
    flask_thread = threading.Thread(target=lambda: app.run()) 
    flask_thread.daemon = True 
    flask_thread.start()
    open_browser()