# Konflikt-Simulator — open content

The rules, example sentences, templates, background texts and explainer cards
behind [konflikt-simulator.de](https://konflikt-simulator.de) and
[conflict-simulator.com](https://conflict-simulator.com), a free tool that
helps people prepare a difficult conversation. No account, no storage, no
language model: every hint the site gives comes from a rule in this
repository, and every rule carries the sentences it must catch and the
sentences it must leave alone.

This repository is content only. The engine, the website and the practice
bot are separate and not published here.

**Premise:** *Communication is not a problem to solve but a relationship to
shape.*

## The six lenses

The tool walks one conversation through six lenses. **Situation** — how heated
is it, what is at stake, should I do this alone (Glasl's escalation stages,
Watzlawick's content and relationship levels). **Myself** — what do I feel,
need and value, and what does this say about me (feelings and needs after
Rosenberg, identity after Stone, Patton and Heen, the value square after
Schulz von Thun, self-distancing after Kross). **The other** — how will they
hear my sentence, what do they want and why (four ears, interests instead of
positions, the vicious circle). **Say it** — my observable occasion, my
I-message and my checkable request, in that order. **Listen** — can I reflect
before I reply (active listening, open questions). **Repair and agree** —
how do I de-escalate, what do we agree on, and what if they say X (repair
attempts, if-then plans after Gollwitzer). Nonviolent Communication sits
inside lenses two and four; it is a foundation, not the frame.

## What is in here

```
catalog.yaml             the structure of the domain: relationships, situations, goals,
                         states, directness levels, opening styles, tones — keys only, no text
content/<lang>/
  lexicon/
    example-layer.yaml   rules for the occasion ("what would a camera have recorded?")
    impact-layer.yaml    rules for the impact (I-message with a feeling word)
    request-layer.yaml   rules for the request (positive, concrete, checkable)
    any-layer.yaml       checks that run on all three layers (yes-but, why-questions, monologue …)
  examples.yaml          example occasions, keyed relationship × situation
  impacts.yaml           example impacts, keyed situation × state
  requests.yaml          example requests: a general layer (goal × directness) and a
                         scenic layer (situation × goal × directness)
  openings.yaml          opening templates (style × tone) and follow-up questions
  ifthen.yaml            "If they say …": the feared line, a calm answer, a repair phrase
  lenses.yaml            templates for the Myself / The other / Listen screens and the card
  safety.yaml            the crisis net: patterns for self-harm and violence, and the helplines
background/<lang>/       the nine background pages (one model each) as Markdown, with sources
cards/                   the eleven explainer cards: cards.json (text), art/*.svg (drawings),
                         <lang>/*.png (rendered) — CC BY 4.0, see below
moves/moves.json         example lines per conversational move (request, need, empathy,
                         attack, contempt, repair …) in three languages
check.py                 the contributor's validator, Python only
```

`<lang>` is `de`, `en` or `es`. Every language directory holds the same set
of files; `check.py` enforces that.

## The doctrine of the three layers

The site asks for three sentences, in this order. Each layer has its own
rules, and the corpus entries of a layer are checked against the rules of
that same layer — the doctrine applies to us as well.

**Occasion — an observable fact.** The yardstick is the camera: what would a
video recording have captured? Not "you are unreliable" but "the hand-over
was agreed for Thursday; it came on Friday". Not "you keep interrupting me"
but "while I was explaining my point I was interrupted twice". Intentions are
not observable and are left out. Forbidden: generalisations (*always*,
*never*, *constantly*), attributions (*disrespectful*, *lazy*), imputed
intent (*on purpose*, *you don't care*), put-downs.

**Impact — an I-message.** The impact is yours, so it is said in the first
person, and a feeling word is mandatory — without one the rule
`feel-missing` fires. "You make me angry" becomes "I get angry". The I-form
alone is not enough: "I think you are unfair" starts with "I" and is still a
judgement about the other person. "I feel ignored" is never marked wrong,
but it says more about what the other person did than about your own
feeling, so the tool adds only a soft hint (`faux_feeling`, severity
`info`): "What do you feel underneath — hurt, sad, angry?" Genuineness
before formula.

**Request — positive, concrete, checkable.** A request is a request only if
both sides can tell afterwards whether it was met. Not "stop interrupting
me" but "I would like to finish before you answer". Not "show more respect"
but "I ask you to give me feedback by Friday".

### Requests have two layers

A request names an action, and actions belong to the occasion — so the
request layer is the only one refined by situation. The site offers the
scenic entries for the chosen situation first, in the chosen directness,
then the same scene in the other directness levels, and the general layer
last. Reading the same request once softer and once firmer is exactly the
decision one faces before a difficult conversation.

**A general entry must not name an object, a place or an occasion.** It is
the fallback for every situation. "I expect you to take my documents only
with my consent" once stood there and was wrong: flawless as a sentence, and
still a scene. A general entry becomes concrete through time and action
("by Thursday noon", "the same day"), not through the object.

Requests are checked with the directness level of the entry: a `high` entry
may contain "from now on", a `low` entry may not.

### What the examples are, and what they are not

Corpus entries do not replace the user's own wording. They are offered as
examples ("how does this sound when others say it?") so that the yardstick
becomes visible. Write them so that they work as *patterns* — concrete
enough to be understood, general enough not to read like somebody else's
story.

## How to write a rule

Rules live in `content/<lang>/lexicon/*.yaml`, grouped by `kind`. A group
carries the severity, a one-line `source` (the school or author the rule
draws on, shown under every hint), a `why` paragraph, optionally `more`
(the id of a background page) and `risk_sensitive: true` (findings of the
group are downgraded to `info` when the user chose high directness).

```yaml
- kind: generalizer
  severity: block
  source: "Thinking traps (CBT): overgeneralisation"
  more: beobachten-statt-bewerten
  why: |
    Generalisations cannot be checked and invite a counter-example. One
    "last week I was on time" tips the whole conversation onto the question
    whether "always" is true — away from the occasion you care about.
  rules:
    - id: gen-always                 # unique across all layers of the language
      match: "always|constantly"     # RE2, WITHOUT \b — see below
      message: "“{match}” is a generalisation."
      ask: "When did you last notice it concretely? Name the one occasion."
      offer:                         # optional: concrete alternatives
        - "the Tuesday hand-over did not happen"
      tests:                         # mandatory
        hits: ["You are always late"]
        misses: ["I always appreciated your help"]
```

Mandatory fields: `id`, `match`, `ask`, `tests.hits`, `tests.misses`. A rule
without an `ask` is rejected — a finding without a way forward is a
reprimand, and this product does not reprimand. `{match}` in `message` is
replaced by the matched text.

Two special rule shapes exist on a group instead of `rules`:
`absence_check` fires when *none* of the words in its `vocabulary` occurs
(this is how `feel-missing` and `req-missing-verb` work), and `length_check`
fires above `max_words`. Both carry `tests` like any other rule.

### Severities

| Severity | Meaning                                   | Shown on the site as         |
| -------- | ----------------------------------------- | ---------------------------- |
| `block`  | violates the doctrine of the layer        | "Leads into defence"         |
| `warn`   | carries, but costs effect                 | "Costs effect"               |
| `info`   | a hint                                    | "Hint"                       |

### The self-tests

Every rule brings its own evidence. `tests.hits` are sentences the rule must
match; `tests.misses` are sentences it must leave alone. The engine's build
(`make lint` in the private repository) compiles every rule and runs both
lists; a rule that does not hit its own examples, or hits one of its misses,
breaks the build. The same run checks every corpus entry against the rules
of its own layer, so an example occasion with a generalisation in it fails
the build too, and it checks coverage: every key combination of a corpus
file (`relationship × situation` for occasions, `situation × state` for
impacts, and so on) needs at least `min_per_bucket` entries, otherwise the
gap is listed.

The crisis net in `safety.yaml` works the same way: each pattern has
`hits`, optionally `unless` (figures of speech an overlapping match must not
count against) and the file ends with a `misses` list of look-alikes that no
rule of any language may catch. The patterns of all languages run on every
input, whatever the page language.

Without the Go toolchain you cannot run the rules, but `python3 check.py`
tells you whether your YAML parses, whether every rule has hits and misses,
and whether the language directories still agree. Run it before opening a
pull request; the full self-tests run when the change is pulled into the
engine.

### Pitfalls (learned the hard way)

These caused real bugs while the project was built. The self-tests found
them.

- **Never write `\b`.** Go's `\b` is ASCII-based: `\bfaul\b` matches inside
  "Fauländer" because the `ä` counts as a non-word character. Write the bare
  pattern — the loader wraps it in Unicode-aware word boundaries. For word
  endings use `\p{L}*`, never `\w*`.
- **Separable verbs need both forms.** German "zusammenreißen" appears in a
  sentence as "reiß dich zusammen". A pattern that only knows the infinitive
  misses the imperative: `dich zusammenreißen|reiß dich zusammen|reiss dich
  zusammen`. The same goes for "aufhören / hör auf", "ausreden / rede aus",
  "nachfragen / frag nach".
- **Think of nominal forms.** "unverschämt" does not match inside
  "Unverschämtheit" — the word boundary sits after the `t`, not before it.
  Add the noun when it is common.
- **Rewrites only when certain.** The impact layer holds the only automatic
  rewrites (`rewrite:` with a `template` such as `ich werde $1`). Before you
  add one, check two things: is the insertion slot closed (`\p{L}+` is almost
  always too wide — enumerate the admissible word forms), and does the
  sentence still carry after the swap (German is a verb-second language, so
  rewrites only work at the sentence start). When in doubt: no rewrite, only
  `ask`. That is always allowed and costs nothing.
- **Word forms, not lemmas.** The vocabularies of the absence checks are kept
  as word forms, not base forms — without morphological analysis the explicit
  form is the more honest solution. `req-missing-verb` is the weakest rule in
  the set: it has a tail of false positives for verbs that are not in its
  list. When one shows up, the word form belongs in the list.
- **Spanish feelings as nouns.** In the Spanish content feelings are written
  as nouns ("siento decepción") so that no sentence presupposes a gender —
  in the corpus and in the lens templates alike.

## Adding a corpus entry

The file follows the layer, the key follows the bucket:

```yaml
# content/<lang>/examples.yaml — key: relationship × situation
- { relationship: colleague, situation: misunderstanding,
    text: "I had written “draft” in the subject line; the file went to the client." }

# content/<lang>/impacts.yaml — key: situation × state
- { situation: misunderstanding, state: annoyed,
    text: "I am annoyed because the effort could have been avoided." }

# content/<lang>/requests.yaml, general layer — key: goal × risk
- { goal: change, risk: medium,
    text: "I ask you to tell me by Thursday noon where I stand with you." }

# content/<lang>/requests.yaml, scenic layer — key: situation × goal × risk
- { situation: reliability_deadlines, goal: change, risk: medium,
    text: "I ask you to look at the calendar before you commit." }
```

The keys are the values in `catalog.yaml`. Every bucket needs at least
`min_per_bucket` entries (default 2). The entry is checked against the rules
of its own layer when it is pulled into the engine.

## Adding a language

A language is one directory: copy `content/en/` to `content/<lang>/`, keep
every file name, and rewrite the texts — natively, not word by word. The
keys (`relationship`, `situation`, `state`, …) stay in English; they are the
structure in `catalog.yaml`, and the structure exists once. `lenses.yaml`
must keep the same keys as the other languages (`check.py` compares them),
`ifthen.yaml` needs the same item ids, and `safety.yaml` needs the helplines
of the countries that speak the language — see the next section. The
background pages and cards are added the same way under `background/<lang>/`
and `cards/<lang>/`. The user-facing labels of the catalog values live in the
site, not here; open an issue and we add them with the language.

## The helplines in `safety.yaml`

The `help` block of each `safety.yaml` holds the texts and numbers the site
shows instead of a rewrite when a sentence points to a crisis or to
violence. **These texts are country-specific and reproduced verbatim**: the
German file names services in Germany, Austria and Switzerland, the English
file the UK, Ireland and the USA plus an international directory, the Spanish
file Spain plus the same directory. Do not translate a help
block into another language — a number that is right in Berlin is wrong in
Bogotá. If you add a language, research the free, anonymous, round-the-clock
services for the countries that speak it, and name only numbers you have
verified. The site matches the patterns of *all* languages against every
input and shows the help text of the page language.

## Contributing

Pull requests and issues are welcome: new rules, better test sentences,
missing word forms, corpus entries for thin buckets, corrections in the
background texts, a new language. Please read [CONTRIBUTING.md](CONTRIBUTING.md)
— it is short. Keep in mind:

- This repository is an export. The private repositories of the site and
  the practice bot are the source of truth; a merged change is pulled in
  there, run through the full self-tests, and re-exported here. Expect that
  round trip rather than a direct merge.
- Content in `de`, `en`, `es` stays in its language; everything else
  (commit messages, issues, this README) is English.
- Nothing from real conversations: no sentence a real person wrote to the
  site or the bot, no names. Test sentences are invented.

## A note on Nonviolent Communication and on names

The content draws on Marshall B. Rosenberg's approach, Nonviolent
Communication (cnvc.org), alongside the other models credited in the
`source` lines and on the background pages. The author is not a
CNVC-certified trainer, and this project is not affiliated with or endorsed
by the Center for Nonviolent Communication or any of the authors and
institutes named. Trademarks and names of others are theirs; they are used
to credit ideas, not to claim association. The drawings on the cards are our
own, not reproductions of any institute's graphics.

## Licence

Everything in this repository except the `cards/` directory is licensed
under **Creative Commons Attribution-ShareAlike 4.0 International**
(CC BY-SA 4.0) — see [LICENSE](LICENSE). You may copy, adapt and
redistribute it, including commercially, as long as you credit the source
and release adaptations under the same licence.

The explainer cards in `cards/` (text, drawings and rendered images) are
licensed **CC BY 4.0** — see [cards/LICENSE](cards/LICENSE) — as already
stated on the site: print, show, hand out, adapt, with the credit. Use in
class is expressly welcome.

Attribution line for both:

> Konflikt-Simulator, Günter Weber, konflikt-simulator.de
