FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Set PYTHONPATH to include /app
ENV PYTHONPATH=/app

# Create the logs directory
RUN mkdir -p /app/logs

# Copy the requirements file
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "serve_hospital_records:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]