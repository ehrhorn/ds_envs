from pathlib import Path
import pickle
import custom_modules as cm
import streamlit as st
import tensorflow as tf

versions_path = Path("./models")
versions = [folder for folder in versions_path.iterdir() if folder.is_dir()]
chosen_version = st.sidebar.selectbox("Version", versions, format_func=lambda x: x.name)

model = tf.keras.models.load_model(chosen_version.joinpath("my_model"))
with open(chosen_version.joinpath("datasets.pkl"), "rb") as f:
    datasets = pickle.load(f)
with open(chosen_version.joinpath("raw_dataset.pkl"), "rb") as f:
    raw_dataset = pickle.load(f)
with open(chosen_version.joinpath("hist.pkl"), "rb") as f:
    history = pickle.load(f)

x = tf.linspace(0.0, 250, 251)
y = model.predict(x)
test_predictions = model.predict(datasets["test_features"]["Horsepower"]).flatten()

fig = cm.plot_loss(history)
st.pyplot(fig)
fig = cm.plot_distributions(raw_dataset)
st.pyplot(fig)
fig = cm.plot_horsepower(datasets, x, y)
st.pyplot(fig)
fig = cm.plot_errors(datasets, test_predictions)
st.pyplot(fig)
fig = cm.plot_residuals(test_predictions, datasets["test_labels"])
st.pyplot(fig)
