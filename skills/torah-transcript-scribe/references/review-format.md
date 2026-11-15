# Review and change-log formats

_Part of Torah Transcript Scribe, a free Claude plugin from [PowerJews.com](https://www.powerjews.com)._

The transcript itself never carries notes. Everything about the work goes here, and the review is built so that the person who must check it reads the risky items first and can settle each in seconds.

## The trust line

Every review and every chat-mode Changes section opens with one line of counts, which is the only confidence score this skill gives:

```
Trust: 41 fixed with anchors · 6 fixed with a note · 3 flagged · citations: 4 verified on Sefaria, 1 exists (topic unverified), 2 as heard
```

The counts are provenance classes, not a feeling. A reader who sees "0 flagged, 0 as heard" knows every change is anchored; a reader who sees "7 as heard" knows where the risk sits. Count honestly: a word whose form only the audio can settle (bas kol or bat kol, amas or amat) is a note, not an anchored fix, however sure the meaning is. Where the script ran, the counts come from its lists (fixes from the substitution events, insertions from the Inserted list), and an item that was not changed is never listed under Fixed or Fixed with a note: a citation written as heard is a Citations row and nothing more. A change in word count is explained only from the script's substitution list; a guessed explanation is a false statement in a document whose one job is to be believed.

## Needs a human: ranked, capped, settled in seconds

List at most five items above the fold, ranked by consequence: attributions and citations first, then names (people, places, seforim), then vocabulary. Each line gives the item, its timestamp when the input had timing (else the sentence it sits in, quoted), and what would settle it. For a YouTube source the timestamp on every row is a full link with its seconds filled in, never a template. Further items go under a "More" line below. The transcript is the deliverable; the review exists so the risky changes can be checked quickly, and padding it hides the ones that matter.

## Chat mode: the Changes section

After the corrected transcript:

```markdown
## Changes

Trust: 12 fixed with anchors · 2 fixed with a note · 3 flagged · citations: 1 verified on Sefaria, 1 exists (topic unverified), 0 as heard

**Style detected:** Sephardi (Keriat Shema, Shabbat, kavanot). Speaker: Rabbi Eli Mansour (from the title).

**Needs a human**
- 04:12 "Dikrothnabash": kedimah b'pikuach nefesh? b'hatzalat nefashot? Ten seconds of audio settles it.
- 11:40 "Rael" in "as Rael said": an audience member, or Rashi? The claim is Kabbalah, which Rashi does not teach, so Rashi is unlikely.
- "Maseri" (host's surname, in "thank Rav Maseri for hosting"): spelling unverified.

**Fixed** (sound, meaning, the sense check and a real anchor all agree)
- Harab ibn Isha'i → the Ben Ish Chai (the sefer being read)
- Kiryat Shema → Keriat Shema, 9×
- Amouda Shahar → amud hashachar (speaker translates "dawn")
- nitsa hamaa → hanetz hachamah, 3× (speaker translates "sunrise")

**Fixed with a note** (vocabulary that is plausible, no outside anchor)
- chelek 17 siman 72 (Tzitz Eliezer): numbers as heard; Sefaria lookup: not resolvable.
- "as I'll show you where" → "as I'm sure you're aware": English repair on sound; the original cannot stand as spoken.

**Inserted** (words written into holes the engine left; each with what pins it)
- 02:31 neshamah, in "blew a ___ into him": Bereishit 2:7, which he translates in the same breath.
- 03:05 ruach, in "the ___ of Elokim hovering": Bereishit 1:2.

**Flagged** (left as heard)
- "Khadim Saifah": Chasam Sofer fits the medical-halacha context, the sound is loose, and a sefer name is never fixed on plausibility. Needs the audio.

**Citations**
- Noda B'Yehuda, Mahadura Tinyana 210 — exists; topic (autopsies and pikuach nefesh) known from the sugya; Sefaria lookup: not resolvable by title
- Berachos 17a — verified on Sefaria

_Proofread with Torah Transcript Scribe, a free tool from PowerJews.com_
```

Group repeated fixes with a count. Keep the whole section short enough to read in a minute.

## File mode: `<output>/_audit/<name>.review.md`

```markdown
# Review: <transcript name>

Trust: <counts as above>

**Speaker:** <name or "unidentified">  **Style:** Ashkenazi / Sephardi / mixed  **Mode:** strict / publication / study
**Engine (guess):** YouTube captions / Whisper / other  **Input timing:** none / SRT / VTT  **Words in → out:** 6,171 → 6,180

## Needs a human (read this first)
1. <timestamp or quoted sentence> — <item> — <what settles it>
2. ...
(at most five; attributions and citations first, then names, then vocabulary)
More: <one line listing the rest, or "none">

## Citations
| As spoken | Written | Outcome |
|---|---|---|
| "the Tithariyeza, Yudzain shiva-ain base" | Tzitz Eliezer, chelek 17, siman 72 | exists (22 volumes); topic unverified; Sefaria: not resolvable |
| "Brachos yud zayin" | Berachos 17a | verified on Sefaria (Rav's prayer) |

## Fixed
- before → after (count) — anchor in one phrase — timestamp of first occurrence when timed
(one line per distinct fix; group repeats)

## Fixed with a note
- before → after — why plausible, what is unverified — timestamp
(guessed English repairs belong here, never under Fixed)

## Inserted
- timestamp word, in "the sentence with ___" — the verse or the speaker's phrase that pins it
(every word that was not in the source; the script's Inserted list must match this one)

## Flagged (left as heard)
- timestamp "garble" — candidates, and what would settle it

## Speaker notes to carry forward
- Recurring terms and their spellings, resolved names, recurring garbles for this speaker (propose; the user merges into speaker-notes.md)

## Faithfulness check
(paste the --md block from scripts/check_faithfulness.py; with a timed input its substitutions carry timestamps)

_Proofread with Torah Transcript Scribe, a free tool from PowerJews.com_
```

## Batch summary: `<output>/_audit/_batch_summary.md`

After a batch, one file: files processed, one trust line per file and one for the batch, the five items most worth a human's time across all files with their timestamps, the speaker notes proposed, and any pattern that recurred across files (a garble that appears in three or more files is worth adding to speaker-notes.md). It ends with the same credit line as the reviews.

## What not to log

Do not log every punctuation decision, every "the the" removed, or confirmations of fixes that need no review. Do not list a citation twice because it recurs; give it once with its outcome and count. Do not write "matches from memory", "checked from memory" or any other verification you did not perform: a quote or citation you did not look up is as heard, and the review says so.
