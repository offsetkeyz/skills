---
name: find-your-voice
description: Discover and document a person's real writing voice through short impromptu writing exercises, then turn it into a reusable voice profile and a personal "write like me" skill. Use this whenever someone wants AI to write blogs, posts, emails, or newsletters that sound like them but has no writing samples, doesn't know their style, says their AI drafts sound generic, or asks to "find my voice", "train AI on my writing", "build a style guide from my writing", or "create a writing-style skill". Also use it to evaluate a handful of pasted samples and extract the style patterns in them.
---

# Find Your Voice

Most people can't describe their own writing style, and AI drafts built from adjectives ("professional but friendly") come out generic. People can usually *produce* their voice on demand, though, if they write fast and don't polish. This skill runs that process: prompt, evaluate, repeat, then synthesize a profile and package it as a skill that drafts in their voice.

The evaluation is the product. Every claim about someone's style must be backed by something they wrote, because a profile that flatters or guesses is worse than none.

## Principles

- **Raw beats polished.** Unedited, unassisted writing carries the signal. Ask for 150-300 words, no editing, no AI help, dictation welcome.
- **One prompt at a time.** Feed prompts individually so each sample gets a real evaluation and the next prompt can target a gap.
- **Evidence over adjectives.** Cite short quotes from their samples for every pattern. If a pattern appears once, label it "seen once".
- **Separate voice from flaws.** Distinctive habits are voice. Filler, repetition, and buried punchlines are things to trim. A style that copies every flaw reads as sloppy, not authentic. Keep the two lists apart.
- **Style only.** Describe how they write, not who they are. No personality diagnoses, no guesses about their life or feelings.
- **Respect privacy.** Samples often mention employers, coworkers, or customers. Don't carry identifying details into the profile or any file meant to be shared, and tell the person which samples are voice-only and not publishable. Name people by role ("a customer"), never by name, even when talking to the person who wrote the sample.

## Workflow

### 1. Intake (at most three questions, skip any already answered)

- What will the AI write for you? (blogs, LinkedIn, newsletters, emails, scripts)
- Who reads it, and what should they think of you afterward?
- Name 1-3 writers or posts you like, and 1-3 you'd hate to sound like.

If the person is unsure, move on. Their samples will answer more than their descriptions.

If they say they hate writing, are stuck, or have nothing written down, lead with the **taste test** (see step 4 and `references/prompt-bank.md`) in your first reply instead of a writing prompt. Reacting to styles is far easier than writing from a blank page, and asking a reluctant writer for 150 words first is the fastest way to lose them. Dictated samples come after their picks.

### 2. Impromptu rounds

Read `references/prompt-bank.md`. Pick the first prompt from the "Warm-up" bucket, adapted lightly to their context. State the rules in two lines, then send the single prompt.

After each sample, run the evaluation (step 3), then choose the next prompt to fill a gap: a register not yet seen, a format they'll actually publish, or a pattern that needs a second data point. Cover at least three of the four buckets. Skip any prompt that feels forced and swap it.

### 3. Evaluate each sample

Read `references/evaluation-rubric.md` once, then for every sample reply in this shape, kept short:

- **Voice signals** (what's distinctive, each with a quote)
- **Flags** (filler, repetition, hedges, buried point, corporate or generic drift)
- **Best line** (one sentence worth keeping as-is)
- **Running profile** (bullets, with a confidence level)
- **Next prompt**

Keep notes tight. The person is writing, not reading essays about their writing.

**Check before sending.** Write the draft reply to a file and run:

```
python scripts/check_evaluation.py --samples <sample files> --reply <draft reply file>
```

It reports each sample's real word count, quoted phrases that aren't verbatim in the samples, and possible third-party names. Fix what it flags. Three things went wrong in testing without this step, and each one makes the rest of the evaluation harder to trust:

- **Estimated measurements.** A reply said a sample "runs about 170 words" when it was 132. Use the printed count, and if a sample is under about 150 words, say so lightly and carry on, since short samples still carry signal.
- **Reworded quotes.** "show me it works" was quoted where the sample said "show them it works". Inside quotation marks, copy exactly. Trim with an ellipsis, never by rewording or reordering. If you're paraphrasing, drop the quotation marks.
- **Names leaking.** A customer's full name appeared in a reply that was supposed to protect it. Refer to people in samples by role ("a customer", "a coworker"), in replies to the person as well as in the profile.

The script ignores quote-style differences and flags intentional non-sample quotes too (intake wording, labels, generic examples), so skip those.

### 4. Know when to stop

Stop prompting when either of these is true:

- 6-8 samples across at least three buckets, or
- two consecutive samples added nothing new to the profile (convergence).

If the person stalls or dislikes writing from scratch (or said so at intake), use the **taste test** from the prompt bank: one topic written in five or six distinct styles. Their picks and rejections become the profile seed, and the next raw samples confirm or correct it.

### 5. Synthesize

Read `references/profile-template.md` and fill it in. Rules:

- Every item cites a sample or says "stated preference" if it came from intake.
- Mark confidence per section: high (3+ samples), medium (2), low (1).
- Include a **register map** (how voice shifts between casual, work, and opinion writing).
- Include **anti-patterns** drawn from their flaws and from generic AI tells, so drafts avoid both.
- Include **open questions** that edits will resolve, such as joke density or preferred length.

Show the profile and ask for corrections before packaging anything.

### 6. Package as a personal skill

Read `references/output-skill-template.md` and build a skill folder named `my-writing-style` (or a name they choose) containing a SKILL.md, the profile, an anti-patterns file, a feedback log, and their approved samples. Use the skill-creator workflow to validate and package it when available. If a skill-proposal or file-delivery tool is available, use it so they can install it with one click.

### 7. Calibrate with a real draft

Write one real draft on a topic they choose, using the new profile. Mark two or three spots where you were unsure. Ask them to edit it. Diff their version against yours, extract the *pattern* behind each change (not just the words), append it to the feedback log, and promote any pattern that shows up twice into the profile. Repeat until edits get light.

## Failure modes to avoid

- Declaring a voice after one sample. One sample gives a hypothesis, not a profile.
- Inventing anecdotes, numbers, or quotes when drafting. Use a placeholder and ask for a real example.
- Praising everything. If a sample is generic, say so and point to the line that wasn't.
- Over-fitting to topic. Content they wrote about is not style. "Writes about sprint demos" is not a voice trait.
- Letting the profile grow past what the evidence supports. Fewer, well-cited patterns beat a long list.
- Stating measurements (word counts, sentence lengths, frequencies) without counting them.
- Contradicting yourself across sections. A habit belongs in one list: voice, trim, or open questions.
