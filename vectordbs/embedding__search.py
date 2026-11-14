import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path.cwd() / "module04"))        # run from the course repo folder, so these imports work
from embedding_queries import CASES, PASS_MARK  # noqa: E402
from embedding_utils import KB_DIR, Embedder  # noqa: E402


# ======================================================================================= PART 2 - YOUR CODE
def cosine(a: np.ndarray, b: np.ndarray) -> float:
    """
    Computes the cosine similarity between two vectors.
    Handles zero-vectors explicitly to prevent NaN propagation.
    """
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    return float(np.dot(a, b) / (norm_a * norm_b))


def top_k(query: np.ndarray, matrix: np.ndarray, k: int = 3) -> list[int]:
    """
    Returns the indices of the top k most similar vectors in the matrix to the query.
    Uses vectorized operations instead of slow Python loops.
    """
    if k <= 0 or matrix.size == 0:
        return np.array([], dtype=int)

    norm_q = np.linalg.norm(query)
    if norm_q == 0:
        return np.arange(min(k, len(matrix)))

    # Vectorized cosine similarity calculation across the entire matrix
    norms_m = np.linalg.norm(matrix, axis=1)
    
    # Suppress division-by-zero warnings for zero-vectors in the matrix, converting NaNs to 0
    with np.errstate(divide='ignore', invalid='ignore'):
        similarities = np.dot(matrix, query) / (norms_m * norm_q)
        similarities[np.isnan(similarities)] = 0.0

    k = min(k, len(matrix))
    
    # argsort returns ascending order, so we reverse it with [::-1] and slice top k
    top_indices = np.argsort(similarities)[::-1][:k]
    return top_indices.tolist()


def split_sections(markdown: str) -> list[tuple[str, str]]:
    """
    Parses a markdown string and extracts sections starting with '## '.
    Ignores frontmatter, title, and empty sections.
    """
    sections = []
    current_heading = None
    current_content = []

    for line in markdown.splitlines():
        if line.startswith("## "):
            # Save the previous section if it has actual content
            if current_heading is not None:
                content_str = " ".join(current_content).strip()
                if content_str:
                    sections.append((current_heading, content_str))
            
            # Start tracking the new heading
            current_heading = line[3:].strip()
            current_content = []
        elif current_heading is not None:
            # We are inside a '## ' section; accumulate text
            stripped_line = line.strip()
            if stripped_line:
                current_content.append(stripped_line)

    # Catch the final section after the loop ends
    if current_heading is not None:
        content_str = " ".join(current_content).strip()
        if content_str:
            sections.append((current_heading, content_str))

    return sections


MY_CASES: list[tuple[str, str]] = [
    ("The jacket I received has a huge tear in the sleeve, what do I do?", "damaged-items"),
    ("How do I know if a medium shirt will actually fit me before ordering?", "size-guide"),
    ("Can I apply a promo code I found online to my checkout cart?", "coupons"),
]

# ========================================================================================= PART 1 - GIVEN
def load_sections() -> tuple[list[str], list[str], list[str]]:
    """All articles -> (texts to embed, article names, 'Article > Section' labels), using YOUR split_sections."""
    texts, docs, labels = [], [], []
    for path in sorted(KB_DIR.glob("*.md")):
        for heading, text in split_sections(path.read_text(encoding="utf-8")):
            texts.append(f"{heading}. {text}")
            docs.append(path.stem)
            labels.append(f"{path.stem} > {heading}")
    return texts, docs, labels


def main() -> None:
    texts, docs, labels = load_sections()
    print(f"{len(texts)} sections loaded with YOUR split_sections()")
    emb = Embedder("bge-small")
    matrix = emb.embed(texts)                                     # offline half: every section, once
    print(f"embedded them with {emb.model_id}: {matrix.shape[0]} rows x {matrix.shape[1]} numbers\n")

    report = ["# Session 24 - my semantic search results", "", f"Model: {emb.model_id}", "",
              "| # | question | expected | top 3 (YOUR top_k) | hit |", "|---|---|---|---|---|"]
    hits = mine = 0
    for i, (question, expected) in enumerate(CASES + MY_CASES, 1):
        q = emb.embed([question], kind="query")[0]                 # online half: the question
        found = [docs[j] for j in top_k(q, matrix, 3)]
        ok = expected in found
        if i <= len(CASES):
            hits += ok
        else:
            mine += ok
        print(f"  {'ok  ' if ok else 'MISS'} {question[:50]:50} -> {found}")
        report.append(f"| {i} | {question} | {expected} | {', '.join(found)} | {'yes' if ok else 'no'} |")

    summary = f"Course questions: hit@3 {hits}/{len(CASES)} (pass mark {PASS_MARK}).  My questions: {mine}/{len(MY_CASES)}."
    print("\n" + summary)
    report += ["", summary, ""]
    out = Path(__file__).with_name("results.md")
    out.write_text("\n".join(report), encoding="utf-8")
    print(f"wrote {out}  - commit it with this file")


if __name__ == "__main__":
    main()
