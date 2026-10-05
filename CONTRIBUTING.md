# Contributing

Thank you for looking. This is how a change gets in.

1. **Pick the file by layer and language.** Rules go to
   `content/<lang>/lexicon/`, example sentences to `examples.yaml`,
   `impacts.yaml` or `requests.yaml`, background corrections to
   `background/<lang>/`. The README explains the layers and the rule format.
2. **Every rule brings its tests.** At least one sentence in `hits` and one
   in `misses`. Think of the miss first: what everyday sentence must this
   rule *not* catch? Every corpus entry must itself pass the rules of its
   layer (no "always", a feeling word in an impact, no object in a general
   request).
3. **Run `python3 check.py`** before you open the pull request. It needs
   only PyYAML. The full self-tests run in the engine when the change is
   pulled in; if they fail we will come back to you with the failing
   sentence.
4. **Invent your sentences.** Nothing from a real conversation, no names of
   real people, nothing a user wrote to the site or the bot.
5. **Keep the language of the content.** German content in German, English
   in English, Spanish in Spanish, written natively rather than translated.
   Commit messages, issues and comments in English.
6. **Helplines are country-specific.** Change a number in `safety.yaml`
   only with a source, and never copy one language's help block into
   another.
7. **Credit the model, not an institute.** A group's `source` line names the
   author or school the rule draws on, in your own words. No programme
   names, no institute graphics, no quotations longer than a line.

Issues are as welcome as pull requests: a sentence the site got wrong (with
the sentence), a false positive of a rule, a thin bucket, a missing
language.

By contributing you agree that your contribution is licensed under
CC BY-SA 4.0 (and CC BY 4.0 for the cards), like the rest of the repository.
