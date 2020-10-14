from pathlib import Path
import pandas as pd
import custom_modules as cm

dataset_path = Path("./data/dataset.csv")

dataset = cm.read_dataset(dataset_path)
dataset = cm.clean_dataset(dataset)
dataset = cm.one_hot_encode_dataset(dataset)
datasets = cm.split_dataset(dataset)
datasets = cm.get_features(datasets)

normalizer = cm.create_normalizer(datasets)
model = cm.create_model(normalizer)

history = model.fit(
    datasets["train_features"]["Horsepower"],
    datasets["train_labels"],
    epochs=100,
    verbose=0,
    validation_split=0.2,
)

hist = pd.DataFrame(history.history)
hist["epoch"] = history.epoch
