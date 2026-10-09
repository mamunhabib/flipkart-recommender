from flask import Blueprint, render_template, request, Response, current_app
from prometheus_client import Counter, generate_latest

# Create a Blueprint (a modular collection of routes)
main_bp = Blueprint('main', __name__)

# Prometheus Metric Tracker
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests to the Frontend")

@main_bp.route("/")
def index():
    """Loads the main chat webpage."""
    REQUEST_COUNT.inc()
    return render_template("index.html")

@main_bp.route("/get", methods=["POST"])
def get_response():
    """Receives the user's chat message and sends it to the AI Brain."""
    user_input = request.form["msg"]
    
    # Safely pull the AI Brain out of the server's memory
    rag_chain = current_app.config['RAG_CHAIN']
    
    # Ask the AI the question! (The session_id triggers our Redis Memory)
    response = rag_chain.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "user-session"}} 
    )["answer"]
    
    return response

@main_bp.route("/metrics")
def metrics():
    """Exposes server metrics for Grafana monitoring."""
    return Response(generate_latest(), mimetype="text/plain")
