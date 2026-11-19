"""Session 26 homework - migrate the S25 collection to Qdrant, prove the results match, keep tenants apart, choose a store.

Setup copies this file to <your work repo>/s26/migrate.py. Run it FROM THE COURSE REPO FOLDER:

    docker compose -f module04/s26_docker-compose.yml up -d     # optional: Qdrant server (else it runs in-process)
    uv run python "<your work repo>\\s26\\migrate.py"
    uv run pytest tests/test_s26.py -rs                          # the checker

Four TODOs. Read module04/s26_vector_stores.ipynb first (its Part B also has the pgvector steps).
PART 1 is given. PART 2 is yours. Using ChatGPT is allowed - never paste your .env or any key.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "module04"))        # run from the course repo folder, so these imports work
from dotenv import find_dotenv, load_dotenv  # noqa: E402
from qdrant_client import models  # noqa: E402

load_dotenv(find_dotenv(usecwd=True))
import embedding_utils as EMBEDDING # noqa: E402
import vs_utils as VS  # noqa: E402

STORES = ["chroma", "qdrant", "pgvector", "pinecone", "weaviate"]


def to_points(rows: dict) -> list[models.PointStruct]:
    ids = rows.get("ids") or []
    embeddings = rows.get("embeddings") or []
    metadatas = rows.get("metadatas") or [{} for _ in ids]
    documents = rows.get("documents") or ["" for _ in ids]

    points: list[models.PointStruct] = []
    for cid, emb, meta, doc in zip(ids, embeddings, metadatas, documents):
        # Unpack meta into a fresh dict to prevent mutating the upstream ChromaDB dictionary
        payload = {
            **(meta or {}),
            "text": doc,
            "chroma_id": cid,
        }
        # Ensure vector is a native Python list of floats (Qdrant rejects raw NumPy arrays)
        vector = emb.tolist() if hasattr(emb, "tolist") else [float(x) for x in emb]
        
        points.append(
            models.PointStruct(
                id=VS.point_id(cid),
                vector=vector,
                payload=payload,
            )
        )
    return points


def overlap_at_k(a: list, b: list, k: int = 3) -> float:
    if k <= 0 or not a or not b:
        return 0.0
    
    return float(len(set(a[:k]) & set(b[:k])) / k)


def tenant_filter(customer_id: str) -> models.Filter:
    """TODO 3 - the filter that keeps one customer's notes private."""
    return models.Filter(
        must=[
            models.FieldCondition(
                key="customer_id",
                match=models.MatchValue(value=customer_id),
            )
        ]
    )


STORE_CHOICES: dict[str, tuple[str, str]] = {
    "hospital_onprem": (
        "pgvector",
        "Strict HIPAA data residency requires on-premise hosting, and leveraging the IT team's existing PostgreSQL infrastructure eliminates introducing a separate database engine.",
    ),
    "startup_no_ops": (
        "pinecone",
        "A fully managed serverless architecture eliminates infrastructure maintenance for a two-person team while providing usage-based scaling for US traffic.",
    ),
    "ecommerce_scale": (
        "qdrant",
        "Self-hosted Qdrant handles tens of millions of vectors with high-performance payload indexing designed specifically for complex multi-attribute metadata filtering.",
    ),
}

# ========================================================================================= PART 1 - GIVEN
QUESTIONS = ["how long do refunds take", "my parcel arrived broken", "can I pay cash on delivery",
             "change my delivery address", "is there a warranty on headphones"]


def main() -> None:
    emb = EMBEDDING.Embedder("bge-small")
    rows = VS.chroma_rows(emb)
    client, where = VS.connect_qdrant("auto")
    n = VS.migrate_to_qdrant(client, rows, to_points=to_points)
    print(f"migrated {n} points with YOUR to_points() -> {where}\n")
    report = ["# Session 26 - my migration results", "", f"Target: {where}", "",
              "## Same results? (YOUR overlap_at_k, top 3)", "", "| question | overlap |", "|---|---|"]

    from vectordbs.vdb_utils import get_collection, open_db, search
    chroma = get_collection(open_db())
    for q in QUESTIONS:
        before = [h["id"] for h in search(chroma, emb, q, 3)]
        qv = emb.embed([q], kind="query")[0]
        after = [p["chroma_id"] for _, p in VS.search_qdrant(client, qv, 3)]
        ov = overlap_at_k(before, after, 3)
        print(f"  {ov:.2f}  {q}")
        report.append(f"| {q} | {ov:.2f} |")

    VS.migrate_notes(client, emb)
    qv = emb.embed(["what did the customer ask about their refund"], kind="query")[0]
    leaked = [p["customer_id"] for _, p in VS.search_qdrant(client, qv, 3, "customer_notes", VS.tenant_filter("CUST-1001"))]
    safe = all(c == "CUST-1001" for c in leaked)
    print(f"\ntenant filter for Asha returned customers {leaked} -> {'SAFE' if safe else 'LEAK'}")
    report += ["", "## Multi-tenancy (YOUR tenant_filter)", "", f"Asha's search returned: {leaked} -> {'SAFE' if safe else 'LEAK'}",
               "", "## My store choices", ""]
    report += [f"- **{k}**: {v[0]} - {v[1]}" for k, v in STORE_CHOICES.items()]

    out = Path(__file__).with_name("results.md")
    out.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"\nwrote {out}  - commit it with this file")


if __name__ == "__main__":
    main()
