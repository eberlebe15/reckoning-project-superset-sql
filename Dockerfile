FROM apache/superset:2.1.0

USER root

# Install AWS CLI and jq
RUN apt-get update && apt-get install -y awscli jq

# Create the log directory and set permissions
RUN mkdir -p /var/log/superset && \
    chown -R superset:superset /var/log/superset

# Copy requirements.txt
COPY requirements.txt /app/requirements.txt

# Install additional dependencies
RUN pip install -r /app/requirements.txt

# Copy application files
COPY /logo /app/logo
COPY superset_config.py /app/superset_config.py
COPY superset-init.sh /app/superset-init.sh
# COPY dashboards /app/dashboards

# Ensure the initialization script is executable
RUN chmod +x /app/superset-init.sh

# Switch back to the non-root user
USER superset

# Entrypoint to run the init script and start the server
ENTRYPOINT ["sh", "/app/superset-init.sh"]
