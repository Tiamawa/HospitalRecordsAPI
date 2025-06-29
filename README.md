# FastAPI Hospital Records

This project is a FastAPI application designed to manage hospital records, including victim information related to crashes. It provides a RESTful API for interacting with the data.

## Project Structure

- `serve_hospital_records.py`: Contains the FastAPI application code, defining API endpoints, data models, and integrating authentication and database query utilities.
- `requirements.txt`: Lists the Python dependencies required for the FastAPI application to run.
- `Dockerfile`: Instructions to build a Docker image for the FastAPI application.
- `README.md`: Documentation for the project.

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-hospital-records
   ```

2. **Create a virtual environment (optional but recommended):**
```bash
conda deactivate
conda create --name doctoral python=3.10
conda activate doctoral

```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
  ```bash
  uvicorn serve_hospital_records:app --reload --host 0.0.0.0 --port 8000
  ```

## Usage

Once the application is running, you can access the API at `http://127.0.0.1:8000`. The API documentation is available at `http://127.0.0.1:8000/docs`.

## Docker Instructions

To build and run the Docker container, use the following commands:

1. **Build the Docker image:**
   ```
   docker build -t fastapi-hospital-records .
   ```

2. **Run the Docker container:**
   ```
   docker run -d --name hospital-records -p 8000:8000 -v ./logs:/app/logs fastapi-hospital-records
   ```

3. Use of .env 
Below informations must be present on you .env file : 

- HOSPITAL_RECORD_LOGGER="/app/logs/record_retrieval_logger.log"
- SERVING_SECRET_KEY="your_key_here"
- SERVING_ALGORITHM="algo_"
- SERVING_ACCESS_TOKEN_EXPIRE_MINUTES=30

#### EndPoints

##### Request to get a token
```bash
curl -X 'POST' \
  'http://localhost:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=admin_cadappar&password=43SoYourAreADataEngineer34&scope=&client_id=string&client_secret=string'
```

`Response`
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl9jYWRhcHBhciIsImV4cCI6MTc0ODcyMzMxN30.cosCZ0vokkNuQZE2SBQCAgZ0NbjcXvztDUVK9r9X7yI",
  "token_type": "bearer"
}

###### Get crashes victims for a given crash identification : 
```bash
curl -X 'POST' \
  'http://localhost:8000/get_record_with_crashId' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl9jYWRhcHBhciIsImV4cCI6MTc0ODcyMTU4M30.NMWI-MM92TLRmqio_T1p4EjEB2dwrzxAxKWfN69A-NI' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'crashId=crash789'
```
`Response`
[
  {
    "cni": "456789123",
    "crashId": "crash789",
    "severity": "minor",
    "recordId": "record789",
    "admissionReason": "Road Crash",
    "admissionTime": "2023-10-03T09:15:00Z",
    "diagnosis": "Minor injuries",
    "treatment": "Rest and medication",
    "finalStatus": "recovered"
  }
]

##### Get crashes victims for a given admission time interval :
```bash
curl -X 'POST' \
  'http://localhost:8000/get_record_with_cni_admission_time' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl9jYWRhcHBhciIsImV4cCI6MTc0ODcyMjkxNH0.t2-0xmeeylwIlDjPeNVt1o3P6R-ejI60OPX3uyvfPog' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'cni=789123456&interval_probable_admission_debut=2023-10-06T09%3A00%3A00Z&interval_probable_admission_fin=2023-10-06T11%3A00%3A00Z&crashId=crash303'
```

`Response`
[
  {
    "cni": "789123456",
    "crashId": "crash303",
    "severity": "minor",
    "recordId": "record303",
    "admissionReason": "Road Crash",
    "admissionTime": "2023-10-06T10:00:00Z",
    "diagnosis": "Bruises and cuts",
    "treatment": "First aid and observation",
    "finalStatus": "recovered"
  }
]

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.