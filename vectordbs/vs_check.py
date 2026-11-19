from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDENT_PATH = Path("vectordbs") / "migrate.py"
STORES = {"chroma", "qdrant", "pgvector", "pinecone", "weaviate"}
SELF_HOSTABLE = {"chroma", "qdrant", "pgvector", "weaviate"}


def load_module(path: Path):
    sys.path.insert(0, str(HERE))
    spec = importlib.util.spec_from_file_location(f"vs_repo{abs(hash(path))}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_vs_work(path: Path) -> list[str]:
    """Returns a list of problems. Empty list = everything passes."""
    if not path.exists():
        return [f"{path} not found - run:  uv run python vectordbs/vs_setup.py"]
    import vs_utils as VS
    from qdrant_client import QdrantClient, models
    mod = load_module(path)
    problems: list[str] = []

    rows = {"ids": ["refunds#1", "warranty#2", "payments#3"],
            "embeddings": [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.7, 0.7, 0.0, 0.0]],
            "metadatas": [{"doc_id": "refunds", "category": "payments"}, {"doc_id": "warranty", "category": "returns"},
                          {"doc_id": "payments", "category": "payments"}],
            "documents": ["refund text", "warranty text", "payment text"]}
    
    try:
        pts = mod.to_points(rows)
        if len(pts) != 3:
            problems.append(f"TODO 1 to_points returned {len(pts)} points for 3 rows")
        else:
            p = pts[0]
            if str(p.id) != VS.point_id("refunds#1"):
                problems.append("TODO 1 point id must be VS.point_id(<chroma id>)")
            if list(p.vector) != [1.0, 0.0, 0.0, 0.0]:
                problems.append("TODO 1 point vector must be the row's embedding")
            want = {"doc_id": "refunds", "category": "payments", "text": "refund text", "chroma_id": "refunds#1"}
            if p.payload != want:
                problems.append(f"TODO 1 payload is {p.payload!r}, expected {want!r}")
            if not problems:
                c = QdrantClient(":memory:")
                c.create_collection("t", vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE))
                c.upsert("t", points=pts, wait=True)
                if c.count("t").count != 3:
                    problems.append("TODO 1 Qdrant didn't accept all three points")
    except NotImplementedError:
        problems.append("TODO 1 to_points() is not written yet")
    except Exception as e:
        problems.append(f"TODO 1 to_points() crashed: {type(e).__name__}: {e}")

    
    try:
        for args, want in [((["x", "y", "z"], ["z", "x", "q"], 3), 2 / 3), ((["a", "b"], ["b", "a"], 2), 1.0),
                           ((["a", "b", "c"], ["d", "e", "f"], 3), 0.0), (([], [], 0), 0.0)]:
            got = mod.overlap_at_k(*args)
            if not isinstance(got, float) or abs(got - want) > 1e-9:
                problems.append(f"TODO 2 overlap_at_k{args} returned {got!r}, expected {want:.4f}")
                break
    except NotImplementedError:
        problems.append("TODO 2 overlap_at_k() is not written yet")
    except Exception as e:
        problems.append(f"TODO 2 overlap_at_k() crashed: {type(e).__name__}: {e}")

    
    try:
        f = mod.tenant_filter("CUST-1001")
        if not isinstance(f, models.Filter):
            problems.append(f"TODO 3 tenant_filter must return a models.Filter, got {type(f).__name__}")
        else:
            c = QdrantClient(":memory:")
            c.create_collection("n", vectors_config=models.VectorParams(size=2, distance=models.Distance.COSINE))
            c.upsert("n", wait=True, points=[models.PointStruct(id=i, vector=[1.0, i / 10], payload={"customer_id": cid})
                                              for i, cid in enumerate(["CUST-1001", "CUST-1002", "CUST-1002", "CUST-1001"])])
            got = {p.payload["customer_id"] for p in c.query_points("n", query=[1.0, 0.1], limit=4, query_filter=f).points}
            if got != {"CUST-1001"}:
                problems.append(f"TODO 3 tenant_filter('CUST-1001') let these customers through: {sorted(got)}")
    except NotImplementedError:
        problems.append("TODO 3 tenant_filter() is not written yet")
    except Exception as e:
        problems.append(f"TODO 3 tenant_filter() crashed: {type(e).__name__}: {e}")

    choices = getattr(mod, "STORE_CHOICES", {})
    for key in ("hospital_onprem", "startup_no_ops", "ecommerce_scale"):
        store, reason = choices.get(key, ("", ""))
        if store not in STORES:
            problems.append(f"TODO 4 {key}: pick one of {sorted(STORES)} (got {store!r})")
        elif len(reason.split()) < 8:
            problems.append(f"TODO 4 {key}: give a reason of at least 8 words")
    if choices.get("hospital_onprem", ("",))[0] == "pinecone":
        problems.append("TODO 4 hospital_onprem: Pinecone is a managed cloud service - the data can't stay in the hospital")

    results = path.with_name("results.md")
    if not results.exists():
        problems.append("results.md not found next to migrate.py - run your file once (it writes results.md)")
    elif "SAFE" not in results.read_text(encoding="utf-8"):
        problems.append("results.md doesn't show a SAFE tenant search - check TODO 3 and run again")
    return problems
