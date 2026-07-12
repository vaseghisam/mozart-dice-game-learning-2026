# Mozart Dice Game Learning

A Python and Jupyter implementation of the musical dice game attributed to Wolfgang Amadeus Mozart, extended with two small probabilistic learning models that generate complete waltzes from precomposed WAV fragments.

The project compares three generative procedures:

1. a historical dice-based generator,
2. a learned position model,
3. a learned transition model.

Each procedure selects one musical fragment for every position in a sixteen-measure minuet and a sixteen-measure trio. The selected WAV fragments are then concatenated into a complete audio file.

This is an educational model of algorithmic and generative composition. It is not intended to reproduce Mozart’s compositional intelligence or to serve as a full machine-learning system for music generation.

---

## Concept

The musical dice game represents a piece as a sequence of positions. At every position, the system chooses one measure from a finite set of admissible alternatives.

A complete minuet can be written schematically as

```text
W = (m₀,j₀, m₁,j₁, ..., m₁₅,j₁₅)
```

where each position has its own collection of possible measures.

The historical generator uses dice:

* two six-sided dice for each minuet position,
* one six-sided die for each trio position.

The two learned models estimate probability distributions from many generated examples.

The position model learns

```text
P(variant | part, position)
```

The transition model learns

```text
P(current variant | previous choice, current position)
```

The code therefore illustrates the distinction between:

```text
designed rule + random sampling
```

and

```text
learned probability distribution + random sampling
```

---

## Repository Contents

A recommended repository structure is:

```text
mozart-dice-game-learning/
├── README.md
├── LICENSE
├── .gitignore
├── mozart_dice_game.ipynb
├── mozart_dice_game.py
└── requirements.txt
```

The WAV files are not included in this repository.

---

## Requirements

The code requires:

* Python 3.9 or later
* Jupyter Notebook or JupyterLab
* `pydub`
* `ffmpeg`

Install the Python dependency with:

```bash
pip install pydub
```

On macOS, install `ffmpeg` with Homebrew:

```bash
brew install ffmpeg
```

On Ubuntu or Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

On Windows, install `ffmpeg` separately and ensure that it is available on the system path.

---

## WAV Fragment Collection

The code expects a folder containing the precomposed Mozart dice-game WAV fragments for one instrument.

A compatible WAV collection can be obtained from Kevin Wayne’s Mozart Musical Dice Game assignment:

```text
https://nifty.stanford.edu/2023/wayne-musical-dice-game/
```

Download the archive named:

```text
mozart.zip
```

After extraction, choose one instrument folder, such as the piano folder.

The code assumes filenames following this convention:

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

The position numbers therefore run from `0` to `15`.

The minuet variants correspond to dice sums from `2` to `12`.

The trio variants correspond to die values from `1` to `6`.

---

## Audio Folder Configuration

Open the notebook or Python script and edit this line:

```python
audio_directory = Path("/PUT/YOUR/FOLDER/PATH/HERE")
```

For example, on macOS:

```python
audio_directory = Path("/Users/yourname/Downloads/mozart/piano")
```

On Windows:

```python
audio_directory = Path(r"C:\Users\yourname\Downloads\mozart\piano")
```

On Linux:

```python
audio_directory = Path("/home/yourname/Downloads/mozart/piano")
```

The selected folder should directly contain files such as:

```text
minuet0-2.wav
minuet0-7.wav
trio0-1.wav
trio15-6.wav
```

Do not point the code to the parent directory if the WAV files are located inside a separate instrument subfolder.

---

## Running the Notebook

Start Jupyter from the repository folder:

```bash
jupyter notebook
```

Open:

```text
mozart_dice_game.ipynb
```

Set the correct `audio_directory`, then run the main code cell.

The program will:

1. verify the WAV directory,
2. inspect the filename convention,
3. generate one historical dice waltz,
4. create a synthetic training dataset,
5. train the position model,
6. train the transition model,
7. generate one waltz from each learned model,
8. concatenate the selected WAV fragments,
9. export three complete audio files.

---

## Generated Files

The code creates:

```text
historical_dice_waltz.wav
learned_position_model_waltz.wav
learned_transition_model_waltz.wav
```

These files are saved in the current working directory of the notebook or script.

In Jupyter, the current working directory can be checked with:

```python
from pathlib import Path

print(Path.cwd())
```

---

## The Three Generators

### 1. Historical Dice Generator

The historical generator uses the direct dice rule.

For every minuet position, it rolls two six-sided dice and uses their sum to choose a fragment.

For every trio position, it rolls one six-sided die.

The two-dice distribution is not uniform. A sum of `7` is more probable than a sum of `2` or `12`.

The probabilities are:

```text
sum  2: 1/36
sum  3: 2/36
sum  4: 3/36
sum  5: 4/36
sum  6: 5/36
sum  7: 6/36
sum  8: 5/36
sum  9: 4/36
sum 10: 3/36
sum 11: 2/36
sum 12: 1/36
```

### 2. Learned Position Model

The position model estimates:

```text
P(variant | part, position)
```

It learns how frequently each variant occurs at each position in the generated training data.

Because the training examples are produced by the historical dice process, the learned model gradually reconstructs the original dice probabilities.

This model does not use the preceding musical fragment as context.

### 3. Learned Transition Model

The transition model estimates:

```text
P(current variant | previous choice, current position)
```

It has a limited one-step memory and resembles a simple Markov model.

When trained only on independently generated dice examples, it should not discover strong musical dependencies, because the historical sampling process itself does not condition each choice on the preceding choice.

The model becomes more meaningful if it is later trained on curated examples, listener ratings, or musical features.

---

## Important Limitation

The learning models in this repository are deliberately small and transparent.

They do not learn Mozart’s compositional style from raw audio.

They do not:

* analyze harmony,
* infer melodic structure,
* generate new notes,
* generate new measures,
* learn long-range musical form,
* use neural networks,
* use transformers,
* optimize a differentiable loss function.

They only learn probability distributions over existing fragment labels.

The musical intelligence remains largely in the original fragment table. The models learn how to select among those fragments.

This limitation is central to the project rather than accidental. It makes the difference between rule-based generation and learned generation easy to inspect.

---

## Why the Transition Model May Sound Similar

The historical dice process selects fragments independently once the position is fixed.

Therefore, training a transition model on examples generated only from that process does not introduce genuinely new musical knowledge. It mainly estimates statistical relations that arise from finite sampling.

A stronger future version could train on:

* human-selected waltzes,
* listener preference scores,
* cadence labels,
* pitch contours,
* rhythmic features,
* harmonic functions,
* MIDI representations,
* MusicXML representations.

Such a model could learn preferences that are not already contained in the original dice rule.

---

## Reproducibility

The code uses:

```python
random.seed(42)
```

This makes the generated results reproducible.

Change the seed to obtain a different sequence:

```python
random.seed(123)
```

Remove the seed entirely to obtain a different result on every run.

---

## Changing Instruments

The downloaded WAV archive may contain separate folders for instruments such as:

* piano,
* clarinet,
* flute and harp,
* mbira.

To change the instrument, point `audio_directory` to another instrument folder:

```python
audio_directory = Path("/path/to/mozart/clarinet")
```

The filenames must follow the same convention.

---

## Common Errors

### `FileNotFoundError`

Example:

```text
Missing audio file: .../minuet0-7.wav
```

Possible causes:

* the path points to the wrong folder,
* the path points to the parent folder rather than the instrument folder,
* the WAV files use a different filename convention,
* the files were not fully extracted,
* the positions start at `1` rather than `0`.

Check the folder with:

```python
for path in sorted(audio_directory.glob("*.wav"))[:20]:
    print(path.name)
```

### `AudioSegment` cannot find ffmpeg

Install `ffmpeg` and restart the Jupyter kernel.

On macOS:

```bash
brew install ffmpeg
```

Then restart Jupyter.

### No output files are visible

Check the notebook working directory:

```python
from pathlib import Path

print(Path.cwd())
```

The generated WAV files are saved there unless another output path is specified.

### The notebook uses an old function definition

Jupyter keeps earlier definitions in memory.

After changing a function:

1. rerun the cell containing that function, or
2. restart the kernel and run all cells again.

---

## Historical and Attribution Note

The musical dice game commonly associated with Mozart was published in 1792 by Nikolaus Simrock under Mozart’s name, after Mozart’s death.

The attribution is not considered fully authenticated.

The project therefore uses formulations such as:

```text
the musical dice game attributed to Mozart
```

rather than treating Mozart’s authorship as certain.

---

## Audio and Source Attribution

The WAV fragments used by this project are external assets and are not included in this repository.

Users should obtain them from their original source:

```text
Kevin Wayne, “Mozart Musical Dice Game”
https://nifty.stanford.edu/2023/wayne-musical-dice-game/
```

According to the source documentation, the fragments were prepared from the published musical material using digital notation and audio tools.

The license of this repository applies only to the original Python code contained here. It does not automatically apply to:

* the historical musical material,
* third-party WAV files,
* soundfonts,
* notation files,
* external archives.

Consult the original source before redistributing those assets.

---

## Citation

When referring to this repository, cite it as:

```text
Sam Vaseghi, Mozart Dice Game Learning, GitHub repository.
```

After the repository is published, add its final URL:

```text
https://github.com/vaseghisam/mozart-dice-game-learning
```

---

## Possible Extensions

The project can be extended in several directions:

* train on human-rated generated waltzes,
* compare uniform and non-uniform sampling,
* extract rhythmic or melodic features,
* represent fragments as MIDI,
* train a feature-aware Markov model,
* use a recurrent neural network,
* use a small transformer,
* generate new measures rather than only selecting existing ones,
* compare different instrument renderings,
* visualize the learned probability distributions,
* measure similarity between generated outputs,
* build an interactive browser interface.

A particularly useful next step would be to assign each fragment a compact feature vector containing pitch contour, rhythmic density, cadence type, and ending note. A model could then learn transitions between musical properties rather than only between table indices.

---

## License

The original Python code in this repository is released under the MIT License.

See:

```text
LICENSE
```

for details.

---

## Author

Sam Vaseghi

Editor-in-Chief, The Quantastic Journal

GitHub:

```text
https://github.com/vaseghisam
```
