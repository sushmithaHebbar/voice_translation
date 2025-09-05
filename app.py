from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    """Serves the main web page."""
    return render_template('index.html')

@app.route('/history')
def get_history():
    """Reads and returns the content of the history file."""
    try:
        with open('history.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain'}
    except FileNotFoundError:
        return "", 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    # Run the Flask server
    app.run(debug=True)