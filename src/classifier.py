import os
from typing import Optional

try:
    import numpy as np
    import cv2
    from tensorflow import keras
except Exception:  # ImportError or runtime error if tf not available
    np = None
    cv2 = None
    keras = None

IMG_SIZE = 224
MAX_SEQ_LENGTH = 20
NUM_FEATURES = 2048
CLASS_NAMES = [
    "basketball",
    "cooking",
    "gymnastics",
    "music",
    "soccer",
    "workout",
]

if keras is not None:
    def build_feature_extractor():
        feature_extractor = keras.applications.InceptionV3(
            weights="imagenet",
            include_top=False,
            pooling="avg",
            input_shape=(IMG_SIZE, IMG_SIZE, 3),
        )
        preprocess_input = keras.applications.inception_v3.preprocess_input
        inputs = keras.Input((IMG_SIZE, IMG_SIZE, 3))
        preprocessed = preprocess_input(inputs)
        outputs = feature_extractor(preprocessed)
        return keras.Model(inputs, outputs, name="feature_extractor")

    feature_extractor = build_feature_extractor()

    def build_sequence_model(num_classes: int):
        frame_input = keras.Input((MAX_SEQ_LENGTH, NUM_FEATURES))
        mask_input = keras.Input((MAX_SEQ_LENGTH,), dtype="bool")
        x = keras.layers.GRU(16, return_sequences=True)(frame_input, mask=mask_input)
        x = keras.layers.GRU(8)(x)
        x = keras.layers.Dropout(0.4)(x)
        x = keras.layers.Dense(8, activation="relu")(x)
        output = keras.layers.Dense(num_classes, activation="softmax")(x)
        return keras.Model([frame_input, mask_input], output)

    sequence_model = build_sequence_model(len(CLASS_NAMES))
    WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "tmp", "video_classifier.weights.h5")
    if os.path.exists(WEIGHTS_PATH):
        sequence_model.load_weights(WEIGHTS_PATH)
else:
    feature_extractor = None
    sequence_model = None

def crop_center_square(frame):
    y, x = frame.shape[0:2]
    min_dim = min(y, x)
    start_x = (x // 2) - (min_dim // 2)
    start_y = (y // 2) - (min_dim // 2)
    return frame[start_y : start_y + min_dim, start_x : start_x + min_dim]

def load_video(path: str, max_frames: int = 0, resize=(IMG_SIZE, IMG_SIZE)):
    if cv2 is None:
        return []
    cap = cv2.VideoCapture(path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = crop_center_square(frame)
        frame = cv2.resize(frame, resize)
        frame = frame[:, :, [2, 1, 0]]
        frames.append(frame)
        if max_frames and len(frames) == max_frames:
            break
    cap.release()
    return frames

def prepare_single_video(frames):
    if keras is None or np is None:
        return None, None
    frames = np.array(frames)
    frames = frames[None, ...]
    frame_mask = np.zeros(shape=(1, MAX_SEQ_LENGTH), dtype="bool")
    frame_features = np.zeros(shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")
    length = min(frames.shape[1], MAX_SEQ_LENGTH)
    for j in range(length):
        frame_features[0, j, :] = feature_extractor.predict(frames[:, j, :])
    frame_mask[0, :length] = 1
    return frame_features, frame_mask

def predict_video_tag(video_path: str) -> Optional[str]:
    if sequence_model is None:
        return None
    frames = load_video(video_path)
    if not frames:
        return None
    frame_features, frame_mask = prepare_single_video(frames)
    if frame_features is None:
        return None
    probabilities = sequence_model.predict([frame_features, frame_mask])[0]
    predicted_index = int(np.argmax(probabilities))
    return CLASS_NAMES[predicted_index]
