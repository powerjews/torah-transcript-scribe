# Torah Transcript Scribe

A Claude plugin from [PowerJews.com](https://powerjews.com) that proofreads speech-to-text transcripts of shiurim and Torah classes. YouTube captions, Whisper, Otter and Descript hear Hebrew, Aramaic and Yiddish through an English-only ear and write down the nearest English sounds: "broccoli of Hashem" for *beracha*, "Russia comments" for "Rashi comments", "the Tithariyeza" for the Tzitz Eliezer. The scribe hears what the speaker actually said and writes that down, changing nothing else.

It works for any speaker, any engine and any genre (halacha, Gemara, Chumash, Kabbalah, mussar, Chassidus, history) because it reasons from sound and context and from Claude's own knowledge of Torah vocabulary, not from a list of known errors. Ashkenazi, Sephardi, Syrian, Israeli and Chabad pronunciations are kept in the speaker's own style.

## What it does

- Restores misheard words, names and citations from the eight ways engines garble Torah speech: English look-alikes, split and merged words, phrase soup, wrong names, citation numbers, swallowed sounds, holes the engine left, and English-to-English swaps.
- Keeps the speaker's words. No paraphrase, no tidying, no deleted tangents. Every sentence that went in comes out.
- Checks every citation on Sefaria when the Sefaria connector is enabled and records the outcome per citation: verified, exists (topic unverified), or not resolvable. Not resolvable never means wrong; many responsa are not on Sefaria.
- Reads the sentence again after every fix, from a Torah perspective, so a word that now fits the sound but not the sugya is caught.
- Handles SRT and VTT caption files: every cue and timing line comes back intact so the file can go straight back onto the video, and each flagged word carries its timestamp and, for YouTube sources, a deep link that opens the audio at that second.

## What it will not do

A wrong source written with confidence is worse than a flagged garble, so the scribe follows three rules you can rely on:

- **Sources are never fixed on plausibility.** A sefer, rav, Tanna or citation is corrected only when something in the transcript anchors it (the speaker's own translation, the sugya, the printed text). Otherwise it is left as heard and the candidate is named in the review.
- **Every change is classified.** Each review opens with one trust line: how many fixes had anchors, how many carry a note, how many were flagged, and what each citation lookup returned. Words written into caption holes are listed separately as insertions with what pins each one.
- **Needs-a-human is ranked and capped.** At most five items above the fold, sources first, then names, then vocabulary, each with its timestamp or sentence and what would settle it, so a reviewer can clear them in minutes.

## Example prompts

- "Here are the YouTube auto-captions for Rabbi Mansour's class on Keriat Shema (captions.vtt). Fix the Hebrew words, keep every cue and its timing, and give me the changes with timestamps."
- "This Whisper transcript of a Daf Yomi shiur on Bava Metzia 59b has the Aramaic quotes as soup. Restore them from the sugya, keep the speaker's words, and flag what you can't pin down."
- "Proofread this transcript of a halacha shiur before we post it. Check the seforim he quotes on Sefaria and tell me which fixes you are sure of and which I should listen to."

Point Claude at a file or paste the text. The corrected transcript comes back with a Changes section (or, in file mode, a review file beside it).

## Where it runs

The skill loads in Claude chat, Cowork and Claude Code. The Sefaria connector appears on the plugin's Connectors tab in claude.ai and loads directly in Claude Code. The faithfulness script runs where Claude has a shell (Claude Code, Cowork on your computer); elsewhere Claude does the comparison by hand and says so in the review.

## What the plugin runs, sends and fetches

Everything the plugin does is in this repository, in plain text.

- `skills/torah-transcript-scribe/SKILL.md` and `references/`: instructions and reference lists Claude reads. No code.
- `skills/torah-transcript-scribe/scripts/check_faithfulness.py`: a Python standard-library script that aligns the original and corrected transcript word by word and reports dropped, added, rewritten and inserted words. It reads the two files named on its command line and writes nothing else.
- `.mcp.json`: declares Sefaria's public text server at `https://mcp.sefaria.org/mcp` as a remote connector so Claude can look up citations. The only data sent is the reference being checked (a book name, a section, a short quoted phrase). No other network access, no analytics, no credentials. See [PRIVACY.md](PRIVACY.md).

## Install

- From Anthropic's directory: **Customize > Plugins > Discover** in claude.ai or the Claude desktop app. A plugin added there also reaches your Claude Code sessions.
- From this repository in Claude Code:

```
claude plugin marketplace add designchai/torah-transcript-scribe
claude plugin install torah-transcript-scribe@powerjews
```

- For one session: `claude --plugin-dir ./torah-transcript-scribe` from a clone.

## How it was tested

The skill ships with ten evaluation transcripts (Sephardi and Ashkenazi speakers, YouTube captions and Whisper, halacha, Gemara, Kabbalah and a clean control) graded by one hundred written checks. The version in this repository passed 98 of 100 against 90 for the version before the trust rules; every miss of the earlier version was a source or name written with more confidence than the transcript allowed. The evaluation set is kept out of the public repository because its fixtures are transcripts of real classes.

## Credits

Built by [PowerJews.com](https://powerjews.com), a nonprofit that makes Jewish learning practical. Citation checks use [Sefaria](https://www.sefaria.org), an independent nonprofit library of Jewish texts. The pronunciation column of `references/spoken-forms.md` is derived from the glossary at [Judaism 101](https://www.jewfaq.org) by Tracey R. Rich, with thanks.

## Support and license

Questions and bug reports: [GitHub issues](https://github.com/designchai/torah-transcript-scribe/issues). Released under the [MIT License](LICENSE).
