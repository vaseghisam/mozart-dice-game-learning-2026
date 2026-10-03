# ============================================================
# MOZART DICE GAME + TOY LEARNING MODEL + WAV EXPORT
# For existing local WAV files named like:
#     minuet0-2.wav, minuet0-3.wav, ...
#     trio0-1.wav, trio0-2.wav, ...
# ============================================================

import random
from pathlib import Path
from collections import defaultdict, Counter
from pydub import AudioSegment


# ============================================================
# 0. EDIT ONLY THIS PATH
# ============================================================

audio_directory = Path("/PUT/YOUR/FOLDER/PATH/HERE")
# Example:
# audio_directory = Path("/Users/YourName/Downloads/mozart/piano")


# ============================================================
# 1. Basic checks
# ============================================================

if not audio_directory.exists():
    raise FileNotFoundError(f"Audio folder does not exist: {audio_directory}")

wav_files = list(audio_directory.glob("*.wav"))

print("Using audio folder:", audio_directory)
print("Number of WAV files:", len(wav_files))
print("First 20 files:")
for p in sorted(wav_files)[:20]:
    print(" ", p.name)


# ============================================================
# 2. Configuration
# ============================================================

random.seed(42)

N_TRAINING_EXAMPLES = 20_000

OUTPUT_HISTORICAL = "historical_dice_waltz.wav"
OUTPUT_POSITION_MODEL = "learned_position_model_waltz.wav"
OUTPUT_TRANSITION_MODEL = "learned_transition_model_waltz.wav"


# ============================================================
# 3. Filename conversion
# ============================================================

def label_to_filename(label):
    """
    Convert symbolic labels into your WAV filenames.

    Internal label:
        M00_07

    Filename:
        minuet0-7.wav

    Internal label:
        T15_04

    Filename:
        trio15-4.wav
    """
    part = label[0]
    position = int(label[1:3])
    variant = int(label[4:6])

    if part == "M":
        return f"minuet{position}-{variant}.wav"

    if part == "T":
        return f"trio{position}-{variant}.wav"

    raise ValueError(f"Unknown label format: {label}")


def structured_waltz_to_labels(waltz):
    """
    Convert tuples into symbolic labels.

    ("M", 0, 7) becomes M00_07
    ("T", 15, 4) becomes T15_04
    """
    return [f"{part}{position:02d}_{variant:02d}" for part, position, variant in waltz]


# ============================================================
# 4. Dice utilities
# ============================================================

def roll_one_die():
    return random.randint(1, 6)


def roll_two_dice_sum():
    return random.randint(1, 6) + random.randint(1, 6)


# ============================================================
# 5. Historical dice generator
# ============================================================

def generate_historical_waltz():
    """
    Generate one symbolic waltz.

    Minuet:
        positions 0...15
        two dice, sums 2...12

    Trio:
        positions 0...15
        one die, values 1...6
    """
    waltz = []

    for position in range(16):
        dice_sum = roll_two_dice_sum()
        waltz.append(("M", position, dice_sum))

    for position in range(16):
        die_value = roll_one_die()
        waltz.append(("T", position, die_value))

    return structured_waltz_to_labels(waltz)


def generate_training_data(n_examples=20_000):
    """
    Generate symbolic training examples from the dice process.
    """
    dataset = []

    for _ in range(n_examples):
        waltz = []

        for position in range(16):
            dice_sum = roll_two_dice_sum()
            waltz.append(("M", position, dice_sum))

        for position in range(16):
            die_value = roll_one_die()
            waltz.append(("T", position, die_value))

        dataset.append(waltz)

    return dataset


# ============================================================
# 6. Learned position model
# ============================================================

def train_position_model(dataset):
    """
    Learn:

        P(variant | part, position)
    """
    counts = defaultdict(Counter)

    for waltz in dataset:
        for part, position, variant in waltz:
            counts[(part, position)][variant] += 1

    return counts


def sample_from_counter(counter):
    items = list(counter.keys())
    weights = list(counter.values())
    return random.choices(items, weights=weights, k=1)[0]


def generate_from_position_model(position_model):
    waltz = []

    for position in range(16):
        variant = sample_from_counter(position_model[("M", position)])
        waltz.append(("M", position, variant))

    for position in range(16):
        variant = sample_from_counter(position_model[("T", position)])
        waltz.append(("T", position, variant))

    return structured_waltz_to_labels(waltz)


# ============================================================
# 7. Learned transition model
# ============================================================

def train_transition_model(dataset):
    """
    Learn:

        P(current_variant | previous choice, current position)
    """
    transitions = defaultdict(Counter)

    for waltz in dataset:
        for previous, current in zip(waltz[:-1], waltz[1:]):
            prev_part, prev_position, prev_variant = previous
            curr_part, curr_position, curr_variant = current

            key = (
                prev_part,
                prev_position,
                prev_variant,
                curr_part,
                curr_position
            )

            transitions[key][curr_variant] += 1

    return transitions


def generate_from_transition_model(transition_model, position_model):
    waltz = []

    # First minuet measure
    first_variant = sample_from_counter(position_model[("M", 0)])
    waltz.append(("M", 0, first_variant))

    # Remaining minuet measures
    for position in range(1, 16):
        prev_part, prev_position, prev_variant = waltz[-1]
        key = (prev_part, prev_position, prev_variant, "M", position)

        if key in transition_model:
            variant = sample_from_counter(transition_model[key])
        else:
            variant = sample_from_counter(position_model[("M", position)])

        waltz.append(("M", position, variant))

    # Trio measures
    for position in range(16):
        prev_part, prev_position, prev_variant = waltz[-1]
        key = (prev_part, prev_position, prev_variant, "T", position)

        if key in transition_model:
            variant = sample_from_counter(transition_model[key])
        else:
            variant = sample_from_counter(position_model[("T", position)])

        waltz.append(("T", position, variant))

    return structured_waltz_to_labels(waltz)


# ============================================================
# 8. WAV export
# ============================================================

def export_waltz_to_wav(waltz_labels, audio_directory, output_path):
    """
    Concatenate selected WAV fragments into one output WAV file.
    """
    audio_directory = Path(audio_directory)
    output_path = Path(output_path)

    combined = AudioSegment.empty()
    missing_files = []

    for label in waltz_labels:
        filename = label_to_filename(label)
        wav_path = audio_directory / filename

        if not wav_path.exists():
            missing_files.append((label, filename, wav_path))
            continue

        combined += AudioSegment.from_wav(wav_path)

    if missing_files:
        print("\nMissing files:")
        for label, filename, wav_path in missing_files[:20]:
            print(f"{label} -> {filename} -> {wav_path}")
        raise FileNotFoundError(
            f"{len(missing_files)} required WAV files were missing. "
            "Check the folder path and filename convention."
        )

    combined.export(output_path, format="wav")
    print(f"Saved: {output_path.resolve()}")

    return output_path


def print_waltz(title, labels):
    print("\n" + title)
    print("=" * len(title))

    print("\nMinuet:")
    print(" ".join(labels[:16]))

    print("\nTrio:")
    print(" ".join(labels[16:]))


# ============================================================
# 9. Sanity checks
# ============================================================

required_examples = [
    "minuet0-2.wav",
    "minuet0-7.wav",
    "minuet15-12.wav",
    "trio0-1.wav",
    "trio15-6.wav",
]

print("\nChecking expected filename convention:")
for filename in required_examples:
    path = audio_directory / filename
    print(f"{filename}: {path.exists()}")

if not (audio_directory / "minuet0-2.wav").exists():
    raise FileNotFoundError(
        "The code expects filenames like minuet0-2.wav. "
        "If your files use another convention, tell me the exact first 20 filenames."
    )


# ============================================================
# 10. Run full experiment
# ============================================================

print("\nGenerating historical dice waltz...")
historical_waltz = generate_historical_waltz()
print_waltz("Historical dice generator", historical_waltz)

export_waltz_to_wav(
    historical_waltz,
    audio_directory=audio_directory,
    output_path=OUTPUT_HISTORICAL
)


print("\nGenerating training data...")
dataset = generate_training_data(n_examples=N_TRAINING_EXAMPLES)

print("Training position model...")
position_model = train_position_model(dataset)

print("Training transition model...")
transition_model = train_transition_model(dataset)


print("\nGenerating learned position-model waltz...")
learned_position_waltz = generate_from_position_model(position_model)
print_waltz("Learned position model", learned_position_waltz)

export_waltz_to_wav(
    learned_position_waltz,
    audio_directory=audio_directory,
    output_path=OUTPUT_POSITION_MODEL
)


print("\nGenerating learned transition-model waltz...")
learned_transition_waltz = generate_from_transition_model(
    transition_model,
    position_model
)

print_waltz("Learned transition model", learned_transition_waltz)

export_waltz_to_wav(
    learned_transition_waltz,
    audio_directory=audio_directory,
    output_path=OUTPUT_TRANSITION_MODEL
)


# ============================================================
# 11. Show learned dice distribution
# ============================================================

print("\nLearned distribution for Minuet position 0")
print("==========================================")

counts = position_model[("M", 0)]
total = sum(counts.values())

for dice_sum in range(2, 13):
    probability = counts[dice_sum] / total
    print(f"sum {dice_sum:2d}: {probability:.4f}")


print("\nFinished.")
print("Generated files:")
print(f"- {Path(OUTPUT_HISTORICAL).resolve()}")
print(f"- {Path(OUTPUT_POSITION_MODEL).resolve()}")
print(f"- {Path(OUTPUT_TRANSITION_MODEL).resolve()}")
