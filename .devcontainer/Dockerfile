FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04 
  
USER root 
  
RUN apt-get update && apt-get install -y \ 
    curl \ 
    git \ 
    postgresql-client \ 
    python3 \ 
    python3-pip \ 
    python3-venv \ 
    nodejs \ 
    npm \ 
    less \ 
    nano \ 
    vim \ 
    jq \ 
    && rm -rf /var/lib/apt/lists/* 
  
USER vscode 