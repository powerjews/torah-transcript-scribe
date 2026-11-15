#!/usr/bin/env python3
"""Word-level faithfulness check between an original transcript and its corrected version.

Part of Torah Transcript Scribe, a free Claude plugin from PowerJews.com (MIT license).

Usage:
    python check_faithfulness.py ORIGINAL CORRECTED [--md] [--json] [--min-run N] [--top N]

The two files are aligned word by word (markdown headings, blockquote markers,
speaker labels, and SRT/VTT cue numbers, timing lines and inline tags are ignored).
The report lists:

  dropped runs         original text with no counterpart in the corrected version
  added runs           corrected text with no counterpart in the original
  rewritten runs       long English stretches replaced by other long stretches (paraphrase risk)
  reconstructed quotes long transliterated (non-English) runs rebuilt into a real quote: expected
                       for garbled Hebrew; listed so each can be checked against its source
  substitutions        short before -> after pairs, grouped, which are the actual fixes

When the original carries SRT or VTT timing, every substitution and dropped run is
reported with the timestamp of the cue it sits in, and the corrected file must keep the
same number of cues with the same timing lines (a corrected caption file goes back onto
the video, so its structure is part of faithfulness).

Exit code 0 when no run of --min-run words or more was dropped or rewritten, the
word-count ratio stays within 0.90 to 1.12, and (for timed input) the cue structure is
intact; exit code 1 otherwise. The check proves that nothing was lost or rephrased.
It does not judge whether a fix is right.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys

WORD = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)
LABEL = re.compile(r"\*\*[^*\n]{1,40}:\*\*")
TIMING = re.compile(
    r"^\s*(?:(\d{1,2}):)?(\d{1,2}):(\d{2})[.,](\d{1,3})\s*-->\s*(?:(\d{1,2}):)?(\d{1,2}):(\d{2})[.,](\d{1,3})"
)
CUE_INDEX = re.compile(r"^\s*\d+\s*$")
INLINE_TAG = re.compile(r"<[^<>\n]{1,80}>")
HEADER_WORDS = ("WEBVTT", "NOTE", "STYLE", "REGION", "Kind:", "Language:")

# Common English function words. A replaced run made mostly of these is an English sentence
# that was rephrased (paraphrase risk). A run with almost none of them is transliterated
# Hebrew/Aramaic "phrase soup" that was reconstructed into the real quote, which is the
# job, not a paraphrase.
ENGLISH = set("""
the a an and or but so if then than that this these those there here is are was were be been
being am do does did done have has had having will would shall should can could may might must
of to in on at by for from with without into onto over under up down out off about above below
between through during before after again further once because as until while what which who
whom whose where when why how all any both each few more most other some such no nor not only
own same too very just also even ever never always now one two three it its he she they them
his her their our your my me you we i us him it's don't doesn't didn't isn't aren't wasn't
weren't can't couldn't won't wouldn't let's you're we're they're i'm he's she's that's there's
know mean say says said like right okay well yeah yes get got go going come thing things way
people person time year day very really actually basically something anything nothing everything
""".split())


def read(path: str) -> str:
    with open(path, encoding="utf-8-sig") as handle:
        return handle.read()


def strip_markup(text: str) -> str:
    text = re.sub(r"^\s{0,3}#{1,6}\s.*$", "", text, flags=re.M)  # headings are not spoken words
    text = re.sub(r"^\s{0,3}>\s?", "", text, flags=re.M)
    text = LABEL.sub(" ", text)
    text = INLINE_TAG.sub(" ", text)
    text = text.replace("*", " ").replace("_", " ")
    return text


def is_timed(text: str) -> bool:
    return any(TIMING.match(line) for line in text.splitlines())


def format_time(match: re.Match) -> str:
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def tokens(text: str) -> tuple[list[str], list[str | None], list[str]]:
    """Return (words, time of each word or None, timing lines in order)."""
    if not is_timed(text):
        return WORD.findall(strip_markup(text)), [], []
    out: list[str] = []
    times: list[str | None] = []
    cues: list[str] = []
    current: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(HEADER_WORDS):
            continue
        timing = TIMING.match(line)
        if timing:
            current = format_time(timing)
            cues.append(" ".join(stripped.split()))
            continue
        if CUE_INDEX.match(line):
            continue
        for word in WORD.findall(strip_markup(line)):
            out.append(word)
            times.append(current)
    return out, times, cues


def norm(word: str) -> str:
    return word.lower().replace("’", "'")


def english_share(items: list[str]) -> float:
    if not items:
        return 0.0
    return sum(1 for t in items if norm(t) in ENGLISH) / len(items)


def analyse(original: str, corrected: str, min_run: int) -> dict:
    a, times_a, cues_a = tokens(original)
    b, _times_b, cues_b = tokens(corrected)
    timed = bool(times_a)

    def when(index: int) -> str | None:
        if not timed or not a:
            return None
        index = min(max(index, 0), len(times_a) - 1)
        return times_a[index]

    matcher = difflib.SequenceMatcher(None, [norm(w) for w in a], [norm(w) for w in b], autojunk=False)

    dropped: list[dict] = []
    added: list[dict] = []
    rewritten: list[dict] = []
    reconstructed: list[dict] = []
    subs: dict[tuple[str, str], dict] = {}

    def note_sub(before: str, after: str, time: str | None) -> None:
        entry = subs.setdefault((before, after), {"count": 0, "times": []})
        entry["count"] += 1
        if time and len(entry["times"]) < 5 and time not in entry["times"]:
            entry["times"].append(time)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        before = " ".join(a[i1:i2])
        after = " ".join(b[j1:j2])
        time = when(i1 if tag != "insert" else i1 - 1)
        if tag == "delete":
            if i2 - i1 >= min_run:
                dropped.append({"text": before, "time": time})
            else:
                note_sub(before, "", time)
        elif tag == "insert":
            if j2 - j1 >= min_run:
                added.append({"text": after, "time": time})
            else:
                note_sub("", after, time)
        else:
            if (i2 - i1) >= min_run and (j2 - j1) >= min_run:
                # Mostly English function words on both sides: an English sentence was
                # rephrased. A non-English original, or a non-English result, means a
                # transliterated run was rebuilt into a Hebrew/Aramaic quote: nobody
                # paraphrases English into Aramaic, so that is reconstruction, not rewriting.
                # Garbled soup often splits one Hebrew word into several tokens, so a rebuilt
                # quote is usually shorter than the soup; length only matters when the
                # original side reads as English.
                similar_length = 0.6 <= (j2 - j1) / (i2 - i1) <= 1.7
                if english_share(a[i1:i2]) < 0.34 or (similar_length and english_share(b[j1:j2]) < 0.25):
                    reconstructed.append({"before": before, "after": after, "time": time})
                else:
                    rewritten.append({"before": before, "after": after, "time": time})
            elif (i2 - i1) - (j2 - j1) >= min_run:
                # A long run shrank into a short one. Soup that collapses into a real
                # quote ("nits who knee by nigh" -> "nitzchuni banai") is reconstruction;
                # an English run that shrank is a real drop.
                rebuilt_is_hebrew = (j2 - j1) >= 2 and english_share(b[j1:j2]) < 0.25
                if english_share(a[i1:i2]) < 0.34 or rebuilt_is_hebrew:
                    reconstructed.append({"before": before, "after": after, "time": time})
                else:
                    dropped.append({"text": before, "time": time})
            else:
                note_sub(before.lower(), after, time)

    ratio = (len(b) / len(a)) if a else 0.0
    sentences_in = len(re.findall(r"[.!?]", original))
    sentences_out = len(re.findall(r"[.!?]", corrected))
    cue_problems: list[str] = []
    if timed:
        if len(cues_a) != len(cues_b):
            cue_problems.append(f"cue count changed: {len(cues_a)} in, {len(cues_b)} out")
        else:
            changed = [(x, y) for x, y in zip(cues_a, cues_b) if x != y]
            if changed:
                cue_problems.append(f"{len(changed)} timing lines differ, first: '{changed[0][0]}' -> '{changed[0][1]}'")
    structure_ok = not cue_problems
    verdict = "PASS" if (not dropped and not rewritten and 0.90 <= ratio <= 1.12 and structure_ok) else "WARN"
    substitutions = sorted(((k, v) for k, v in subs.items() if k[0]), key=lambda kv: (-kv[1]["count"], kv[0]))
    inserted = sorted(((k, v) for k, v in subs.items() if not k[0]), key=lambda kv: (-kv[1]["count"], kv[0]))
    return {
        "inserted_words": [
            {"word": k[1], "count": v["count"], "times": v["times"]}
            for k, v in inserted
        ],
        "inserted_word_events": sum(v["count"] for _, v in inserted),
        "verdict": verdict,
        "timed": timed,
        "cues_in": len(cues_a),
        "cues_out": len(cues_b),
        "cue_problems": cue_problems,
        "words_in": len(a),
        "words_out": len(b),
        "ratio": round(ratio, 3),
        "sentence_marks_in": sentences_in,
        "sentence_marks_out": sentences_out,
        "distinct_substitutions": len(subs),
        "substitution_events": sum(v["count"] for v in subs.values()),
        "dropped_runs": dropped,
        "added_runs": added,
        "rewritten_runs": rewritten,
        "reconstructed_runs": reconstructed,
        "substitutions": [
            {"before": k[0], "after": k[1], "count": v["count"], "times": v["times"]}
            for k, v in substitutions
        ],
    }


def stamp(time: str | None) -> str:
    return f"{time} " if time else ""


def render_md(result: dict, top: int) -> str:
    return _render_md_body(result, top) + "\n\n_check_faithfulness.py, Torah Transcript Scribe by PowerJews.com_"


def _render_md_body(result: dict, top: int) -> str:
    lines = [
        "### Faithfulness check",
        "",
        f"- **Verdict:** {result['verdict']}",
        f"- **Words:** {result['words_in']} → {result['words_out']} (ratio {result['ratio']})",
        f"- **Sentence marks:** {result['sentence_marks_in']} → {result['sentence_marks_out']}",
        f"- **Substitutions:** {result['substitution_events']} events, {result['distinct_substitutions']} distinct",
        f"- **Dropped runs:** {len(result['dropped_runs'])}  **Added runs:** {len(result['added_runs'])}  **Rewritten runs:** {len(result['rewritten_runs'])}  **Reconstructed quotes:** {len(result['reconstructed_runs'])}",
        f"- **Inserted words:** {result['inserted_word_events']} (words with no counterpart in the original; each needs a stated pin in the review)",
    ]
    if result["timed"]:
        cue_note = "intact" if not result["cue_problems"] else "; ".join(result["cue_problems"])
        lines.append(f"- **Cues:** {result['cues_in']} → {result['cues_out']}, timing {cue_note}")
    for title, key in (("Dropped (original text missing from the corrected version)", "dropped_runs"),
                       ("Added (corrected text with no source in the original)", "added_runs")):
        if result[key]:
            lines += ["", f"**{title}**"]
            lines += [f"- {stamp(run['time'])}\"{run['text']}\"" for run in result[key]]
    if result["rewritten_runs"]:
        lines += ["", "**Rewritten (paraphrase risk)**"]
        lines += [f"- {stamp(r['time'])}\"{r['before']}\" → \"{r['after']}\"" for r in result["rewritten_runs"]]
    if result["reconstructed_runs"]:
        lines += ["", "**Reconstructed quotes (transliterated runs rebuilt; confirm each against its source)**"]
        lines += [f"- {stamp(r['time'])}\"{r['before']}\" → \"{r['after']}\"" for r in result["reconstructed_runs"]]
    if result["inserted_words"]:
        lines += ["", "**Inserted words (not in the original)**"]
        for ins in result["inserted_words"]:
            count = f" ({ins['count']}×)" if ins["count"] > 1 else ""
            times = f" [{', '.join(ins['times'])}]" if ins["times"] else ""
            lines.append(f"- {ins['word']}{count}{times}")
    if result["substitutions"]:
        lines += ["", f"**Substitutions (top {min(top, len(result['substitutions']))})**"]
        for sub in result["substitutions"][:top]:
            count = f" ({sub['count']}×)" if sub["count"] > 1 else ""
            times = f" [{', '.join(sub['times'])}]" if sub["times"] else ""
            lines.append(f"- {sub['before'] or '∅'} → {sub['after'] or '∅'}{count}{times}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("original")
    parser.add_argument("corrected")
    parser.add_argument("--md", action="store_true", help="print a markdown block for the review file")
    parser.add_argument("--json", action="store_true", help="print the full result as JSON")
    parser.add_argument("--min-run", type=int, default=6, help="words in a run before it counts as dropped/added/rewritten (default 6)")
    parser.add_argument("--top", type=int, default=40, help="substitutions to list in markdown (default 40)")
    args = parser.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    result = analyse(read(args.original), read(args.corrected), args.min_run)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_md(result, args.top))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
