# Scramble to unscramble!

This is a word unscrambling game. Right now it's just a concept and likely won't go further. Try it out at http://alexmojaki.github.io/scramble_to_unscramble/

On the left is a list of words, on the right are some scrambled letters. You have to click the correct unscrambled word on the left.

If you choose correctly, the word will be removed and one new word will be added to the list. At the same time one letter in the scrambled letters will change. (the letters get rescrambled for now, but only because I haven't bothered preserving the order)

This means that what's on the screen only changes slightly with each word, and consecutive words consist of similar letters. If a word *almost* fits the scrambled letters but not quite, it's likely the next word. All words in the list will at some point soon be the correct word.

The idea is that each word can be unscrambled quite easily, and with some skill it might be possible to get into a flow and unscramble many consecutive words in a short time.

Based on this an actual game could reward solving words quickly and punish taking too long or clicking wrong. For example a simple mechanic could be that each word has to be solved correctly in under 5 seconds or the game ends, and the goal is simply to get the longest streak you can.

# Basic commands

- `poetry install` to install Python dependencies.
- `python precompute.py` to create a graph of words linking words that differ by one letter and save it to `app/src/words_data.json`.
- `python game.py` to play a text version of the game.
- Under `app`:
    - `npm install` to install dependencies.
    - `npm start` to play the game locally.
    - `npm run deploy` to deploy to GitHub pages.
    
