# viz.py
#    
# WordTM: Show a wordcloud for a precribed range of Scripture
#
# Copyright (C) 2022-2023 WordTM Project
# Author: Johnny Cheng <drjohnnycheng@gmail.com>
# Updated: 23 Jan. 2024
#
# URL:  nil
# For license information, see LICENSE.TXT

import numpy as np
import pandas as pd
from importlib_resources import files
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image

from wordtm import util


def plot_cloud(wordcloud):
    """Plot the prepared wordcloud"""
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud) 
    plt.axis("off");


def show_wordcloud(docs image='heart.jpg', mask=None):
    """Prepare and show a wordcloud"""
    if image:
        img_file = files('wordtm.images').joinpath(image)
        mask = np.array(Image.open(img_file))

    if isinstance(docs, pd.DataFrame):
        docs = ' '.join(list(docs.text))
    elif isintance(docs, list) or isinstance(docs, np.ndarray):
        docs = ' ' .join(docs)

    wordcloud = WordCloud(background_color='black', colormap='Set2', mask=mask) \
                    .generate(docs)

    plot_cloud(wordcloud)


def chi_wordcloud(docs, image='heart.jpg', mask=None):
    """Prepare and show a Chinese wordcloud"""
    util.set_lang('chi')
    diction = util.get_diction(docs)

    if image:
        img_file = files('wordtm.images').joinpath(image)
        mask = np.array(Image.open(img_file))

    font = 'msyh.ttc'
    wordcloud = WordCloud(background_color='black', colormap='Set2', 
                          mask=mask, font_path=font) \
                    .generate_from_frequencies(frequencies=diction)

    plot_cloud(wordcloud)
