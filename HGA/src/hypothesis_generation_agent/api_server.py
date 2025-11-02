

import logging
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our main crew class
from .crew import HypothesisGenerationAgentHgaCrew
from .config import setup_logging

# Setup logging for the API server
setup_logging()
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Hypothesis Generation Agent API",
    description="An API to run the HGA crew, designed for integration with Langflow.",
    version="1.1.0"
)

# --- CORS Middleware ---
# This is crucial! It allows the Langflow UI (on a different port) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you should restrict this to Langflow's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for Request/Response ---
class RunCrewRequest(BaseModel):
    """Defines the expected request body for running the crew."""
    business_problem: str

class RunCrewResponse(BaseModel):
    """Defines the structure of the successful response."""
    status: str
    result: str

class ErrorResponse(BaseModel):
    """Defines the structure of an error response."""
    status: str
    message: str

# --- API Endpoint ---
@app.post("/run-crew", response_model=RunCrewResponse, responses={500: {"model": ErrorResponse}})
def run_hga_crew(request: RunCrewRequest):
    """
    Accepts a business problem, runs the HGA crew, and returns the analysis.

    This endpoint is designed to be called by the Langflow CrewAI component.
    """
    logger.info(f"Received request to run crew for problem: '{request.business_problem}'")
    
    try:
        # Instantiate the crew
        hga_crew = HypothesisGenerationAgentHgaCrew()
        
        # Define the inputs for the crew
        inputs = {"business_problem": request.business_problem}
        
        # Kick off the crew execution
        result = hga_crew.kickoff(inputs=inputs)
        
        logger.info("Crew execution completed successfully.")
        return RunCrewResponse(status="success", result=result)

    except Exception as e:
        logger.error(f"An error occurred during crew execution: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")

# --- Health Check Endpoint ---
@app.get("/health")
def health_check():
    """A simple health check endpoint."""
    return {"status": "healthy"}

# To run this server directly from the command line for development:
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)