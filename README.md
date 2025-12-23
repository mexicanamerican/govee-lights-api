## Govee Lights API Docker Configuration

This directory contains a complete Docker setup for the Govee Lights API application that can be easily deployed with Portainer.

### Files

1. `Dockerfile` - Containerizes the Python application
2. `docker-compose.yml` - Defines the service configuration
3. `.env.example` - Example environment variables template

### How to Use with Portainer

1. Create a folder named `govee-lights-api` in your Docker host or Portainer volume.
2. Copy the `govee-lights-api.zip` file to this folder.
3. Copy the contents of this directory to the same folder.
4. Rename `.env.example` to `.env` and update it with your Govee API key.
5. In Portainer, select "Stacks" and click "Add stack".
6. Choose the "Web editor" method and paste the content of `docker-compose.yml`.
7. Give your stack a name (e.g., "govee-lights-api") and deploy.

### Environment Variables

- `GOVEE_API_KEY` (required) - Your Govee Developer API key
- `GOVEE_BASE_URL` (optional) - Govee API base URL (default provided)

### Port Mappings

- Host port 8000 maps to container port 8000

### Access

Once deployed, the API will be available at `http://<your-host-ip>:8000`
The interactive API documentation will be available at `http://<your-host-ip>:8000/docs`