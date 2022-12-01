from frontend.components.BubbleChart import BubbleChart
import matplotlib.pyplot as plt
import streamlit as st
#ref https://matplotlib.org/3.5.0/g


def create_nlp_page():
    overall = [('services', 33062), ('cms', 28732), ('patients', 22148), ('health', 19614), ('care', 18837),
               ('medicare', 17899), ('access', 16054), ('cuts', 15917), ('management', 15208), ('therapy', 13823)]

    adjs = [('behavioral', 8567), ('physical', 7607), ('mental', 7132), ('new', 5060), ('patient', 4928),
            ('underserved', 4749), ('additional', 4053), ('remote', 3828), ('digital', 3632), ('rural', 3571)]

    nouns = [('services', 32921), ('patients', 22113), ('health', 19471), ('care', 18588), ('management', 15206),
             ('therapy', 13821), ('access', 13364), ('cuts', 13313), ('codes', 13282), ('psychologists', 10406)]

    verbs = [('proposed', 12374), ('urge', 6682), ('provided', 6444), ('ensure', 5038), ('allow', 4672),
             ('support', 4426), ('ask', 3921), ('appreciate', 3022), ('recognize', 2741), ('underutilized', 2739)]

    ##overall
    word_dict = {}
    colors = ['#5A69AF', '#579E65', '#F9C784', '#FC944A',
              '#F24C00', '#00B825', '#FC944A', '#EF4026',
              'goldenrod', 'green', '#F9C784', '#FC944A',
              'coral']
    keys = [i[0] for i in overall]
    values = [i[1] / 18837 for i in overall]
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