"""Twin 1 scope definition (from project-admin/Master_OCR_Allocation_Plan.md).
Single source of truth for which PDFs this worker owns."""
REPO_ROOT = "/home/user/ocr"

# (chapter, lecture, filename, expected_pages) -- expected_pages from the master inventory (508 total)
TWIN1_SCOPE = [
    ("Binomial Theorem", "01", "Binomial Theorem 01 Class Notes.pdf", 33),
    ("Binomial Theorem", "02", "Binomial Theorem 02 Class Notes.pdf", 40),
    ("Binomial Theorem", "03", "Binomial Theorem 03 Class Notes.pdf", 35),
    ("Binomial Theorem", "04", "Binomial Theorem 04 Class Notes.pdf", 46),
    ("Binomial Theorem", "05", "Binomial Theorem 05 Class Notes.pdf", 38),
    ("Binomial Theorem", "06", "Binomial Theorem 06 Class Notes.pdf", 43),
    ("Binomial Theorem", "07", "Binomial Theorem 07 Class Notes.pdf", 34),
    ("Binomial Theorem", "08", "Binomial Theorem 08 Class Notes.pdf", 46),
    ("Binomial Theorem", "09", "Binomial Theorem 09 Class Notes.pdf", 29),
    ("Permutations & Combinations", "01", "Permutations and Combinations 01 Class Notes.pdf", 46),
    ("Permutations & Combinations", "02", "Permutations and Combinations 02 Class Notes.pdf", 33),
    ("Permutations & Combinations", "03", "Permutations and Combinations 03 Class Notes.pdf", 42),
    ("Permutations & Combinations", "04", "Permutations and Combinations 04 Class Notes.pdf", 43),
]

def slug(chapter, lecture):
    return (chapter.lower().replace(" & ", "-").replace(" ", "-")) + f"-l{lecture}"
