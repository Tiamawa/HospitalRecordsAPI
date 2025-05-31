from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request, Form
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from slowapi.middleware import SlowAPIMiddleware
from datetime import timedelta
import os
from fastapi import FastAPI, File, UploadFile, Form, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, List
import json
from dotenv import load_dotenv
from uuid import uuid4
import time
from datetime import timedelta
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter, getLogger
from auth_utils import authenticate_user, create_access_token, verify_token, get_current_user
from database_query_utils import record_with_cni_admission_time, record_with_cni_crashId, record_with_crashId, record_within_admision_time

app = FastAPI()

class VictimRecord(BaseModel):
    cni: str
    crashId: str

class VictimRecordResponse(BaseModel):
    cni: str
    crashId: str
    severity: str
    recordId: str # hospital based
    admissionReason: str
    admissionTime: str
    diagnosis: str
    treatment: str
    finalStatus: str

load_dotenv() 
logger = logging.getLogger(__name__)
log_file_path=os.environ.get("HOSPITAL_RECORD_LOGGER", "logs/record_retrieval_logger.log")
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
fileHandler = RotatingFileHandler(log_file_path, maxBytes=5 * 1024 * 1024, backupCount=3)
    
formatter = Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)

# Securing API 2 : Add a global exception handler for rate limiting
# Initialize the Limiter
limiter = Limiter(key_func=get_remote_address)
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Rate limit exceeded. Please try again later."},
    )

#######
##### ENDPOINTS
#######

# Securing API 3 : Token endpoint
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Apply rate limiting to the /status endpoint
@app.get("/status")
@limiter.limit("5/minute")  # Allow 5 requests per minute per client
def get_status(request: Request):
    """
    Secured endpoint to check the status of the service.
    Requires a valid token for access.
    """
    return {"message": "Model Serving via FastAPI is running !"}

@app.post("/get_record_with_cni_admission_time", response_model=List[VictimRecordResponse])
@limiter.limit("10/minute")  # Allow 10 requests per minute per client
async def get_record_with_cni_admission_time(
        request: Request,
        cni: str = Form(...),
        interval_probable_admission_debut: str = Form(...),
        interval_probable_admission_fin: str = Form(...),
        crashId: Optional[str] = Form(None),
        current_user: dict = Depends(get_current_user)
):
    # Log the authenticated user
    logger.info(f"Record for cni:{cni} requested by user: {current_user['username']}")
    patients = record_with_cni_admission_time(
        cni=cni,
        interval_probable_admission_debut=interval_probable_admission_debut,
        interval_probable_admission_fin=interval_probable_admission_fin,
        crashId=crashId
    )
   # if not patients:
   #     raise HTTPException(
    #        status_code=status.HTTP_404_NOT_FOUND,
    #        detail="No records found for the given CNI and admission time interval."
    #    )
    return patients

@app.post("/get_record_with_cni_crashId", response_model=List[VictimRecordResponse])
@limiter.limit("10/minute")  # Allow 10 requests per minute per client
async def get_record_with_cni_crashId(
        request: Request,
        cni: str = Form(...),
        crashId:  str = Form(...),
        current_user: dict = Depends(get_current_user)
):
    """
    Endpoint to retrieve a patient's record based on their CNI and crash ID.
    """
    # Log the authenticated user
    logger.info(f"Record for cni:{cni} and crashId:{crashId} requested by user: {current_user['username']}")
    
    patient = record_with_cni_crashId(cni=cni, crashId=crashId)
    #if not patient:
    #    raise HTTPException(
    #        status_code=status.HTTP_404_NOT_FOUND,
    #        detail="No records found for the given CNI and crash ID."
    #    )
    
    return patient

@app.post("/get_record_with_crashId", response_model=List[VictimRecordResponse])
@limiter.limit("10/minute")  # Allow 10 requests per minute per client
async def get_record_with_crashId(
        request: Request,
        crashId:  str = Form(...),
        current_user: dict = Depends(get_current_user)
):
    """
    Endpoint to retrieve a patient's record based on their crash ID.
    """
    # Log the authenticated user
    logger.info(f"Records for crashId:{crashId} requested by user: {current_user['username']}")
    
    patients = record_with_crashId(crashId=crashId)
    #if not patients:
    #    raise HTTPException(
    #        status_code=status.HTTP_404_NOT_FOUND,
    #       detail="No patients found for the given crash ID."
    #    )
    
    return patients

@app.post("/get_record_within_admision_time", response_model=List[VictimRecordResponse])
@limiter.limit("10/minute")  # Allow 10 requests per minute per client
async def get_record_within_admision_time(
        request: Request,
        interval_probable_admission_debut: str = Form(...),
        interval_probable_admission_fin: str = Form(...),
        current_user: dict = Depends(get_current_user)
):
    """
    Endpoint to retrieve all patient records within the specified admission time interval.
    """
    # Log the authenticated user
    logger.info(f"Records requested for admission time interval: {interval_probable_admission_debut} to {interval_probable_admission_fin} by user: {current_user['username']}")
    
    patients = record_within_admision_time(
        interval_probable_admission_debut=interval_probable_admission_debut,
        interval_probable_admission_fin=interval_probable_admission_fin
    )
    
    # if not patients:
    #    raise HTTPException(
    #        status_code=status.HTTP_404_NOT_FOUND,
    #        detail="No records found within the specified admission time interval."
    #    )
    
    return patients
    

########
#### Middlewares
########

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Generate a unique request ID for tracking
    request_id = str(uuid4())
    
    # Log the start of the request
    logger.info(f"Request ID={request_id} - Start request: {request.method} {request.url}")
    
    # Record the start time
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate the processing time
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log the end of the request
    logger.info(
        f"Request ID={request_id} - Completed request: {request.method} {request.url} "
        f"Status code={response.status_code} - Process time={process_time:.4f}s"
    )
    
    return response