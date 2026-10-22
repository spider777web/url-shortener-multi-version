from flask import Flask, render_template_string, request, redirect
import os
import random
import string

app = Flask(__name__)

# In-memory storage for v2
urls = {}

HTML = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener - v2</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #eef2ff, #f8fafc); padding: 40px; }
        .card { max-width: 720px; margin: auto; background: white; border-radius: 14px; padding: 30px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08); }
        h1 { text-align: center; color: #0f172a; }
        form { display: flex; gap: 12px; margin-top: 20px; }
        input[type="text"] { flex: 1; padding: 12px 14px; border: 1px solid #cbd5e1; border-radius: 10px; }
        button { background: #0f766e; color: white; border: none; border-radius: 10px; padding: 12px 18px; font-weight: bold; cursor: pointer; }
        .result { margin-top: 22px; padding: 16px 18px; background: #ecfeff; color: #115e59; border-radius: 10px; }
        .result a { color: #0f766e; font-weight: bold; }
        .error { color: #b91c1c; margin-top: 14px; font-weight: bold; }
        .links { margin-top: 18px; }
        .links a { color: #1d4ed8; }
    </style>
</head>
<body>
    <div class="card">
        <h1>URL Shortener v2</h1>
        <form method="POST" action="/">
            <input type="text" name="url" placeholder="Enter original URL" required>
            <button type="submit">Create Short Link</button>
        </form>
        {% if short_url %}
            <div class="result">
                Your short link: <a href="{{ short_url }}" target="_blank">{{ short_url }}</a>
            </div>
        {% endif %}
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <div class="links">
            <p>Total links: <strong>{{ total_links }}</strong></p>
        </div>
    </div>
</body>
</html>
'''

urls = {}

def generate_code(length=6):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    error = None
    total_links = len(urls)

    if request.method == 'POST':
        original_url = request.form.get('url', '').strip()
        if not original_url:
            error = 'URL cannot be empty.'
        else:
            if not original_url.startswith(('http://', 'https://')):
                original_url = 'https://' + original_url
            code = generate_code()
            while code in urls:
                code = generate_code()
            urls[code] = original_url
            short_url = request.host_url + code
            total_links = len(urls)

    return render_template_string(HTML, short_url=short_url, error=error, total_links=total_links)


@app.route('/<code>')
def redirect_url(code):
    target = urls.get(code)
    if target:
        return redirect(target, code=302)
    return 'Not found', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
