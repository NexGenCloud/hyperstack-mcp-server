# Hyperstack MCP Server

A Model Context Protocol (MCP) server for managing Hyperstack infrastructure through natural language interactions. This server provides a comprehensive interface to Hyperstack's API, enabling automated infrastructure management through AI assistants.

## Features

- **Virtual Machine Management**: Create, manage, and monitor VMs
- **Volume Management**: Handle storage volumes and attachments
- **Floating IP Management**: Allocate and manage public IP addresses
- **Cluster Management**: Deploy and manage Kubernetes clusters
- **Billing & Usage**: Track costs and resource usage
- **Metadata Services**: Query available flavors, environments, and stock

## Architecture

- **Python 3.12**: Built with the latest stable Python version for optimal performance
- **uv Package Manager**: Ultra-fast Python package management with uv (10-100x faster than pip)
- **Ruff Linter**: Lightning-fast Python linting with Rust (100x faster than Flake8)
- **FastMCP Framework**: Built on FastMCP for robust MCP protocol support
- **AsyncIO-based Client**: High-performance async HTTP client with connection pooling
- **Pydantic v2 Models**: Strong type validation and serialization with latest Pydantic v2
- **Clean Architecture**: Modular design with separated concerns
- **Production-ready**: Docker support, health checks, and monitoring

## Prerequisites

- Python 3.12+
- Docker and Docker Compose (optional, for containerized deployment)
- Hyperstack API key
- uv package manager (will be installed automatically)

## Installation

The Hyperstack MCP Server can be deployed in three different modes:

### 1. Local Development (venv-based)

For quick iteration and development with hot reload:

1. Clone the repository:
```bash
git clone https://github.com/hyperstack/hyperstack-mcp-server.git
cd hyperstack-mcp-server
```

2. Set up development environment:
```bash
# Complete setup (installs uv if needed, creates venv, installs deps, configures pre-commit)
make setup

# Copy .env.example to .env and add your HYPERSTACK_API_KEY
cp .env.example .env

# Runs locally with hot reload (uv / venv-based)
make dev

# Quickly verify server is running
curl http://localhost:8080/health

# You should see:
{"status":"ok","service":"hyperstack-mcp-server","version":"0.1.0"}
```

### 2. Dev / Staging Deployment

Containerized environment for staging purposes (Docker-based):

1. Build the Docker image:
```bash
make build
```

2. Configure environment:
```bash
# Make sure .env.dev is configured
# This must have your HYPERSTACK_API_KEY
cat .env.dev
```

3. Run the dev (staging) container:
```bash
# Uses docker-compose.dev.yml overlay with hot reload
make docker-run MODE=dev
```

### 3. Production Deployment

Production-ready deployment (Docker-based):

1. Build the Docker image:
```bash
make build
```

1. Configure environment:
```bash
# Make sure .env.prod is configured
# This must have your HYPERSTACK_API_KEY
cat .env.prod
```

1. Run the production container:
```bash
# Uses docker-compose.prod.yml overlay with production ready launch config
make docker-run MODE=prod
```

## Configuration

Configuration is managed through environment variables. Different environment files are used for each deployment mode:

- **Local Development**: `.env` (copy from `.env.example`)
- **Docker Development**: `.env.dev`
- **Docker Production**: `.env.prod`

### Application Configuration

#### Required
- `HYPERSTACK_API_KEY`: Your Hyperstack API authentication key

#### Optional
- `ENVIRONMENT`: Environment mode (local/dev/prod)
- `HYPERSTACK_API_URL`: API base URL (default: https://infrahub-api.nexgencloud.com/v1)
- `LOG_LEVEL`: Logging level - lowercase for Docker (debug, info, warning, error)
- `LOG_FORMAT`: Log output format (json/text, default: text)

#### Connection Pool Settings
- `MAX_CONNECTIONS`: Maximum HTTP connections (default: 100)
- `MAX_KEEPALIVE_CONNECTIONS`: Maximum keep-alive connections (default: 50)
- `KEEPALIVE_EXPIRY`: Keep-alive connection expiry in seconds (default: 5)

#### Request Settings
- `REQUEST_TIMEOUT`: Default request timeout in seconds (default: 30)
- `MAX_RETRIES`: Maximum retry attempts (default: 3)
- `RETRY_BACKOFF_FACTOR`: Exponential backoff multiplier (default: 2.0)

#### Rate Limiting
- `RATE_LIMIT_ENABLED`: Enable rate limiting (default: true)
- `RATE_LIMIT_REQUESTS`: Maximum requests per minute (default: 100)

#### Python Settings
- `PYTHONDONTWRITEBYTECODE`: Prevent .pyc file creation (default: 1)
- `PYTHONUNBUFFERED`: Unbuffered stdout/stderr (default: 1)

### Docker-Specific Configuration

These variables are only used in Docker deployments (docker-compose.yml):

- `SERVER_HOST`: Server bind address (default: 0.0.0.0)
- `SERVER_PORT`: Server port (default: 8080)
- `SERVER_WORKERS`: Number of worker processes (default: 1 for dev, 4 for prod)
- `SERVER_KEEPALIVE_EXPIRY`: Uvicorn keep-alive timeout (default: 5)
- `SERVER_LIMIT_CONCURRENCY`: Maximum concurrent connections (default: 2000)

## Usage

### Starting the Server

```bash
# Local development with hot reload
make dev

# Docker development mode
make docker-run

# Docker production mode
make docker-run MODE=prod
```

### API Endpoints

The server provides the following HTTP endpoints:

- `GET /health` - Standard health check endpoint
- `GET /healthz` - Kubernetes-style health check endpoint
- `GET /tools` - List all registered MCP tools with their descriptions

### Available MCP Tools

The server exposes 44 MCP tools across 6 categories:

#### Virtual Machines (16 tools)
- `create_vm`: Create a new virtual machine
- `list_vms`: List all virtual machines
- `get_vm`: Get VM details
- `start_vm`: Start a VM
- `stop_vm`: Stop a VM
- `delete_vm`: Delete a VM
- `hard_reboot_vm`: Hard reboot a VM
- `hibernate_vm`: Hibernate a VM
- `restore_vm`: Restore a hibernated VM
- `get_vm_events`: Get VM event history
- `attach_volume_to_vm`: Attach a volume to a VM
- `detach_volume_from_vm`: Detach a volume from a VM
- `attach_floating_ip_to_vm`: Attach a floating IP to a VM
- `detach_floating_ip_from_vm`: Detach a floating IP from a VM
- `add_firewall_rule`: Add a firewall rule to a VM
- `remove_firewall_rule`: Remove a firewall rule from a VM

#### Volumes (7 tools)
- `create_volume`: Create a new volume
- `list_volumes`: List all volumes
- `get_volume`: Get volume details
- `update_volume`: Update volume properties
- `delete_volume`: Delete a volume
- `list_volume_types`: List available volume types
- `update_volume_attachment`: Update volume attachment properties

#### Floating IPs (6 tools)
- `allocate_floating_ip`: Allocate a new floating IP
- `list_floating_ips`: List all floating IPs
- `get_floating_ip`: Get floating IP details
- `associate_floating_ip`: Associate IP with VM
- `disassociate_floating_ip`: Disassociate IP from VM
- `release_floating_ip`: Release a floating IP

#### Clusters (5 tools)
- `create_cluster`: Create a new cluster
- `list_clusters`: List all clusters
- `get_cluster`: Get cluster details
- `delete_cluster`: Delete a cluster
- `get_cluster_events`: Get cluster events

#### Billing (5 tools)
- `get_billing_status`: Get billing account status
- `get_billing_usage`: Get usage for a period
- `get_previous_day_cost`: Get previous day's cost
- `get_credit_balance`: Get credit balance
- `get_payment_history`: Get payment history

#### Metadata (5 tools)
- `list_flavors`: List available instance types
- `get_flavor`: Get flavor details
- `list_environments`: List available regions
- `get_environment`: Get environment details
- `check_stock`: Check stock availability

## Development

### Code Quality

The project uses modern tools to maintain code quality:

- **Ruff**: Ultra-fast linting and import sorting (Rust-based)
- **Black**: Code formatting (works alongside Ruff)
- **mypy**: Static type checking

Run all checks:
```bash
make lint
```

Auto-format code:
```bash
make format
```

### Testing

Run tests:
```bash
# Run tests
make test

# Run tests with coverage report
make test COVERAGE=1
```

### Pre-commit Hooks

Pre-commit hooks are automatically installed during setup and run on each commit.

## Docker

### Multi-stage Build

The project uses a multi-stage Docker build for optimal image size:
- Stage 1: Builder - Compiles dependencies
- Stage 2: Runtime - Minimal runtime image

### Security Features

Production deployment includes enhanced security:
- Non-root user execution (UID 1000)
- Read-only filesystem (production only)
- Health checks with automatic restarts
- Resource limits (CPU and memory)
- No new privileges flag

## Makefile Commands

```bash
make help           # Show all available commands
make setup          # Complete development setup (installs uv, creates venv, installs deps)
make install-dev    # Install/update development dependencies
make lint           # Run all linting checks (ruff, black, mypy)
make format         # Auto-format code with ruff and black
make test           # Run tests (use COVERAGE=1 for coverage report)
make dev            # Run server locally with hot reload (venv-based)
make build          # Build Docker image
make build-no-cache # Build Docker image without cache
make docker-run     # Run in Docker (use MODE=dev|prod, default=dev)
make docker-down    # Stop and remove Docker containers
make clean          # Clean all generated files and Docker containers
```

### Examples:
```bash
# Initial setup
make setup
source .venv/bin/activate

# Development workflow
make format         # Format code
make lint           # Check code quality
make test           # Run tests
make dev            # Start local server

# Testing with coverage
make test COVERAGE=1

# Docker deployment
make build
make docker-run MODE=prod
```

## Project Structure

```
hyperstack-mcp-server/
├── src/
│   ├── server.py           # Main MCP server
│   ├── config.py           # Configuration management
│   ├── client/             # AsyncIO API client
│   │   ├── base.py         # Base HTTP client
│   │   └── hyperstack.py   # Hyperstack API client
│   ├── handlers/           # MCP action handlers
│   │   ├── virtual_machines.py
│   │   ├── volumes.py
│   │   ├── floating_ips.py
│   │   ├── clusters.py
│   │   ├── billing.py
│   │   └── metadata.py
│   ├── models/             # Pydantic models
│   └── exceptions.py       # Custom exceptions
├── tests/
├── docker/
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Commit with descriptive messages
6. Push and create a pull request

## License

MIT License - see [LICENSE](./LICENSE.txt) file for details

## Support

For issues and questions:
- GitHub Issues: [github.com/NexGenCloud/hyperstack-mcp-server/issues](https://github.com/NexGenCloud/hyperstack-mcp-server/issues)
- Documentation: [docs.hyperstack.cloud](https://docs.hyperstack.cloud)
