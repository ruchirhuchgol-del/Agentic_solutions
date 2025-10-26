"""API Gateway for GitHub Profile Optimizer microservices."""
from flask import Flask, request, jsonify
from ..utils.logger import get_logger
from ..auth.tenant_manager import tenant_manager


app = Flask(__name__)
logger = get_logger("api_gateway")


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "api-gateway"
    }), 200


@app.route("/optimize/<tenant_id>", methods=["POST"])
def optimize_profile(tenant_id: str):
    """Optimize GitHub profile for a tenant."""
    try:
        # Validate tenant
        if not tenant_manager.get_tenant_config(tenant_id):
            return jsonify({"error": "Tenant not found"}), 404
        
        # Get request data
        data = request.get_json()
        github_handle = data.get("github_handle")
        
        if not github_handle:
            return jsonify({"error": "github_handle is required"}), 400
        
        # In a real implementation, this would forward to the profile service
        # For now, we'll return a mock response
        return jsonify({
            "status": "success",
            "message": f"Optimization job started for {github_handle}",
            "job_id": f"job_{tenant_id}_{github_handle}"
        }), 202
        
    except Exception as e:
        logger.error(f"Error in optimize_profile: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/analyze/<tenant_id>", methods=["POST"])
def analyze_profile(tenant_id: str):
    """Analyze GitHub profile for a tenant."""
    try:
        # Validate tenant
        if not tenant_manager.get_tenant_config(tenant_id):
            return jsonify({"error": "Tenant not found"}), 404
        
        # Get request data
        data = request.get_json()
        github_handle = data.get("github_handle")
        
        if not github_handle:
            return jsonify({"error": "github_handle is required"}), 400
        
        # In a real implementation, this would forward to the profile service
        # For now, we'll return a mock response
        return jsonify({
            "status": "success",
            "message": f"Analysis job started for {github_handle}",
            "job_id": f"analysis_{tenant_id}_{github_handle}"
        }), 202
        
    except Exception as e:
        logger.error(f"Error in analyze_profile: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/tenants", methods=["GET"])
def list_tenants():
    """List all tenants."""
    try:
        tenants = tenant_manager.list_tenants()
        return jsonify({
            "tenants": tenants
        }), 200
    except Exception as e:
        logger.error(f"Error in list_tenants: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)