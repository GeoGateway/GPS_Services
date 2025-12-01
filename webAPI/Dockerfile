# Use Micromamba base image
FROM mambaorg/micromamba:latest

# Switch to root user for setup
USER root

# Install ca-certificates and other dependencies
RUN apt-get update && \
    apt-get install -y ca-certificates curl wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy environment file
COPY environment.yml .

# Install packages from environment.yml using micromamba
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes

# Create static directory with proper permissions BEFORE copying files
RUN mkdir -p /app/static /app/localdata && \
    chown -R $MAMBA_USER:$MAMBA_USER /app

# Copy application files
COPY --chown=$MAMBA_USER:$MAMBA_USER . .

# Ensure permissions are correct after copying (in case static folder was copied)
RUN chown -R $MAMBA_USER:$MAMBA_USER /app/static /app/localdata && \
    chmod -R 755 /app/static /app/localdata

# Switch back to non-root user
USER $MAMBA_USER

# Expose port 5000 (default Flask port)
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=GPS_service_API.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV MAMBA_DOCKERFILE_ACTIVATE=1

# Run the Flask application with micromamba using shell form
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
