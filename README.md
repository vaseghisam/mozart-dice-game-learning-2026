# Mozart Dice Game Learning

A Jupyter/Python implementation of the musical dice game attributed to Wolfgang Amadeus Mozart, extended with two small probabilistic learning models.

The program generates complete waltzes by selecting precomposed WAV fragments for:

* a 16-measure minuet,
* a 16-measure trio.

It compares three generators:

1. a historical dice-based generator,
2. a learned position model,
3. a learned transition model.

The selected WAV fragments are concatenated into playable audio files.

## What the project demonstrates

The historical generator uses:

* two six-sided dice for the minuet,
* one six-sided die for the trio.

The learned position model estimates

```text
P(variant | part, position)
```

The learned transition model estimates

```text
P(current variant | previous choice, current position)
```

These are deliberately small and transparent models. They do not generate new notes or learn Mozart’s compositional style from raw audio. They learn probability distributions over existing musical fragments.

## Requirements

* Python 3.9 or later
* Jupyter Notebook or JupyterLab
* `pydub`
* `ffmpeg`

Install the Python package with:

```bash
pip install pydub
```

On macOS, install `ffmpeg` with:

```bash
brew install ffmpeg
```

## WAV files

The WAV fragments are not included in this repository.

A compatible collection is available from Kevin Wayne’s Mozart Musical Dice Game assignment:

```text
https://nifty.stanford.edu/2023/wayne-musical-dice-game/
```

Download the archive named:

```text
mozart.zip
```

After extraction, choose one instrument folder, such as `piano`, `clarinet`, or another available instrument.

The code expects filenames such as:

```text
minuet0-2.wav
minuet0-3.wav
...
minuet15-12.wav

trio0-1.wav
trio0-2.wav
...
trio15-6.wav
```

The position numbers run from `0` to `15`.

## Configure the audio path

In the notebook or script, edit:

```python
audio_directory = Path("/PUT/YOUR/FOLDER/PATH/HERE")
```

Example on macOS:

```python
audio_directory = Path("/Users/yourname/Downloads/mozart/piano")
```

The selected folder must directly contain the WAV files.

## Run the project

Open the notebook:

```text
mozart_dice_game.ipynb
```

Set the correct `audio_directory`, then run the main code cell.

The program will:

1. check the WAV folder,
2. generate a historical dice waltz,
3. create synthetic training data,
4. train the position model,
5. train the transition model,
6. generate one waltz from each learned model,
7. export three WAV files.

## Generated output

The code creates:

```text
historical_dice_waltz.wav
learned_position_model_waltz.wav
learned_transition_model_waltz.wav
```

The files are saved in the current working directory.

In Jupyter, check that directory with:

```python
from pathlib import Path

print(Path.cwd())
```

## Important limitation

The learned models do not create new musical measures.

They only select among existing WAV fragments.

The musical structure remains largely encoded in the original fragment table. The models learn how to sample from that table.

## Repository structure

```text
mozart-dice-game-learning/
├── README.md
├── LICENSE
├── .gitignore
├── mozart_dice_game.ipynb
├── mozart_dice_game.py
└── requirements.txt
```

## Historical note

The musical dice game was published in 1792 by Nikolaus Simrock under Mozart’s name, after Mozart’s death. Its attribution to Mozart is not considered fully authenticated.

For that reason, this repository refers to it as the musical dice game attributed to Mozart.

## Audio attribution

The WAV fragments are external assets and are not included in this repository.

Obtain them from:

```text
Kevin Wayne, Mozart Musical Dice Game
https://nifty.stanford.edu/2023/wayne-musical-dice-game/
```

The repository license applies only to the original code in this project. It does not automatically apply to third-party WAV files, soundfonts, notation files, or historical musical material.

## License

The original code in this repository is released under the MIT License.

## Author

Sam Vaseghi

GitHub:

```text
https://github.com/vaseghisam
```
