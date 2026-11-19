import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "vectordbs"))      
from dotenv import find_dotenv, load_dotenv  # noqa: E402

load_dotenv(find_dotenv(usecwd=True))
import hb_queries as Q  # noqa: E402
import hb_utils as HB  # noqa: E402


# ======================================================================================= PART 2 - YOUR CODE
def rrf_fuse(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)


def weighted_fuse(keyword: dict[str, float], dense: dict[str, float], alpha: float = 0.5) -> list[tuple[str, float]]:
    def _minmax(d: dict[str, float]) -> dict[str, float]:
        if not d:
            return {}
        lo, hi = min(d.values()), max(d.values())
        if hi == lo:
            return {doc_id: 1.0 for doc_id in d}
        span = hi - lo
        return {doc_id: (score - lo) / span for doc_id, score in d.items()}

    kw_norm = _minmax(keyword)
    dn_norm = _minmax(dense)

    fused = {
        doc_id: alpha * dn_norm.get(doc_id, 0.0) + (1.0 - alpha) * kw_norm.get(doc_id, 0.0)
        for doc_id in kw_norm.keys() | dn_norm.keys()
    }
    return sorted(fused.items(), key=lambda item: item[1], reverse=True)


def rerank_top(question: str, candidates: list, score_fn, k: int = 3) -> list[tuple[float, object]]:
    if not candidates:
        return []
    texts = [c.chunk.search_text for c in candidates]
    scores = score_fn(question, texts)
    ranked = sorted(
        ((float(score), cand) for score, cand in zip(scores, candidates)),
        key=lambda item: item[0],
        reverse=True,
    )
    return ranked[:k]


MY_EXACT_CASES: list[tuple[str, str, str]] = [
    ("Is SKU-EL-006 in stock right now?", "products", "SKU-EL-006"),
    ("What sizes are available for Sprint Lite?", "products", "SKU-FW-004"),
    ("Which backpack fits a 15.6 inch laptop?", "products", "SKU-BG-002"),
]

GATE: tuple[float, str] = (
    -7.5,
    "Sits midway between the highest out-of-scope score (-10.20) and lowest in-scope score (-4.99), leaving ~2.5 logit points of margin to keep paraphrased help queries while still rejecting off-topic questions.",
)

# ========================================================================================= PART 1 - GIVEN
class YourRetriever:
    """The course Retriever, with YOUR fusion and YOUR reranking step plugged in."""

    def __init__(self, r: HB.Retriever):
        self.r = r

    def search(self, method: str, question: str, k: int = 3):
        r = self.r
        if method == "hybrid":
            return r.hybrid(question, k, fuse=rrf_fuse)
        if method == "weighted":
            return r.weighted(question, k, alpha=0.5, fuse=weighted_fuse)
        if method == "rerank":
            if r.reranker is None:
                r.reranker = HB.Reranker()
            cands = r.hybrid(question, k=20, fuse=rrf_fuse)
            return [HB.Hit(s, c.chunk, c.key) for s, c in rerank_top(question, cands, r.reranker.score, k)]
        return r.search(method, question, k)


def main() -> None:
    rs = {c: YourRetriever(HB.Retriever(c)) for c in HB.CORPORA}
    cases = Q.CASES + [(q, c, e, "exact") for q, c, e in MY_EXACT_CASES]
    report = ["# Session 27 - my hybrid search results", "",
              (f"{len(cases)} questions ({sum(c[3] == 'exact' for c in cases)} exact incl. my {len(MY_EXACT_CASES)}, "
               f"{sum(c[3] == 'meaning' for c in cases)} meaning), top 3"), "",
              "| method | hit@3 | MRR | exact | meaning |", "|---|---|---|---|---|"]
    print(report[2] + "\n")
    for m in ("keyword", "dense", "hybrid", "weighted", "rerank"):
        res = HB.evaluate(rs, cases, m)
        a, e, n = res["all"], res["exact"], res["meaning"]
        line = f"| {m} | {a['hits']}/{a['n']} | {a['mrr']:.2f} | {e['hits']}/{e['n']} | {n['hits']}/{n['n']} |"
        print(line)
        report.append(line)

    threshold, reason = GATE
    r = rs["help"]
    inside = [q for q, c, *_ in Q.CASES if c == "help"]
    kept = sum(r.search("rerank", q, 1)[0].score >= threshold for q in inside)
    blocked = sum(r.search("rerank", q, 1)[0].score < threshold for q, _ in Q.OUT_OF_SCOPE)
    gate = (f"Gate {threshold}: kept {kept}/{len(inside)} in-scope questions, said 'I don't know' to "
            f"{blocked}/{len(Q.OUT_OF_SCOPE)} out-of-scope ones. Why this number: {reason}")
    print("\n" + gate)
    report += ["", "## My relevance gate", "", gate, "", "## My exact-term questions", ""]
    report += [f"- `{q}` ({c}) -> {e}" for q, c, e in MY_EXACT_CASES]

    out = Path(__file__).with_name("results.md")
    out.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"\nwrote {out}  - commit it with this file")


if __name__ == "__main__":
    main()
