from flask import Flask, request, jsonify, render_template_string
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['endpoint'])

todos = [
    {"id": 1, "task": "Configure GitHub Actions CI", "status": "Completed"},
    {"id": 2, "task": "Build Docker Container", "status": "In Progress"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DevOps To-Do List Application</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #f8fafc; }
        .card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 600px; margin: auto; }
        h2 { color: #0f172a; text-align: center; }
        input, select, button { padding: 10px; margin: 8px 0; width: 100%; box-sizing: border-box; }
        button { background: #0284c7; color: white; border: none; font-weight: bold; cursor: pointer; border-radius: 4px; }
        button:hover { background: #0369a1; }
        ul { list-style: none; padding: 0; }
        li { padding: 12px; margin-bottom: 8px; background: #f1f5f9; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .Completed { background: #dcfce7; color: #166534; }
        .Pending { background: #fef9c3; color: #854d0e; }
        .In-Progress { background: #e0f2fe; color: #0369a1; }
    </style>
</head>
<body>
    <div class="card">
        <h2>To-Do List App (DevOps Pipeline)</h2>
        <form method="POST" action="/add">
            <input type="text" name="task" placeholder="Enter task title..." required>
            <select name="status">
                <option value="Pending">Pending</option>
                <option value="In-Progress">In Progress</option>
                <option value="Completed">Completed</option>
            </select>
            <button type="submit">Add Task</button>
        </form>

        <h3>Current Tasks</h3>
        <ul>
            {% for t in todos %}
            <li>
                <span><strong>#{{ t.id }}</strong> {{ t.task }}</span>
                <span class="badge {{ t.status }}">{{ t.status }}</span>
            </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    REQUEST_COUNT.labels(method='GET', endpoint='/', status='200').inc()
    return render_template_string(HTML_TEMPLATE, todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    status = request.form.get('status', 'Pending')
    new_todo = {
        "id": len(todos) + 1,
        "task": task,
        "status": status
    }
    todos.append(new_todo)
    REQUEST_COUNT.labels(method='POST', endpoint='/add', status='200').inc()
    return render_template_string(HTML_TEMPLATE, todos=todos)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    REQUEST_COUNT.labels(method='GET', endpoint='/api/todos', status='200').inc()
    return jsonify({"total": len(todos), "todos": todos}), 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)