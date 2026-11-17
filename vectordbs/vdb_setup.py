import os
import shutil
import sys
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "vectordbs" / "vdb_search.py"


def main() -> None:
    load_dotenv(find_dotenv(usecwd=True))                    # a WORK_REPO set in the shell wins over .env
    work = os.getenv("WORK_REPO", "").strip().strip('"')
    if not work:
        sys.exit("WORK_REPO is not set. Add this line to the .env in the course repo folder (your own path), then run again:\n"
                 "    WORK_REPO=D:\\genai-course-work")
    repo = Path(work).expanduser()
    if not repo.is_dir():
        sys.exit(f"WORK_REPO points to {repo}, but that folder doesn't exist. Fix the WORK_REPO line.")
    if repo.resolve() == ROOT:
        sys.exit("WORK_REPO points at the COURSE repo. It must be your own work repository.")

    dst = repo / "vectordbs" / "vdb_search.py"
    dst.parent.mkdir(exist_ok=True)
    if dst.exists() and "--fresh" not in sys.argv:
        print(f"Kept your existing {dst}  (add --fresh to start again from the original)")
    else:
        shutil.copy2(SRC, dst)
        print(f"Copied the homework file to {dst}")

    sep = "\\" if os.name == "nt" else "/"
    print("\nNext (stay in this course repo folder):")
    print(f"  Read first:      uv run jupyter lab module04{sep}s25_vector_db.ipynb")
    print(f"  Edit in VS Code: {dst}   (four TODOs)")
    print(f"  Run it:          uv run python \"{dst}\"")
    print("  Check it:        uv run pytest tests/test_vdb.py -rs")
    print(f"  Commit:          cd \"{repo}\"  then  git add vectordbs  ;  git commit -m \"S25: vector database\"  ;  git push")


if __name__ == "__main__":
    main()
