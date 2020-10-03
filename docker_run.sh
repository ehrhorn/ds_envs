#!/bin/bash
docker run -v $PWD:/code \
    -p 8501:8501 \
    ehrhorn/ds_envs:0.1 \
    streamlit run /code/main.py