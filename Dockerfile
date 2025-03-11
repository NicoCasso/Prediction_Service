FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app

#ajouté pour installer les librairies nécessaires à odbc
RUN apt-get update && apt-get install -y curl apt-transport-https ca-certificates gnupg && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /usr/share/keyrings/microsoft-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/ubuntu/20.04/prod focal main" | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc unixodbc-dev

RUN python -m venv /opt/.venv
# je ne sais sincèrement pas à quoi sert cette ligne
# ENV PATH="opt/.venv/bin:$PATH"  

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

#documentation uniquement
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3100", "--reload"]