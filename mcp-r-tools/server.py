"""MCP server for R package development tools."""

import asyncio
import os
from typing import List, Optional

from typing import Annotated
from pydantic import Field

from dotenv import load_dotenv
from mcp.server import MCPServer

load_dotenv()

RSCRIPT = os.getenv("RSCRIPT_PATH", r"C:\Program Files\R\R-4.5.2\bin\x64\Rscript.exe")

server = MCPServer(
    "r-tools-mcp",
    version="0.2.0",
    description="MCP server for R package development tools (devtools, lintr)",
)


async def _run_r_script(code: str, working_dir: Optional[str] = None, timeout: int = 900):
    """Execute R code via RScript.exe and return stdout/stderr."""
    wrapped_code = f"""tryCatch(
{{
    {code}
}}, error = function(e) {{
    message(paste("ERROR:", e$message))
    quit(status = 1)
}})
"""

    try:
        proc = await asyncio.create_subprocess_exec(
            RSCRIPT, "-e", wrapped_code,
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
                "stderr": f"RScript timed out after {timeout} seconds",
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
            "stderr": f"RScript not found at: {RSCRIPT}",
            "return_code": 127,
        }
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "return_code": 1}


def _format_output(result):
    """Format R script output for the LLM client."""
    lines = []
    if result["return_code"] != 0:
        lines.append(f"[R exited with code {result['return_code']}]")
    lines.append(result["stdout"])
    if result["stderr"]:
        lines.append("--- stderr ---\n" + result["stderr"])
    return "\n".join(lines)


# ── devtools::document ─────────────────────────────────────────────

@server.tool(description="Run devtools::document() to update package documentation (NAMESPACE and man/)")
async def devtools_document(working_dir: Optional[str] = None) -> str:
    """Run devtools::document() to update package documentation."""
    result = await _run_r_script("devtools::document()", working_dir)
    return _format_output(result)


# ── devtools::check ────────────────────────────────────────────────

@server.tool(description="Build and check an R package with devtools::check().")
async def devtools_check(
    working_dir: Optional[str] = None,
    document: Optional[bool] = None,
    cran: bool = True,
    manual: bool = False,
    vignettes: bool = True,
    error_on: Annotated[str, Field(pattern="^(never|error|warning|note)$", description="Stop on 'never', 'error', 'warning', or 'note'.")] = "never",
    args: Optional[List[str]] = None,
    build_args: Optional[List[str]] = None,
) -> str:
    """Run devtools::check() to build and check an R package.

    Args:
        working_dir: Path to the package root (default: current directory).
        document: Override documentation behaviour (True/False/null=default).
        cran: Use CRAN-like settings (default True).
        manual: Build and check manual (default False = --no-manual).
        vignettes: Build and check vignettes (default True).
        error_on: Stop on "never", "error", "warning", or "note".
        args: Extra arguments passed to R CMD check.
        build_args: Extra arguments passed to R CMD build.
    """
    import json
    parts = ["pkg = '.'"]
    parts.append(f"cran = {str(cran).lower()}")
    parts.append(f"manual = {str(manual).lower()}")
    parts.append(f"vignettes = {str(vignettes).lower()}")
    parts.append(f'error_on = "{error_on}"')
    if document is not None:
        parts.append(f"document = {str(document).lower()}")
    if args:
        parts.append(f"args = {json.dumps(args)}")
    if build_args:
        parts.append(f"build_args = {json.dumps(build_args)}")

    r_code = f"devtools::check({', '.join(parts)})"

    result = await _run_r_script(r_code, working_dir)
    return _format_output(result)


# ── lintr::lint ────────────────────────────────────────────────────

@server.tool(description="Run lintr::lint() to check R code style and best practices.")
async def lintr_lint(
    path: Optional[str] = None,
    working_dir: Optional[str] = None,
) -> str:
    """Run lintr::lint() to check R code style.

    Args:
        path: Specific file or directory to lint (default: entire package root).
        working_dir: Package root if path is a relative reference.
    """
    import json
    if path:
        # Use repr for safe R string literal
        r_path = repr(path)
        r_code = f"lintr::lint({r_path})"
    else:
        r_code = "lintr::lint()"
    result = await _run_r_script(r_code, working_dir)
    return _format_output(result)


# ── devtools::test ─────────────────────────────────────────────────

@server.tool(description="Run devtools::test() to execute testthat tests for an R package.")
async def devtools_test(
    working_dir: Optional[str] = None,
    filter: Optional[str] = None,
    reporter: Optional[str] = None,
) -> str:
    """Run devtools::test() to execute package tests.

    Args:
        working_dir: Path to the package root (default: current directory).
        filter: Pattern to match test file names.
        reporter: Which test reporter to use (e.g., 'summary', 'minimal').
    """
    import json
    parts = ["pkg = '.'"]
    if filter:
        parts.append(f"filter = {json.dumps(filter)}")
    if reporter:
        parts.append(f"reporter = {json.dumps(reporter)}")
    r_code = f"devtools::test({', '.join(parts)})"

    result = await _run_r_script(r_code, working_dir)
    return _format_output(result)


def main():
    asyncio.run(server.run_stdio_async())


if __name__ == "__main__":
    main()
