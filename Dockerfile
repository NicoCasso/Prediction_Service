FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# ajouté pour que la machine virtuelle utilisée pour le container ne parte pas en erreur
ENV DEBIAN_FRONTEND=noninteractive

COPY requirements.txt /app

#ajouté pour installer les librairies nécessaires à odbc 
# le -y est pour accepter les configurations par défaut
RUN apt-get update \
    && apt-get install -y apt-utils \ 
    && apt-get install -y libterm-readline-perl-perl \ 
    && apt-get install -y curl apt-transport-https ca-certificates gnupg \ 
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /usr/share/keyrings/microsoft-archive-keyring.gpg > /dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/ubuntu/20.04/prod focal main" | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc unixodbc-dev

RUN python -m venv /opt/.venv 

# permet d'éxécuter les pip install directement depuis /opt/.ven/bin,  
# sans avoir besoin de faire source opt/.venv/bin/activate
ENV PATH="opt/.venv/bin:$PATH"  

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

#documentation uniquement
EXPOSE 3100

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3100", "--reload"]
CMD ["gunicorn", "--bind", "0.0.0.0:3100", "main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "-w", "1"]