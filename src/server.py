"""Main MCP server implementation for Hyperstack."""

import logging

import structlog

# Import handler modules (they will auto-register with FastMCP)
from src.handlers import (  # noqa: F401
    billing,
    clusters,
    metadata,
    virtual_machines,
    volumes,
)

from .config import settings
from .mcp_instance import mcp

# This is needed for libraries that use stdlib logging (like uvicorn, aiohttp, etc.)
# The simple format is used because structlog will handle the actual formatting
logging.basicConfig(level=getattr(logging, settings.log_level))

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        (
            structlog.processors.JSONRenderer()
            if settings.log_format == "json"
            else structlog.dev.ConsoleRenderer()
        ),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

# Get logger
logger = structlog.get_logger()


# Initialize server at module load
logger.info(
    "Initializing Hyperstack MCP Server",
    log_level=settings.log_level,
)

# Validate configuration at module load time
if not settings.hyperstack_api_key:
    logger.warning("HYPERSTACK_API_KEY environment variable is not set")

# Create the HTTP app for uvicorn
app = mcp.http_app()
