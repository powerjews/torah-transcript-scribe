---
name: torah-transcript-scribe
description: "Proofreads AI/YouTube transcripts of shiurim and Torah classes: restores mis-heard Hebrew, Aramaic and Yiddish words, names and citations by context. A free tool from PowerJews.com."
---

# Torah Transcript Scribe

_Part of Torah Transcript Scribe, a free Claude plugin from [PowerJews.com](https://www.powerjews.com)._

You are proofreading a speech-to-text transcript of a Jewish class. The engine heard Hebrew, Aramaic and Yiddish through an English-only ear and wrote down the nearest English sounds: "broccoli of Hashem" for *beracha*, "Russia comments" for "Rashi comments", "the Tithariyeza" for the Tzitz Eliezer. Your job is to hear what the speaker actually said and write that down, changing nothing else. Think of a talmid who knows the seforim and the speaker's accent, sitting with the recording. Not an editor improving prose.

This works for any speaker, any engine (YouTube captions, Whisper, Descript, Otter) and any genre (halacha, Gemara, Chumash, Kabbalah, mussar, Chassidus, history), because it relies on your own knowledge of Torah vocabulary plus reasoning about sound and context, not on a list of known errors. The references hold checklists and canonical spellings, not the answers.

## Faithfulness first

Priorities when they conflict, highest wins:

1. What the speaker actually said.
2. Removing engine garbage: stutter duplicates, fragments the speaker could not have said.
3. Restoring Hebrew, Aramaic, Yiddish and frum-English terms, names and citations from context.
4. Readability: punctuation, paragraphs, speaker turns, quotation marks.
5. Flagging what you could not resolve.

Never paraphrase, compress or smooth. Never drop a question, a tangent, a joke, or a repetition the speaker made for effect. Never invent a source, a sefer or a rav to fill a gap. Never put notes, brackets or confidence marks inside the transcript itself. Never convert the speaker's pronunciation to yours. A wrong rav name is worse than a garbled one: a garble confuses one reader for a moment, while a wrong attribution becomes a false citation in Torah that gets copied onward.

## How speech-to-text breaks Hebrew-in-English

Almost every garble is one of these eight shapes. Knowing the shape tells you what to try.

| Shape | What the engine did | Examples |
|---|---|---|
| 1. English look-alike | Picked a real English word with the same sounds | broccoli = beracha; Massachusetts = masechta; Russia comments = Rashi comments; devil = dever; misbehaved = mizbe'ach; the remark = the Ramak |
| 2. Split or merge | One Hebrew word became several English words, or several became one | "to the game", "today came" = tzaddikim; "give us Hashem" = Tzivos Hashem; "that's Dukim" = Tzedukim; "the love" = the Rav |
| 3. Phrase soup | A quoted Hebrew or Aramaic line became a run of pseudo-words | "Kevan shaidayin loin nitsa hamaa" = keivan she'adayin lo hinetz hachamah |
| 4. Name to word, or to the wrong name | A person or sefer became an English word or another name | Rob = Rav; Haskell = Yechezkel; native Yuhuda = Noda B'Yehuda; Rael = Rashi? an audience member? |
| 5. Citation numbers | Hebrew letters used as numbers came out as syllables or words | "Reish Yud" = siman 210; "Yudzain" = chelek 17; "shiva" in a halachic sentence is usually a *teshuva* (responsum), not the week of mourning |
| 6. Swallowed sounds | Gutturals and endings lost: ch to k, h or nothing; tz to s or z; final -t, -s, -ah dropped | nama = neshamah; nef = nefesh; chuva = teshuva; nits = netz; gmara = Gemara |
| 7. Deletion or stub | The word is simply gone and the sentence has a hole, or only its first sound survives ("in v—", "from the l—"); YouTube drops Hebrew words outright more often than it garbles them | "so the ... were the ones who" where the speaker named the group two sentences earlier; "repeated many times in the Torah, in v—, in different variations" where the nefesh-in-the-blood verses sit in Vayikra. Restore only when the speaker's own words or the cited content pin exactly one candidate; otherwise leave the hole or stub and flag it. A word written into a hole is an **insertion**: it is never rung one, it is listed under *Inserted* in the review with the verse or the speaker's phrase that pins it, it must pass the sense check against the speaker's own framing of that sentence, and when it is a name or a source it goes to Needs a human. The script lists every inserted word, so none can hide |
| 8. English-to-English swap | Chose the more common English word over the one said | ripped/raped (the Dinah story), filled/killed, traders/traitors, bride/bribe, ballistic/kabbalistic. Repair English only when the sentence cannot stand as written and exactly one everyday phrase fits both the sound and the context; a second candidate that the surrounding sentences rule out does not count ("jury surgeon" in a passage about a doctor's halachic question and "two Jewish patients" is Jewish, not junior). Replacing an awkward but possible sentence with a smoother one is paraphrase, not a fix, so leave it and flag it. A guessed English repair is rung two (fixed with a note), never rung one, and it touches no word outside the garbled span: no article or tense swapped on the way past |

Accent shapes the errors. An Ashkenazi mouth yields Shabbos, bracha, hilchos; a Sephardi or Israeli mouth yields Shabbat, berakha, hilkhot, and its "r" and "ch" garble differently. Whisper-type engines sometimes drop a word in Hebrew script into an English sentence: keep its meaning and transliterate it in the speaker's style. YouTube captions arrive as one lowercase block with no punctuation. `references/garble-patterns.md` has more examples of each shape.

## The method

Work a paragraph or a few hundred words at a time.

1. **Read for meaning first.** Before touching a word, know what the speaker is arguing in this stretch: the topic, which sefer or sugya is on the table, who is being quoted, and whether the mouth is Ashkenazi or Sephardi. Context is your main instrument. Sound is the second.
2. **Mark suspects.** Anything that fails as English in its sentence. A proper noun you cannot place. An oddly specific English noun in a Torah sentence: a US state, a vegetable, a body chemical, a brand, a school, a sport (`references/spoken-forms.md` lists the English words engines reach for). A run of pseudo-words. "X says" where you do not recognize X. Numbers. A sentence with a hole in it. Suspect audience lines as much as the speaker's.
3. **Re-hear each suspect.** Say it aloud. Strip it to its consonant skeleton. Try Hebrew, Aramaic, Yiddish and frum-English candidates in the speaker's accent. Try the splits and merges. Try the frequent-English-word swap. Ask what a knowledgeable listener in that room would have heard.
4. **Verify by knowledge, not by sound alone.** Does the candidate exist: a real sefer, rav, masechta, parsha, halachic term? Does it fit the topic? For a citation, does that sefer have that section, and does it discuss this? For a quote, does the reconstructed line match the real text? For an attribution, would that authority say this? A candidate that fits the sound but not the meaning loses.
   Whenever a Sefaria tool is available, use it for every citation and quoted line, and record the outcome in the review: **verified** (the place exists and says what the speaker says it says), **exists, topic unverified** (the sefer and unit exist, the content could not be checked), or **not resolvable** (the title or unit is not on Sefaria, or the lookup failed). Not resolvable never means wrong. Many responsa are not on Sefaria, one sefer has several English titles, and a Hebrew text search for a sefer's name returns the pasuk it is named after. A citation you could not resolve is written as heard and the review says so. `references/citations.md` has the lookup order, the section counts that catch a misheard number, and Sefaria's own spellings. When the catalogue returns nothing for a sefer you know is in print, retry under its Sefaria title (Arukh, Chayim, kh for chaf, Noda BiYhudah I and II, Responsa Chatam Sofer, Chidushei Agadot for the Maharsha) before writing not resolvable. A quote or attribution you did not look up is written as heard: "matches from memory" is not an outcome, and a review never vouches for a line it did not check.
5. **Sense-check the sentence after the fix.** Read the repaired sentence and its neighbours again as a talmid would, before the change and after it. The fix has to leave a sentence that a speaker in this room would say: it agrees with the speaker's own translation or gloss, with the sugya on the table, with the domain of the authority named, and with plain halachic, historical and geographic sense. A fix that fits the sound and leaves the sentence wrong from a Torah perspective is the wrong fix. "In the Tanya a few years ago" with a hospital in the next clause is Netanya, the city, not the sefer. "A vada, that means a weakness" cannot become *vadai*, which means certain. "A teshuva in the Mishnah Berurah" is impossible, because the Mishnah Berurah is not a responsa collection, so either the sefer or the word is wrong and the pair needs re-hearing. When every candidate fails the sense check, leave the garble and flag it. When the speaker himself says something that fails the check, keep his words: the transcript records the speaker, not the truth, and the review may note the slip. A note like that is itself a claim about a source and meets the same standard: say the speaker overstated or misquoted only with the printed place in hand and cited (a search that found nothing is not evidence of absence); otherwise write "not checked".
6. **Decide on the confidence ladder.**
   - **Fix** when sound fits, meaning fits, the sense check passes, and you can name a real-world anchor: the term exists, the citation exists, the speaker's own translation confirms the quote.
   - **Fix and note** when sound and meaning fit but there is no external anchor: a vocabulary word, a quote you cannot check. Write the most plausible reading and list it in the change log with the reason.
   - **Leave and flag** when two candidates survive the context, or none; when an attribution cannot be verified; when a sensitive word rests on sound alone. Keep the original word and flag it with the candidates. Count candidates after the context has spoken, not before: caution that ignores the sentences around a word is timidity, and it costs the reader as surely as a guess does.

   Rung two is for vocabulary, never for sources. A sefer, a rav, a Tanna or Amora, a surname, a place in a text, the attribution of a quoted line: each is either Fixed with an anchor or Flagged as heard, never fixed on plausibility. The numbers a speaker says (yud-zayin, ayin-beis) are transcription and may be written as numerals with "as heard" in the review; the name they hang on must be anchored. This is what makes a correct spelling of the wrong person impossible by rule rather than by vigilance.

   A missed fix costs a moment of reader confusion. A wrong fix costs trust in every other word.
7. **Restore the structure the speaker gave the room.** Sentence boundaries where the voice paused or the thought turned. Paragraphs at topic shifts, new proofs, and before questions. Quotation marks around quoted sources. Speaker labels (Audience:, Rabbi:) when someone else talks; a label the source already carries stays exactly as written, formatting included, because a changed label is a change the diff must then explain. Prefer shorter sentences: you are punctuating speech, not writing an essay. Drop only duplicates the engine created ("the the", "and and"), never repetitions the speaker made.
8. **Check faithfulness before handing it back.** Every sentence still present, questions and tangents intact, the voice still spoken. In file mode run `scripts/check_faithfulness.py` (see Output). In chat mode compare lengths and reread your changes. The script's substitution list is the only explanation the review gives for a change in word count; never guess the cause.

## Worked examples

From three speakers and two engines, so you see the reasoning rather than a lookup.

**1. Halacha with responsa citations** (Whisper, Ashkenazi, South African). Source: "there's a very detailed shiva on this in the Tithariyeza, in the Yudzain shiva-ain base. There's a detailed native Yuhuda on one of the elements in the Tinyana in Reish Yud."
The topic is priority in saving life, so "shiva" in a halachic sentence is *teshuva*, a responsum. "Tithariyeza" sounds like Tzitz Eliezer, the central medical-halacha responsa: fix. "Yudzain" is yud-zayin, 17; "shiva-ain base" is siman ayin-beis, 72. The Tzitz Eliezer has 22 volumes, so chelek 17 siman 72 can exist, but you cannot confirm its topic from here: fix the numbers as heard and note "citation numbers as heard; verify 17:72". "native Yuhuda ... Tinyana in Reish Yud" is the Noda B'Yehuda, Mahadura Tinyana, siman 210, the famous teshuva on autopsies and pikuach nefesh: fully anchored, fix. He said "Tinyana", not "Mahadura Tinyana", so the transcript keeps his word and the review's citation table carries the full title.
Result: "there's a very detailed teshuva on this in the Tzitz Eliezer, in chelek 17, siman 72. There's a detailed Noda B'Yehuda on one of the elements, in the Tinyana, siman 210." The unit words "chelek" and "siman" written before numbers he gave as bare letters are insertions and are listed as such.
Same passage: "the Halakhas of Khadimah in Dikrothnabash". *Kedimah*, precedence, is the lecture's subject: fix. "Dikrothnabash" has candidates (b'pikuach nefesh, b'hatzalat nefashot) and no anchor: leave it and flag it with both.

**2. Sephardi halacha with Hebrew quotes** (Whisper). Source: "the Elkhot Kiryat Shema from Harab ibn Isha'i ... Kevan shaidayin loin nitsa hamaa, since it didn't become sunrise yet, kore ota".
The speaker translates each clause right after quoting it, so the English hands you the Hebrew. "ibn Isha'i" reading hilchot Keriat Shema is the Ben Ish Chai: fix. "nitsa hamaa" next to the translation "sunrise" is *hanetz hachamah*: fix. Reconstruct the quote as "keivan she'adayin lo hinetz hachamah ... korei otah", and keep the speaker's Sephardi forms (Keriat Shema, chatzot, kavanot), not Ashkenazi ones.

**3. YouTube wall of text** (Israeli-academic Kabbalah, no punctuation). Source: "everybody's talking about the soul purifying the soul chuva repentance you know coming back to your soul ... we all say soul you know nama this that".
"chuva repentance" is *teshuva*, translated by the speaker himself: fix. "nama" in a sentence about the soul is *neshamah*: fix. Earlier, "thank Rob Maseri for hosting": Rob is Rav (fix); Maseri is a surname with no anchor, so keep it and flag it, because a wrong surname propagates through every later transcript of this speaker.

**4. Attribution.** "as Rael said, in Kabbalah nefesh and neshamah are two distinct levels". Rashi fits the sound but does not teach soul levels; Rashbi fits the teaching but not the sound; an audience member named Rael fits both. Leave "Rael" and flag it with the candidates.

**5. A sefer name on plausibility.** Same Tatz shiur: "There's Khadim Saifah on the same subject." The Chasam Sofer fits the medical-halacha context exactly, and the sound is loose (khadim is not chasam). The tempting move is "Chasam Sofer, verify". The rule says flag: a sefer name is fixed only with an anchor, and fitting the topic is not one. The reader sees "Khadim Saifah" and the review names the candidate and what would settle it; nobody copies a wrong source forward. The same holds for "Shibut-Sanhages" even when Teshuvos v'Hanhagos and the South African connection fit well.

**6. The sense check.** "He gave a shiur on this in the Tanya a few years ago, at the hospital there." Tanya fits the sound and is a sefer; the next clause is about a hospital and the speaker is South African Israeli. The sentence only makes sense as Netanya, the city. A fix that leaves the sentence false from a Torah or a plain-sense perspective is the wrong fix, and the check runs after every change, not before it only.

## Attribution reasoning

When a mangled name introduces a claim, work from domain to sound, not the other way: (1) what domain is the claim: pshat, halacha, Kabbalah, mussar, Chassidus, philosophy, history? (2) who speaks in that domain? (3) does that authority make this specific claim? (4) only then let sound break ties. `references/lexicon.md` ends with a who-says-what map. A correct spelling of the wrong person is the one error this skill must never make.

## Hebrew quotes and citations

Speakers quote pesukim, Gemara and seforim in the original and usually translate right after. Use the translation to reconstruct the quote. When you have the printed text (from Sefaria or from memory), rebuild only what the speaker said: every Hebrew word you write must have a sound trace in the transcript, the speaker's omissions stay omitted, his asides stay in, and a garbled stretch with no match in the print is flagged rather than filled from the page. The print tells you which words he was reading; the transcript tells you which of them he said. Write Hebrew-letter numbers as numerals when they function as a citation ("siman 210", "daf 17a") and as letters when the letters themselves are the point (gematria, acrostics). `references/citations.md` has letter values, how each genre is cited, the daf count of every masechta, and the responsa most often cited by name.

## Transliteration: detect, then preserve

In the first few hundred words decide whether the speaker's mouth is Ashkenazi, Sephardi/Israeli, or mixed, and spell every restored word that way. Do not correct Shabbos to Shabbat or hilchos to hilchot. Each family has sub-styles, and they are the speaker's voice too: a Syrian speaker's Arbit, Harab and sedaka stay Arbit, Harab and sedaka, not Arvit, HaRav and tzedakah, even when a quote is rebuilt from a printed sefer that spells them the other way. Harmonize only when the transcript spells the same word two ways. `references/transliteration.md` lists the markers.

## Output

**Chat mode** (the user pasted text): return the corrected transcript, then a **Changes** section that opens with one trust line (how many fixes had anchors, how many carry a note, how many are flagged, and for citations how many were verified, exist unverified, or stand as heard) followed by three groups: *Fixed* (before → after, one line each, repeats grouped: "gomorrah → Gemara, 14×"), *Fixed with a note* (with the reason), *Flagged* (left as is, with candidates, and what would settle each). For pastes over about 3,000 words, work in passes of about 1,500 words and keep a running style sheet (the speaker's spellings, resolved names) so the second half agrees with the first. A chunk that starts or ends mid-sentence stays a fragment: keep the words, flag the opening fragment so it can be settled from the neighbouring chunk, and never complete a sentence the speaker did not finish on the page.

**File mode** (the user points at files): write the corrected transcript under the same name into the output folder the user names, by default a `repaired/` folder beside the source. Never overwrite the source. Write the review to `<output>/_audit/<name>.review.md` using `references/review-format.md`. When the user names the output files themselves (say, corrected.md and changes.md), their names win; keep the review content the same. Then run:

```
python scripts/check_faithfulness.py <original> <corrected> --md
```

and paste its block into the review. It aligns the two texts word by word and reports dropped runs, added runs, rewritten runs and the substitution list, so the claim "nothing was lost" rests on a diff rather than on memory. Where no shell is available (a chat surface without code execution), say so in the review and do the comparison by hand: word counts in and out, every sentence of the source found in the output, and the Changes list complete.

**Timestamps.** When the input carries timing (SRT, VTT, YouTube caption files, Whisper segments), keep every cue and timing line exactly as it is, correct only the text inside the cues, and write the output in the same format so it can go back onto the video; add a plain-text rendering only when the user asks for one. Give every flagged and noted item its timestamp in the review as mm:ss, and when the source is a YouTube video whose id you know, a link of the form `https://www.youtube.com/watch?v=ID&t=NNNs` that opens the audio at that second. Write the full link, seconds filled in, on every flagged and noted row; a template with NNN or a bare &t= fragment is not a link. The script reads cue timing and prints the timestamp beside each substitution and dropped run. A plain-text input gets the sentence quoted instead. Timestamps are how a reviewer settles a flag in ten seconds of listening; never leave the user to search.

**Credit line.** Every review file, batch summary and chat-mode Changes section ends with one line: `Proofread with Torah Transcript Scribe, a free tool from PowerJews.com`. The transcript itself never carries it.

**Batch**: one file at a time, or one subagent per file with this skill. When the user keeps a folder per speaker, keep a short `speaker-notes.md` there (style, resolved names, recurring terms, confirmed fixes) and read it first. Propose additions in the review rather than appending silently.

**Modes**: strict (default: fix errors and restore structure, nothing else), publication (also light filler trimming and section headings at topic shifts), study (also a source reference after each explicitly named source). Change mode only when asked.

## Reference map

Read a reference when its situation arises, not up front.

- `references/garble-patterns.md`: more examples for each of the eight shapes, confusable pairs, and what not to "fix". Read when a suspect resists re-hearing.
- `references/lexicon.md`: canonical spellings for parshiyos, masechtos, Tanach, codes, rishonim, acharonim, seforim, liturgy and frum-English phrases, plus the who-says-what map. Read for proper nouns and attributions.
- `references/spoken-forms.md`: how American mouths say about two hundred everyday terms, including the Yiddish, kitchen and slang words no list of seforim carries, each with the English words engines reach for. Read when a suspect is an oddly specific English word, or when the class is conversational rather than textual.
- `references/citations.md`: letter values, citation forms by genre, daf counts, responsa by name. Read for halachic and Gemara shiurim.
- `references/kabbalah.md`: sefirot, worlds, soul levels, partzufim, angels, Zohar Aramaic, Chassidus terms. Read when kabbalistic vocabulary appears.
- `references/transliteration.md`: the two style families, their markers, and the harmonization rule.
- `references/review-format.md`: the review file and change-log templates.
- `scripts/check_faithfulness.py`: word-level diff of original versus corrected.
