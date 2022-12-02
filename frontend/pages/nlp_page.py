from frontend.components.BubbleChart import BubbleChart
import matplotlib.pyplot as plt
import streamlit as st
import random
from wordcloud import WordCloud
from wordcloud import STOPWORDS

# ref https://matplotlib.org/3.5.0/g


def create_nlp_page():
    show_option = st.selectbox(
        label="",
        options=("keywords", "key phrases")
    )
    keywords = [('services', 33062), ('cms', 28732), ('patients', 22148), ('health', 19614), ('care', 18837),
                ('medicare', 17899), ('access', 16054), ('cuts', 15917), ('management', 15208), ('therapy', 13823),
                ('codes', 13292), ('proposed', 12376), ('psychologists', 10412), ('reimbursement', 9869),
                ('patient', 9028), ('behavioral', 8573), ('supervision', 8560), ('training', 8245), ('support', 8071),
                ('treatment', 7927)]

    key_phrases = [('psychological services medicare', 0.6466),
                   ('psychotherapeutic services medicare', 0.637),
                   ('services cms medicare', 0.6348),
                   ('cms proposed medicare', 0.6247),
                   ('medicare requests cms', 0.6243),
                   ('utilize cms medicare', 0.6241),
                   ('medicare cms regarding', 0.6137),
                   ('medicare program cms', 0.6135),
                   ('cms behavioral health', 0.6134),
                   ('cms strengthen medicare', 0.6116),
                   ('outpatient services cms', 0.6098),
                   ('provide behavioral healthcare', 0.6083),
                   ('cms understanding medicare', 0.6074),
                   ('behavioral healthcare services', 0.6066),
                   ('cms medicare program', 0.6066),
                   ('cms beneficiaries outpatient', 0.606),
                   ('integrated behavioral healthcare', 0.6057),
                   ('treatment cms policies', 0.6054),
                   ('medicare clients cms', 0.6049),
                   ('cms ensure medicare', 0.6036)]
    key_phrases_dict = {}
    for t in key_phrases:
        key_phrases_dict[t[0]] = t[1]

    if show_option == "keywords":
        draw_bubble_chart(keywords)
    elif show_option == "key phrases":
        cloud = WordCloud(max_font_size=50, max_words=100, background_color="white")\
            .generate_from_frequencies(key_phrases_dict)
        fig, ax = plt.subplots()
        plt.title("All Comments - Wordcloud")
        plt.imshow(cloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)


def draw_bubble_chart(frequencies):
    word_dict = {}
    colors = ["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)]) for j in frequencies]
    keys = [i[0] for i in frequencies]
    values = [i[1] / 18837 for i in frequencies]
    word_dict['word'] = keys
    word_dict['frequency'] = values
    word_dict['color'] = colors[:len(keys)]

    bubble_chart = BubbleChart(area=word_dict['frequency'],
                               bubble_spacing=0.1)
    bubble_chart.collapse()

    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    fig.set_size_inches(9, 13, forward=True)
    bubble_chart.plot(
        ax, word_dict['word'], word_dict['color'])
    ax.axis("off")
    ax.relim()
    ax.autoscale_view()
    plt.show()

    st.pyplot(fig)
