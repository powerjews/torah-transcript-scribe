# Privacy policy: Torah Transcript Scribe

_Effective 2026-11-15. Published by Power Jews Corporation (PowerJews.com), a New Jersey nonprofit._

Torah Transcript Scribe is a plugin for Claude. It is a set of written instructions and reference lists that Claude follows when you ask it to proofread a transcript, plus one small script that compares two text files. The plugin has no server, no account, no database and no analytics of its own.

## What the plugin does with your data

- **Your transcripts stay in your Claude conversation.** The plugin does not copy, store, upload or transmit them anywhere. Anthropic's own privacy policy and your plan's data terms govern what happens to content inside Claude.
- **Nothing is collected about you.** The plugin does not read your name, email, contacts, files you did not hand it, or anything about your device. It keeps no logs.
- **One optional connection to Sefaria.** The plugin declares Sefaria's public text server (`https://mcp.sefaria.org/mcp`) as a connector so Claude can check the citations a speaker gives. When that connector is enabled, Claude sends Sefaria the reference it is checking: a book name, a section number, or a short quoted phrase from the transcript. It does not send the transcript itself. Sefaria is an independent nonprofit; its handling of requests is described in its own privacy policy at https://www.sefaria.org/privacy-policy. If you leave the connector off, no request leaves Claude, and the plugin records every citation as "as heard".
- **The faithfulness script runs on your machine.** In Claude Code or any environment with a shell, Claude may run `scripts/check_faithfulness.py` to compare the original and corrected transcript word by word. The script reads the two files you name, prints a report, and writes nothing except the output files you asked for.

## What the publisher sees

Anthropic's plugin directory shows publishers aggregate usage figures for a listed plugin, such as install counts. PowerJews receives no transcript content, no prompts and no personal data through the plugin.

## Children

The plugin is a text proofreading tool for general audiences. It is not directed at children under 13 and collects no data from anyone.

## Changes and contact

Changes to this policy are published in this repository with a new effective date. Questions go to the issue tracker at https://github.com/powerjews/torah-transcript-scribe/issues or through the contact form at https://powerjews.com.
