"""MCP server for lossless in-place PNG compression via ImageMagick."""

import asyncio
import glob
import os
import shutil
import tempfile
from typing import Annotated, Optional

from dotenv import load_dotenv
from mcp.server import MCPServer
from pydantic import Field

load_dotenv()

MAGICK = (
    os.getenv("MAGICK_PATH")
    or shutil.which("magick")
    or r"C:\Users\pbulsink\AppData\Local\Microsoft\WindowsApps\magick.exe"
)

TEMP_PREFIX = ".mcp-png-compress-"

server = MCPServer(
    "png-compress-mcp",
    version="0.1.0",
    description="MCP server for lossless in-place PNG compression via ImageMagick (magick.exe)",
)


async def _run_command(cmd: list[str], timeout: int) -> dict:
    """Execute command and return stdout/stderr/return_code."""
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
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
        return {"stdout": "", "stderr": f"Command not found: {cmd[0]}", "return_code": 127}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "return_code": 1}


async def _compress_one(path: str, compression_level: int, filter_type: str, strip: bool, timeout: int) -> dict:
    """Compress a single PNG file in place. Returns a result record."""
    before = os.path.getsize(path)

    fd, tmp = tempfile.mkstemp(prefix=TEMP_PREFIX, suffix=".png", dir=os.path.dirname(os.path.abspath(path)))
    os.close(fd)

    try:
        cmd = [MAGICK, path]
        if strip:
            cmd.append("-strip")
        cmd += [
            "-define", f"png:compression-level={compression_level}",
            "-define", f"png:filter-type={filter_type}",
            tmp,
        ]
        result = await _run_command(cmd, timeout)
        if result["return_code"] != 0:
            return {"file": path, "status": "error", "detail": (result["stderr"] or result["stdout"]).strip()}

        # Verify the re-encoded file is pixel-identical before overwriting.
        check = await _run_command([MAGICK, "compare", "-metric", "AE", path, tmp, "null:"], timeout)
        if check["return_code"] != 0:
            return {
                "file": path,
                "status": "error",
                "detail": f"losslessness check failed (magick compare exit {check['return_code']}); original left untouched",
            }

        after = os.path.getsize(tmp)
        if after >= before:
            return {"file": path, "status": "skipped", "before": before, "after": after}

        os.replace(tmp, path)
        return {"file": path, "status": "compressed", "before": before, "after": after}
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def _collect_png_files(path: str) -> list[str]:
    """Expand a file or directory argument into a list of PNG files."""
    p = os.path.abspath(path)
    if os.path.isfile(p):
        return [p]
    matches = sorted(glob.glob(os.path.join(p, "**", "*.png"), recursive=True))
    return [m for m in matches if not os.path.basename(m).startswith(TEMP_PREFIX)]


def _format_report(results: list[dict]) -> str:
    lines = []
    total_before = 0
    total_after = 0
    counts = {"compressed": 0, "skipped": 0, "error": 0}
    for r in results:
        counts[r["status"]] += 1
        if r["status"] == "compressed":
            saved = r["before"] - r["after"]
            pct = 100.0 * saved / r["before"]
            lines.append(f"OK      {r['file']}: {r['before']} -> {r['after']} bytes (-{pct:.1f}%)")
            total_before += r["before"]
            total_after += r["after"]
        elif r["status"] == "skipped":
            lines.append(f"SKIPPED {r['file']}: no improvement ({r['before']} -> {r['after']} bytes), left unchanged")
        else:
            lines.append(f"ERROR   {r['file']}: {r['detail']}")

    saved_total = total_before - total_after
    summary = (
        f"Summary: {counts['compressed']} compressed, {counts['skipped']} skipped, "
        f"{counts['error']} error(s) out of {len(results)} file(s); "
        f"total saved {saved_total} bytes."
    )
    return "\n".join(lines + ["", summary])


@server.tool(description="Losslessly compress PNG image files in place using ImageMagick. Overwrites each file only if the re-encoded result is verified pixel-identical and strictly smaller.")
async def compress_png(
    path: Annotated[str, Field(description="Absolute path to a .png file or a directory containing .png files (searched recursively).")],
    compression_level: Annotated[int, Field(ge=0, le=9)] = 9,
    filter_type: Annotated[
        str,
        Field(description="PNG filter strategy. One of FilterTypeNone/Horizontal/Vertical/Up/Left/Paeth/Sub/All (default: FilterTypeAll tries all filters for best compression)."),
    ] = "FilterTypeAll",
    strip: bool = True,
    timeout: Annotated[int, Field(ge=10)] = 600,
) -> str:
    """Losslessly compress PNG files in place (overwrites existing files).

    Args:
        path: Absolute path to a .png file or a directory of .png files (recursed).
        compression_level: zlib level 0-9, default 9 (maximum).
        filter_type: PNG filter strategy; FilterTypeAll (default) is slowest but best.
        strip: Remove metadata chunks such as EXIF/profiles/comments (default True).
        timeout: Per-file timeout in seconds for ImageMagick operations.
    """
    p = os.path.abspath(path)
    if not os.path.exists(p):
        return f"ERROR path does not exist: {p}"
    if os.path.isfile(p) and not p.lower().endswith(".png"):
        return f"ERROR not a PNG file: {p}"

    files = _collect_png_files(p)
    if not files:
        return f"No .png files found under: {p}"

    results = [await _compress_one(f, compression_level, filter_type, strip, timeout) for f in files]
    return _format_report(results)


def main():
    asyncio.run(server.run_stdio_async())


if __name__ == "__main__":
    main()
