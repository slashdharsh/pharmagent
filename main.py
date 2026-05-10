import time
import os
from pharmagent import research_drug
from brief_writer import write_marketing_brief

# ─────────────────────────────────────────
# YOUR DRUG LIST — add or remove any drug
# ─────────────────────────────────────────
DRUG_LIST = [
    "Ozempic",
    "Humira",
    "Keytruda",
    "Jardiance",
    "Mounjaro",
    "Eliquis",
    "Dupixent",
    "Xarelto",
    "Stelara",
    "Skyrizi",
    "Tremfya",
    "Taltz",
    "Cosentyx",
    "Cimzia",
    "Enbrel",
    "Rinvoq",
    "Imbruvica",
    "Revlimid",
    "Opdivo",
    "Tecentriq",
]


def run_pharmagent(drug_name):
    """Run the full pipeline for one drug. Returns status and time taken."""
    start = time.time()

    try:
        print(f"\n{'─'*55}")
        print(f"  Processing: {drug_name.upper()}")
        print(f"{'─'*55}")

        # Step 1 & 2: Search + quick AI summary
        summary, raw_search_data = research_drug(drug_name)

        # Step 3: Full structured brief
        brief = write_marketing_brief(drug_name, raw_search_data)

        # Save to file
        os.makedirs("briefs", exist_ok=True)  # creates a 'briefs' folder if it doesn't exist
        filename = f"briefs/{drug_name.lower().replace(' ', '_')}_brief.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(brief)

        elapsed = round(time.time() - start, 1)
        print(f"  ✅ Done — saved to {filename} ({elapsed}s)")
        return {"drug": drug_name, "status": "success", "file": filename, "time": elapsed}

    except Exception as e:
        elapsed = round(time.time() - start, 1)
        print(f"  ❌ Failed — {str(e)} ({elapsed}s)")
        return {"drug": drug_name, "status": "failed", "error": str(e), "time": elapsed}


def run_all(drug_list):
    """Loop through all drugs and print a final summary report."""

    print(f"\n{'='*55}")
    print(f"  PHARMAGENT — BATCH RUN")
    print(f"  Running briefs for {len(drug_list)} drugs")
    print(f"{'='*55}")

    total_start = time.time()
    results = []

    for i, drug in enumerate(drug_list, 1):
        print(f"\n[{i}/{len(drug_list)}]", end="")
        result = run_pharmagent(drug)
        results.append(result)

        # Small pause between drugs to avoid hitting API rate limits
        if i < len(drug_list):
            time.sleep(2)

    # ── SUMMARY REPORT ──────────────────────────────
    total_time = round(time.time() - total_start, 1)
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "failed"]

    print(f"\n\n{'='*55}")
    print(f"  BATCH COMPLETE")
    print(f"{'='*55}")
    print(f"  Total drugs processed : {len(drug_list)}")
    print(f"  Successful            : {len(successful)}")
    print(f"  Failed                : {len(failed)}")
    print(f"  Total time            : {total_time}s")
    print(f"  Avg time per drug     : {round(total_time / len(drug_list), 1)}s")
    print(f"  Briefs saved to       : /briefs folder")

    if failed:
        print(f"\n  Failed drugs:")
        for r in failed:
            print(f"    ✗ {r['drug']} — {r.get('error', 'unknown error')}")

    print(f"\n  Successful briefs:")
    for r in successful:
        print(f"    ✓ {r['drug']} ({r['time']}s)")

    print(f"{'='*55}\n")

    # Resume metric — this is your quantifiable number
    if successful:
        print(f"  RESUME METRIC:")
        print(f"  Generated {len(successful)} pharma marketing briefs")
        print(f"  Avg {round(total_time / len(successful), 1)}s per brief vs ~3hrs manually")
        reduction = round((1 - (total_time / len(successful)) / 10800) * 100)
        print(f"  Time reduction: ~{reduction}% faster than manual research")
        print(f"{'='*55}\n")


# ─────────────────────────────────────────
# RUN OPTIONS — choose one:
# ─────────────────────────────────────────
if __name__ == "__main__":

    # OPTION A: Run ALL 20 drugs (full portfolio run)
    run_all(DRUG_LIST)

    # OPTION B: Run just one drug (for testing)
    # run_pharmagent("Ozempic")

    # OPTION C: Run a small custom batch (for testing before full run)
    # run_all(["Eliquis", "Dupixent", "Mounjaro"])