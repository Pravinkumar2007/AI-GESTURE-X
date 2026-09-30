# ============================================================
# GESTUREX - HANDWRITING CHARACTER MODEL TRAINER
# A-Z + 0-9
# ============================================================

import os
import numpy as np
import torch

from torchvision import datasets
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
import joblib


# ============================================================
# SETTINGS
# ============================================================

DATA_DIR = "handwriting_data"
MODEL_FILE = "handwriting_model.pkl"

# Number of samples used for faster CPU training.
# Increase later for better accuracy.
TRAIN_SAMPLES = 100000
TEST_SAMPLES = 20000

RANDOM_STATE = 42


# ============================================================
# EMNIST LABEL INFORMATION
# ============================================================

# We use the EMNIST ByClass dataset because it contains
# handwritten digits + uppercase/lowercase letters.
#
# We will keep:
#   0-9
#   A-Z
#
# EMNIST ByClass has 62 classes:
#
# 0-9  -> labels 0-9
# A-Z  -> labels 10-35
#
# lowercase letters are ignored.
# ============================================================


def convert_label(label):

    # --------------------------------------------------------
    # Digits
    # --------------------------------------------------------

    if 0 <= label <= 9:

        return str(label)

    # --------------------------------------------------------
    # Uppercase A-Z
    # --------------------------------------------------------

    if 10 <= label <= 35:

        return chr(
            ord("A") + label - 10
        )

    return None


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    print()
    print("=" * 60)
    print("GESTUREX HANDWRITING DATASET")
    print("=" * 60)

    print()
    print("Downloading/loading EMNIST...")
    print("This may take some time the first time.")
    print()

    train_dataset = datasets.EMNIST(
        root=DATA_DIR,
        split="byclass",
        train=True,
        download=True
    )

    test_dataset = datasets.EMNIST(
        root=DATA_DIR,
        split="byclass",
        train=False,
        download=True
    )

    print("Dataset loaded successfully.")

    return train_dataset, test_dataset


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data(dataset, max_samples):

    print()
    print("Preparing handwriting images...")

    images = []
    labels = []

    total = min(
        len(dataset),
        max_samples
    )

    # Random selection gives a better training sample.
    rng = np.random.default_rng(
        RANDOM_STATE
    )

    indexes = rng.choice(
        len(dataset),
        size=total,
        replace=False
    )

    skipped = 0

    for count, index in enumerate(indexes):

        image, label = dataset[index]

        label = int(label)

        character = convert_label(
            label
        )

        # Ignore lowercase letters.
        if character is None:

            skipped += 1
            continue

        # ----------------------------------------------------
        # Convert PIL image → NumPy
        # ----------------------------------------------------

        image = np.array(
            image,
            dtype=np.float32
        )

        # ----------------------------------------------------
        # EMNIST orientation correction
        # ----------------------------------------------------

        image = np.transpose(
            image
        )

        image = np.fliplr(
            image
        )

        # ----------------------------------------------------
        # Normalize
        # ----------------------------------------------------

        image = image / 255.0

        # ----------------------------------------------------
        # Flatten 28 × 28 → 784
        # ----------------------------------------------------

        image = image.reshape(
            -1
        )

        images.append(
            image
        )

        labels.append(
            character
        )

        if (count + 1) % 5000 == 0:

            print(
                f"Processed {count + 1}/{total} samples..."
            )

    X = np.array(
        images,
        dtype=np.float32
    )

    y = np.array(
        labels
    )

    print()
    print(
        f"Prepared samples: {len(X)}"
    )

    print(
        f"Skipped lowercase samples: {skipped}"
    )

    print(
        f"Feature size: {X.shape[1]}"
    )

    return X, y


# ============================================================
# TRAIN MODEL
# ============================================================

def train_model(X_train, y_train):

    print()
    print("=" * 60)
    print("TRAINING HANDWRITING CLASSIFIER")
    print("=" * 60)

    print()
    print("Training using CPU-friendly SGD classifier...")
    print()

    model = SGDClassifier(
        loss="log_loss",
        max_iter=30,
        tol=1e-3,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    print()
    print("Training completed!")

    return model


# ============================================================
# TEST MODEL
# ============================================================

def test_model(model, X_test, y_test):

    print()
    print("=" * 60)
    print("TESTING MODEL")
    print("=" * 60)

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print()
    print(
        f"Test Accuracy: {accuracy * 100:.2f}%"
    )

    return accuracy


# ============================================================
# SAVE MODEL
# ============================================================

def save_model(model):

    print()
    print("Saving trained model...")

    joblib.dump(
        model,
        MODEL_FILE
    )

    print()
    print(
        f"Model saved successfully:"
    )

    print(
        os.path.abspath(
            MODEL_FILE
        )
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("GESTUREX")
    print("AI HANDWRITING CHARACTER RECOGNITION")
    print("A-Z + 0-9")
    print("=" * 60)

    # --------------------------------------------------------
    # Load EMNIST
    # --------------------------------------------------------

    train_dataset, test_dataset = load_dataset()

    # --------------------------------------------------------
    # Prepare training data
    # --------------------------------------------------------

    X_train, y_train = prepare_data(
        train_dataset,
        TRAIN_SAMPLES
    )

    # --------------------------------------------------------
    # Prepare testing data
    # --------------------------------------------------------

    X_test, y_test = prepare_data(
        test_dataset,
        TEST_SAMPLES
    )

    # --------------------------------------------------------
    # Train
    # --------------------------------------------------------

    model = train_model(
        X_train,
        y_train
    )

    # --------------------------------------------------------
    # Accuracy
    # --------------------------------------------------------

    test_model(
        model,
        X_test,
        y_test
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_model(
        model
    )

    print()
    print("=" * 60)
    print("GESTUREX HANDWRITING MODEL READY")
    print("=" * 60)

    print()
    print("Next step:")
    print("Connect handwriting_model.pkl to GestureX.")
    print()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()