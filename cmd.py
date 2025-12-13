import asyncio
from typing import Tuple, Optional

async def run_cmd(*args: str, check: bool = True, timeout: Optional[float] = 60.0) -> Tuple[int, str, str]:
    """
    Run a command asynchronously and return (rc, stdout, stderr).
    Enforces a timeout and avoids deadlocks by using communicate().
    """
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        stdout_b, stderr_b = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
        stdout_b, stderr_b = await proc.communicate()
        rc = proc.returncode if proc.returncode is not None else 124
        out = stdout_b.decode(errors="replace")
        err = (stderr_b.decode(errors="replace") + f"\n[run_cmd timeout after {timeout}s]").strip()
        if check:
            raise RuntimeError(f"Command timed out: {args}\n{err}")

        return rc, out, err

    rc = proc.returncode or 0
    out = stdout_b.decode(errors="replace")
    err = stderr_b.decode(errors="replace")

    if check and rc != 0:
        raise RuntimeError(f"Command failed rc={rc}: {args}\nstdout:\n{out}\nstderr:\n{err}")

    print("rc=", rc)
    print("out=", repr(out))
    print("err=", repr(err))

    return rc, out, err

