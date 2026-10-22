from flask import Flask, render_template_string, request, redirect, url_for
import os
import random
import string

app = Flask(__name__)

# In-memory storage for v1
urls = {}

HTML = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener - v1</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f7fb; margin: 0; padding: 40px; }
        .card { max-width: 700px; margin: auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 8px 24px rgba(0,0,0,.08); }
        h1 { text-align: center; color: #1f2937; }
        form { display: flex; gap: 12px; margin-top: 18px; }
        input[type="text"] { flex: 1; padding: 12px 14px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 16px; }
        button { background: #2563eb; color: white; border: none; border-radius: 8px; padding: 12px 18px; font-size: 16px; cursor: pointer; }
        .result { margin-top: 25px; padding: 18px; border-radius: 8px; background: #eef2ff; color: #312e81; }
        .result a { color: #312e81; font-weight: bold; }
        .error { margin-top: 12px; color: #b91c1c; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h1>URL Shortener v1</h1>
        <form method="POST" action="/">
            <input type="text" name="url" placeholder="https://example.com" required>
            <button type="submit">Shorten</button>
        </form>
        {% if short_url %}
            <div class="result">
                Short link: <a href="{{ short_url }}" target="_blank">{{ short_url }}</a>
            </div>
        {% endif %}
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
'''


def generate_code(length=6):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    error = None

    if request.method == 'POST':
        original_url = request.form.get('url', '').strip()
        if not original_url:
            error = 'Please enter a URL.'
        else:
            if not original_url.startswith(('http://', 'https://')):
                original_url = 'https://' + original_url
            code = generate_code()
            while code in urls:
                code = generate_code()
            urls[code] = original_url
            short_url = request.host_url + code

    return render_template_string(HTML, short_url=short_url, error=error)


@app.route('/<code>')
def redirect_url(code):
    target = urls.get(code)
    if target:
        return redirect(target, code=302)
    return 'Not found', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
