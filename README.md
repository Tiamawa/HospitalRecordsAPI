
#### Commands to launch the api
```bash
conda create --name doctoral python=3.10
conda activate doctoral
pip install -r requirements.txt
```

#### API documentation 

http://localhost:8000/docs#/

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