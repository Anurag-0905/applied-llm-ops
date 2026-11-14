"""
Environment initialization script.
Configures working directories and bootstraps the initial application structure.
"""
import os
import shutil
import sys
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "orchestration" / "app.py"


def main() -> None:
    load_dotenv(find_dotenv(usecwd=True), override=True)
    work = os.getenv("WORK_REPO", "").strip().strip('"')
    
    if not work:
        sys.exit("Configuration Error: WORK_REPO is not set in the environment.")
        
    repo = Path(work).expanduser()
    if not repo.is_dir():
        repo.mkdir(parents=True, exist_ok=True)
        
    if repo.resolve() == ROOT:
        sys.exit("Configuration Error: WORK_REPO cannot point to the core system repository.")

    dst = repo / "s23" / "app.py"
    dst.parent.mkdir(exist_ok=True)
    
    if dst.exists() and "--fresh" not in sys.argv:
        print(f"Target already exists at {dst} (run with --fresh to overwrite).")
    else:
        if SRC.exists():
            shutil.copy2(SRC, dst)
            print(f"Successfully deployed application entry point to {dst}")
        else:
            print(f"Source file {SRC} not found. Ensure repository integrity.")

    win = os.name == "nt"
    slash = "\\" if win else "/"
    
    print("\n=== Deployment Instructions ===")
    print(f"  [Server]    uv run python \"{dst}\"")
    print(f"  [API Docs]  http://127.0.0.1:8000/docs")
    print(f"  [Client]    uv run python module03{slash}s23_client.py")
    print(f"  [Tests]     uv run pytest tests/test_s23.py -rs")


if __name__ == "__main__":
    main()