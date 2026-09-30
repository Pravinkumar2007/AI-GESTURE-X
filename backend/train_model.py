import os
import numpy as np

from sklearn.neighbors import KNeighborsClassifier
import joblib


# ==========================================
# SETTINGS
# ==========================================

DATASET_DIR = "dataset"
MODEL_DIR = "models"

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "air_writing_model.pkl"
)

POINT_COUNT = 50


# ==========================================
# CREATE MODEL FOLDER
# ==========================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ==========================================
# NORMALIZE POINTS
# ==========================================

def normalize_points(points):

    if len(points) < 2:
        return None

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    min_x = min(xs)
    max_x = max(xs)

    min_y = min(ys)
    max_y = max(ys)

    width = max_x - min_x
    height = max_y - min_y

    if width == 0:
        width = 1

    if height == 0:
        height = 1

    normalized = []

    for x, y in points:

        nx = (x - min_x) / width
        ny = (y - min_y) / height

        normalized.append(
            (nx, ny)
        )

    return normalized


# ==========================================
# RESAMPLE POINTS
# ==========================================

def resample_points(points):

    if len(points) < 2:
        return None

    indexes = np.linspace(
        0,
        len(points) - 1,
        POINT_COUNT
    ).astype(int)

    result = []

    for index in indexes:

        result.append(
            points[index]
        )

    return result


# ==========================================
# CREATE FEATURES
# ==========================================

def create_features(points):

    normalized = normalize_points(points)

    if normalized is None:
        return None

    resampled = resample_points(
        normalized
    )

    if resampled is None:
        return None

    features = []

    for x, y in resampled:

        features.append(x)
        features.append(y)

    return features


# ==========================================
# LOAD DATASET
# ==========================================

X = []
y = []


if not os.path.exists(DATASET_DIR):

    print(
        "ERROR: dataset folder not found."
    )

    print(
        "Run collect_data.py first."
    )

    exit()


# ==========================================
# READ LETTER FOLDERS
# ==========================================

letters = sorted(
    os.listdir(DATASET_DIR)
)


for letter in letters:

    letter_folder = os.path.join(
        DATASET_DIR,
        letter
    )

    if not os.path.isdir(
        letter_folder
    ):
        continue


    print(
        "Loading:",
        letter
    )


    files = os.listdir(
        letter_folder
    )


    for filename in files:

        if not filename.endswith(".txt"):
            continue


        filepath = os.path.join(
            letter_folder,
            filename
        )


        points = []


        try:

            with open(
                filepath,
                "r"
            ) as file:

                for line in file:

                    line = line.strip()

                    if not line:
                        continue

                    x, y_value = line.split(",")

                    points.append(
                        (
                            float(x),
                            float(y_value)
                        )
                    )


        except Exception as error:

            print(
                "Could not read:",
                filepath
            )

            print(
                error
            )

            continue


        features = create_features(
            points
        )


        if features is None:
            continue


        X.append(features)

        y.append(letter)


# ==========================================
# CHECK DATA
# ==========================================

print()
print("------------------------------------------")
print("DATASET INFORMATION")
print("------------------------------------------")

print(
    "Samples:",
    len(X)
)

print(
    "Letters:",
    sorted(set(y))
)

print("------------------------------------------")


if len(X) == 0:

    print(
        "ERROR: No training data found."
    )

    print(
        "Collect some letters first."
    )

    exit()


# ==========================================
# CONVERT TO NUMPY
# ==========================================

X = np.array(X)

y = np.array(y)


# ==========================================
# CREATE CLASSIFIER
# ==========================================

model = KNeighborsClassifier(
    n_neighbors=3
)


# ==========================================
# TRAIN
# ==========================================

print()
print("Training model...")

model.fit(
    X,
    y
)


# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    MODEL_FILE
)


# ==========================================
# DONE
# ==========================================

print()
print("------------------------------------------")
print("MODEL TRAINING COMPLETE")
print("------------------------------------------")

print(
    "Model saved to:"
)

print(
    MODEL_FILE
)

print()
print(
    "Training samples:",
    len(X)
)

print(
    "Letters trained:",
    len(set(y))
)

print("------------------------------------------")