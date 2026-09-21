"""MCP server for R code formatting tools."""

import asyncio
import os
from typing import Optional

from mcp.server import MCPServer

AIR_PATH = r"C:\Users\pbulsink\.local\bin\air.exe"
RY_PATH = r"C:\Users\pbulsink\.local\bin\ry.exe"

server = MCPServer(
    "r-format-mcp",
    version="0.1.0",
    description="MCP server for R code formatting (air) and type checking (ry)",
)


async def _run_command(cmd: list[str], working_dir: Optional[str] = None, timeout: int = 300):
    """Execute command and return stdout/stderr."""
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=working_dir or os.getcwd(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return {
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "return_code": 124,
            }
        return {
            "stdout": stdout.decode("utf-8", errors="replace"),
            "stderr": stderr.decode("utf-8", errors="replace"),
            "return_code": proc.returncode,
        }
    except FileNotFoundError:
        return {
            "stdout": "",
            "stderr": f"Command not found: {cmd[0]}",
            "return_code": 127,
        }
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "return_code": 1}


def _format_output(result):
    """Format command output for the LLM client."""
    lines = []
    if result["return_code"] != 0:
        lines.append(f"[Command exited with code {result['return_code']}]")
    lines.append(result["stdout"])
    if result["stderr"]:
        lines.append("--- stderr ---\n" + result["stderr"])
    return "\n".join(lines)


# ── air format ─────────────────────────────────────────────────────────

@server.tool(description="Format R code files using air format")
async def air_format(
    path: Optional[str] = None,
    working_dir: Optional[str] = None,
    check: bool = False,
) -> str:
    """Format R code with air.

    Args:
        path: Specific file or directory to format (default: current directory).
        working_dir: Working directory for the command.
        check: If True, check formatting without writing changes.
    """
    cmd = [AIR_PATH, "format"]
    if check:
        cmd.append("--check")
    if path:
        cmd.append(path)
    
    result = await _run_command(cmd, working_dir)
    return _format_output(result)


# ── air format check ───────────────────────────────────────────────────

@server.tool(description="Check R code formatting with air without modifying files")
async def air_format_check(
    path: Optional[str] = None,
    working_dir: Optional[str] = None,
) -> str:
    """Check if R code is formatted correctly with air.

    Args:
        path: Specific file or directory to check (default: current directory).
        working_dir: Working directory for the command.
    """
    cmd = [AIR_PATH, "format", "--check"]
    if path:
        cmd.append(path)
    
    result = await _run_command(cmd, working_dir)
    return _format_output(result)


# ── ry check ───────────────────────────────────────────────────────────

@server.tool(description="Run ry type checker on R code")
async def ry_check(
    path: Optional[str] = None,
    working_dir: Optional[str] = None,
    output_format: str = "full",
) -> str:
    """Run ry type checker on R code.

    Args:
        path: Specific file or directory to check (default: current directory).
        working_dir: Working directory for the command.
        output_format: Output format (full, concise, json, github, gitlab, junit).
    """
    cmd = [RY_PATH, "check", "--output-format", output_format]
    if path:
        cmd.append(path)
    
    result = await _run_command(cmd, working_dir)
    return _format_output(result)


def main():
    asyncio.run(server.run_stdio_async())


if __name__ == "__main__":
    main()
