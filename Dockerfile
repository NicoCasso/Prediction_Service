FROM python:3.12-slim

WORKDIR /app

# Install dependencies for Azure SQL and ODBC driver
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    apt-transport-https \
    software-properties-common \
    curl \
    gnupg2 \
    build-essential \
    unixodbc-dev \
    libcurl4 \
    libssl3

# Remove conflicting ODBC packages
RUN apt-get remove --purge -y libodbc* libodbccr* unixodbc* && apt-get autoremove -y

# Install Microsoft ODBC Driver 18
RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg \
    && install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

# Configure ODBC
RUN echo "[ODBC Data Sources]" >> /etc/odbc.ini && \
    echo "AzureSQL = ODBC Driver 18 for SQL Server" >> /etc/odbc.ini && \
    echo "" >> /etc/odbc.ini && \
    echo "[AzureSQL]" >> /etc/odbc.ini && \
    echo "Driver=ODBC Driver 18 for SQL Server" >> /etc/odbc.ini && \
    echo "Server=madebayosqlserver.database.windows.net" >> /etc/odbc.ini && \
    echo "Database=ussba_db" >> /etc/odbc.ini && \
    echo "Uid=admin" >> /etc/odbc.ini && \
    echo "Pwd=ussba2025RBX" >> /etc/odbc.ini && \
    echo "Encrypt=yes" >> /etc/odbc.ini && \
    echo "TrustServerCertificate=no" >> /etc/odbc.ini

# Install wait-for-it.sh
RUN wget -O /wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /wait-for-it.sh

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    ODBCINI=/etc/odbc.ini \
    ACCEPT_EULA=Y

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Entry point with error handling and database wait
CMD ["sh", "-c", " \
    /wait-for-it.sh madebayosqlserver.database.windows.net:1433 -t 60 -- \
    alembic upgrade head || (echo 'Migrations failed. Retrying...' && sleep 5 && alembic upgrade head) && \
    python populate_db.py || (echo 'Data population failed. Retrying...' && sleep 5 && python populate_db.py) && \
    gunicorn -k uvicorn.workers.UvicornWorker -w 4 main:app --bind 0.0.0.0:80"]