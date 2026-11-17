import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "vectordbs"))        # run from the course repo folder, so these imports work
import embedding_utils as EMBEDDING  # noqa: E402
import vdb_utils as VDB  # noqa: E402

CATEGORIES = ["orders", "payments", "returns", "account", "products"]


# ======================================================================================= PART 2 - YOUR CODE
def make_metadata(chunk: EMBEDDING.Chunk, info: dict) -> dict:
    return {
        "doc_id": chunk.doc_id,
        "category": info["category"],
        "updated": int(info["updated"].replace("-", ""))
    }


def build_where(category: str | None = None, since: str | None = None) -> dict | None:
    category_filter = {"category": category} if category else None
    
    since_int = int(since.replace("-", "")) if since else None
    since_filter = {"updated": {"$gte": since_int}} if since else None

    if category_filter and since_filter:
        return {"$and": [category_filter, since_filter]}
    
    return category_filter or since_filter or None


def recall_at_k(exact: list[list[int]], approx: list[list[int]], k: int = 10) -> float:
    if not exact or not approx or k <= 0:
        return 0.0
        
    recalls = [len(set(e[:k]) & set(a[:k])) / k for e, a in zip(exact, approx)]
    return float(sum(recalls) / len(exact))

MY_FILTERED: list[tuple[str, str | None, str | None]] = [
    ("What is the process for sending back a broken item I just received?", "returns", "2026-07-01"),
    ("How do I permanently delete my profile and personal data?", "account", None),
]


# ========================================================================================= PART 1 - GIVEN
def main() -> None:
    client = VDB.open_db(None)                                   # in memory - nothing written to your disk
    emb = EMBEDDING.Embedder("bge-small")
    col = VDB.build_collection(client, emb, make_metadata=lambda c: make_metadata(c, VDB.META[c.doc_id]))
    print(f"collection built with YOUR make_metadata(): {col.count()} rows\n")
    report = ["# Session 25 - my vector database results", "", "## Filtered search (YOUR build_where)", "",
              "| question | filter | top results | all match the filter? |", "|---|---|---|---|"]

    course = [("how long do refunds take", "payments", None), ("change my delivery address", None, "2026-01-01"),
              ("my parcel arrived broken", "returns", "2026-06-01")]
    for question, category, since in course + MY_FILTERED:
        where = build_where(category, since)
        hits = VDB.search(col, emb, question, 3, where)
        ok = all((not category or h["meta"]["category"] == category) and
                 (not since or h["meta"]["updated"] >= VDB.date_int(since)) for h in hits)
        names = ", ".join(f"{h['meta']['doc_id']} ({h['meta']['updated']})" for h in hits) or "no rows match"
        print(f"  {'ok  ' if ok else 'FAIL'} {question[:40]:40} {where}\n        -> {names}")
        report.append(f"| {question} | `{where}` | {names} | {'yes' if ok else 'NO'} |")

    print("\nANN experiment: 20,000 vectors (about 20 seconds), exact top-10 vs three HNSW settings (YOUR recall_at_k)")
    x, q = VDB.clustered_vectors(20_000)
    exact = VDB.exact_top_k(x, q, 10)
    report += ["", "## Speed vs accuracy (YOUR recall_at_k)", "", "| setting | recall@10 | ms/query |", "|---|---|---|"]
    ann = VDB.open_db(None)
    for preset in VDB.HNSW_PRESETS:
        r = VDB.hnsw_run(ann, x, q, preset)
        rec = recall_at_k(exact, r["ids"], 10)
        print(f"  {preset:9} recall@10 {rec:.2f}   {r['ms_per_query']:.2f} ms/query")
        report.append(f"| {preset} | {rec:.2f} | {r['ms_per_query']:.2f} |")

    out = Path(__file__).with_name("results.md")
    out.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"\nwrote {out}  - commit it with this file")


if __name__ == "__main__":
    main()
