# Evaluation Rubric

Use this to evaluate each impromptu sample. The goal is a profile grounded in evidence, so quote the text for every observation.

Contents: dimensions, voice vs. flaw, confidence levels, per-sample output format, scoring a draft against a profile.

## Dimensions

For each sample, look at these. Note only what's distinctive. Skip dimensions with nothing to say.

1. **Opening move.** Starts with a claim, a feeling, a scene, a question, or context? How fast does it reach the point?
2. **Sentence rhythm.** Length variety, fragments, run-ons, short punches after long sentences. Estimate typical length and how much it varies.
3. **Diction.** Plain or formal, contractions, idioms, jargon, slang. What register do they default to?
4. **Rhetorical moves.** Contrast (said vs. did), lists, analogy, repetition for effect, rhetorical questions, understatement, exaggeration.
5. **Humor.** None, dry, playful, self-deprecating, sarcastic. How is it delivered: a single line, an extended bit, implied?
6. **Specificity.** Concrete details (names, numbers, objects, moments) versus abstractions. Does one detail carry the point?
7. **Stance.** How they relate to the topic and reader: teacher, peer, skeptic, advocate, storyteller. Do they hedge or commit?
8. **Structure.** How they organize: chronological, claim-then-evidence, list, story-then-moral. Where does the point land?
9. **Closing move.** Ends on a plain statement, a punchline, a call to action, a trailing thought, or abruptly?
10. **Quirks.** Recurring words, punctuation habits, signature phrases.

## Voice vs. flaw

Sort observations into two lists. This matters because copying flaws makes drafts sound sloppy.

- **Voice (keep):** distinctive and deliberate-seeming. Deadpan understatement. A habit of ending on the uncomfortable truth. Contractions and idioms.
- **Flaws (trim):** filler words ("really", "just", "basically" used reflexively), hedges that weaken the best line ("in my opinion"), repeating the key noun three or more times, burying the strongest line at the end, over-explaining setup, trailing filler like "and things like that", jargon drift when describing roles.

A habit goes in one list only. If it's ambiguous (for example, a word repeated three times that might be a deliberate rant device or might be filler), put it under open questions and ask, rather than listing it as both voice and flaw. Check the register map against the trim list before showing the profile, since this is where contradictions creep in.

Test: if the writer deleted it on a second pass and the sentence got better, it's a flaw. If deleting it flattens the sentence, it's voice.

## Confidence levels

- **Seen once:** one sample. Treat as hypothesis.
- **Medium:** two samples, or one sample plus a stated preference that agrees.
- **High:** three or more samples across at least two registers.

A pattern seen only in one register (say, rants) is flagged as register-specific, not general.

## Per-sample output format

Keep each evaluation under roughly 200 words.

```
## Sample N notes

**Voice signals**
- <pattern> ("<short quote>")

**Flags**
- <flaw> ("<short quote>")

**Best line:** "<quote>"

## Running profile (N samples, <confidence>)
- <bullet per established pattern, with confidence>

## Next
<single prompt, chosen to fill a gap>
```

## Evaluating generic output

If a sample is generic (could have been written by anyone, no concrete detail, stock phrases), say so kindly and specifically. Point to the one line that wasn't generic and ask for a rewrite of the same prompt in a more spoken way, or swap the prompt. Do not invent distinctiveness that isn't there.

## Scoring a draft against a profile

When checking a draft you wrote from the profile (before showing it), score each item pass/fail and fix failures:

- Opens with the point or scene, not a warm-up
- At least one concrete detail doing real work
- Signature move present where it fits (for example, a contrast)
- No filler words from the person's trim list
- No key noun repeated more than twice
- No generic AI tells (see the anti-patterns list in the profile)
- Register matches the format (opinion vs. work-facing)
- No invented facts, anecdotes, or quotes

Report failures you fixed in one line, not a full audit.
