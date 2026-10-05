# Explainer cards — CC BY 4.0

Eleven cards, one idea each, at most sixty words, one drawing. Licensed
[CC BY 4.0](LICENSE): print, show, hand out, adapt — with the credit
"konflikt-simulator.de" (or "conflict-simulator.com"). Use in class is
expressly welcome.

- `cards.json` — title, text, credit and the labels inside the drawing, per
  language; `order` is the display order, `_about` the house rules.
- `art/<id>.svg` — the drawings as SVG fragments with `$placeholders`:
  colours (`$ink`, `$accent`, `$wash`, `$red`, `$amber`, `$green`, …) and
  the label words from `cards.json` (`$fact`, `$self`, `$sentence`, …).
  The site's renderer substitutes them and wraps the fragment in the card
  frame; to use a drawing on its own, replace the placeholders and add an
  `<svg viewBox="0 0 940 470">` wrapper.
- `<lang>/<id>.png` — the rendered cards as they appear on the site.

The drawings are our own; they credit the model's author ("after Schulz von
Thun") and do not reproduce any institute's graphics.

Attribution: Konflikt-Simulator, Günter Weber, konflikt-simulator.de
