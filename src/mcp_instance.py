"""Shared MCP instance for the Hyperstack server."""

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

# Initialize FastMCP server
mcp = FastMCP("Hyperstack MCP Server")


# Add health check endpoints using custom routes
@mcp.custom_route("/health", methods=["GET"])
async def health_check(_request: Request) -> JSONResponse:
    """Health check endpoint for monitoring."""
    return JSONResponse(
        {
            "status": "ok",
            "service": "hyperstack-mcp-server",
            "version": "0.1.0",
        }
    )


@mcp.custom_route("/healthz", methods=["GET"])
async def healthz_check(_request: Request) -> JSONResponse:
    """Kubernetes-style health check endpoint."""
    return JSONResponse(
        {
            "status": "ok",
            "service": "hyperstack-mcp-server",
            "version": "0.1.0",
        }
    )


@mcp.custom_route("/tools", methods=["GET"])
async def list_tools(_request: Request) -> JSONResponse:
    """List all registered MCP tools."""
    # Get the tools using the async method
    tools = await mcp.get_tools()
    tools_info = []

    for tool_name, tool in tools.items():
        # Debug: Check the actual structure of tool_data
        tools_info.append(
            {
                "name": tool_name,
                "title": tool.title or "No title provided",
                "description": tool.description or "No description provided",
                "input_schema": tool.parameters or "No input schema provided",
                "output_schema": tool.output_schema or "No output schema provided",
            }
        )

    return JSONResponse(
        {
            "total": len(tools),
            "tools": tools_info,
        }
    )
