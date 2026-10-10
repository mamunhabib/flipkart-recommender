from flask import Flask
from app.routes import main_bp
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

def create_app(rag_chain):
    # 1. Initialize the Flask Web Server
    app = Flask(__name__)
    
    # 2. Inject the AI Brain into the server's memory so the URLs can use it
    app.config['RAG_CHAIN'] = rag_chain
    
    # 3. Register our web URLs (the routes)
    app.register_blueprint(main_bp)
    
    # 4. Attach the /metrics endpoint for Grafana/Prometheus Observability
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })
    
    return app
