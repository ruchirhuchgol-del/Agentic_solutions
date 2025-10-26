"""
Web server for the DevSecOps Deployment Gatekeeper.
Provides health check and metrics endpoints.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import logging
from typing import Dict, Any
from .health import get_health_status, get_metrics
from .config.settings import settings
from .utils.logger import get_logger

logger = get_logger(__name__)

class HealthCheckHandler(BaseHTTPRequestHandler):
    """HTTP request handler for health check endpoints."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/health":
            self._handle_health_check()
        elif self.path == "/metrics":
            self._handle_metrics()
        else:
            self._handle_not_found()
    
    def _handle_health_check(self):
        """Handle health check request."""
        try:
            health_status = get_health_status()
            status_code = 200 if health_status["status"] == "healthy" else 503
            
            self._send_json_response(status_code, health_status)
            logger.info(f"Health check request completed with status {status_code}")
            
        except Exception as e:
            logger.error(f"Error handling health check: {str(e)}")
            self._send_json_response(500, {"error": str(e)})
    
    def _handle_metrics(self):
        """Handle metrics request."""
        try:
            metrics = get_metrics()
            self._send_json_response(200, metrics)
            logger.info("Metrics request completed")
            
        except Exception as e:
            logger.error(f"Error handling metrics request: {str(e)}")
            self._send_json_response(500, {"error": str(e)})
    
    def _handle_not_found(self):
        """Handle not found requests."""
        self._send_json_response(404, {"error": "Not found"})
    
    def _send_json_response(self, status_code: int, data: Dict[str, Any]):
        """Send JSON response."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to use our logger."""
        logger.info(f"{self.address_string()} - {format % args}")

class HealthCheckServer:
    """Simple HTTP server for health checks and metrics."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8090):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Start the health check server."""
        try:
            self.server = HTTPServer((self.host, self.port), HealthCheckHandler)
            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.daemon = True
            self.thread.start()
            
            logger.info(f"Health check server started on {self.host}:{self.port}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start health check server: {str(e)}")
            return False
    
    def stop(self):
        """Stop the health check server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            logger.info("Health check server stopped")
    
    def is_running(self) -> bool:
        """Check if the server is running."""
        return self.thread is not None and self.thread.is_alive()

def start_health_server():
    """Start the health check server as a background thread."""
    if not settings.enable_metrics:
        logger.info("Metrics server is disabled")
        return None
    
    server = HealthCheckServer(port=settings.metrics_port)
    if server.start():
        return server
    else:
        return None

if __name__ == "__main__":
    # Run the server when executed directly
    server = HealthCheckServer()
    if server.start():
        try:
            logger.info("Press Ctrl+C to stop the server")
            while True:
                pass
        except KeyboardInterrupt:
            logger.info("Shutting down server...")
            server.stop()
    else:
        logger.error("Failed to start server")
        exit(1)