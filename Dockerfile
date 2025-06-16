FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Streamlit
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
