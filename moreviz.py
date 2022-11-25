# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:50:40 2022

@author: mengy
"""
import pandas as pd
from folium.plugins import HeatMap
import folium as folium
import streamlit.components.v1 as components
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
#============================================================feature importance
# m = folium.Map([lat, lon], tiles='cartodbpositron', zoom_start=9)
# HeatMap(long_staydf).add_to(m)
# components.html(m._repr_html_(), width=1400, height=1000)

pickled_model = pickle.load(open('linear.pkl', 'rb'))
# print(pickled_model.coef_)
coeff = pickled_model.coef_.tolist()
X = ['age_group', 'apr_severity_of_illness_code', 'cdc_2018_overall_svi',
       'sum_countunique_rndrng_npi_physician_other_providers', 'covid_hosp',
       'long_stay', 'gender_M', 'race_Multi-racial', 'race_Other Race',
       'race_White', 'covid_True', 'ethnicity_Not Span/Hispanic',
       'ethnicity_Spanish/Hispanic', 'ethnicity_Unknown',
       'type_of_admission_Trauma', 'type_of_admission_Urgent',
       'payment_typology_1_Federal/State/Local/VA',
       'payment_typology_1_Medicaid', 'payment_typology_1_Medicare',
       'patient_disposition_Cancer Center or Children\'s Hospital',
       'patient_disposition_Court/Law Enforcement',
       'patient_disposition_Critical Access Hospital',
       'patient_disposition_Expired',
       'patient_disposition_Facility w/ Custodial/Supportive Care',
       'patient_disposition_Home or Self Care',
       'patient_disposition_Home w/ Home Health Services',
       'patient_disposition_Hospice - Home',
       'patient_disposition_Hospice - Medical Facility',
       'patient_disposition_Inpatient Rehabilitation Facility',
       'patient_disposition_Left Against Medical Advice',
       'patient_disposition_Medicaid Cert Nursing Facility',
       'patient_disposition_Medicare Cert Long Term Care Hospital',
       'patient_disposition_Psychiatric Hospital or Unit of Hosp',
       'patient_disposition_Short-term Hospital',
       'patient_disposition_Skilled Nursing Home', 'apr_drg_code_165',
       'apr_drg_code_166', 'apr_drg_code_167', 'apr_drg_code_169',
       'apr_drg_code_171', 'apr_drg_code_173', 'apr_drg_code_175',
       'apr_drg_code_180', 'apr_drg_code_191', 'apr_drg_code_197',
       'apr_drg_code_24', 'apr_drg_code_26', 'apr_drg_code_305',
       'apr_drg_code_309', 'apr_drg_code_310', 'apr_drg_code_312',
       'apr_drg_code_313', 'apr_drg_code_314', 'apr_drg_code_316',
       'apr_drg_code_317', 'apr_drg_code_320', 'apr_drg_code_321',
       'apr_drg_code_344', 'apr_drg_code_351', 'apr_drg_code_361',
       'apr_drg_code_364', 'apr_drg_code_380', 'apr_drg_code_4',
       'apr_drg_code_405', 'apr_drg_code_420', 'apr_drg_code_424',
       'apr_drg_code_440', 'apr_drg_code_444', 'apr_drg_code_447',
       'apr_drg_code_468', 'apr_drg_code_48', 'apr_drg_code_5',
       'apr_drg_code_6', 'apr_drg_code_710', 'apr_drg_code_73',
       'apr_drg_code_82', 'apr_drg_code_890', 'apr_drg_code_892',
       'apr_drg_code_894', 'apr_drg_code_950', 'apr_drg_code_951',
       'apr_drg_code_952', 'apr_mdc_code_10', 'apr_mdc_code_11',
       'apr_mdc_code_18', 'apr_mdc_code_2', 'apr_mdc_code_24',
       'apr_mdc_code_5', 'apr_mdc_code_8', 'apr_mdc_code_9']

feat_dict= {}
for col, val in sorted(zip(X, coeff),key=lambda x:x[1],reverse=True):
  feat_dict[col]=val
  
feat_df = pd.DataFrame({'Feature':feat_dict.keys(),'Importance':feat_dict.values()})
feat_df_pos = feat_df.loc[feat_df['Importance'] > 0,:].sort_values("Importance", ascending = False)
feat_df_neg = feat_df.loc[feat_df['Importance'] < 0,:].sort_values("Importance", ascending = False)

featdf_postop = feat_df_pos.head(10)
featdf_negtop = feat_df_neg.tail(10)

feat_dftop = pd.concat([featdf_postop,featdf_negtop],ignore_index=True)

values = feat_dftop.Importance    
idx = feat_dftop.Feature
fig = plt.figure(figsize=(10,8))
clrs = ['green' if (x < max(values)) else 'red' for x in values ]
sns.barplot(y=idx,x=values,palette=clrs).set(title='Important features to predict LOS')
plt.show()

# st.pyplot(fig)



#====================word frequency bubble chart
import numpy as np
#ref https://matplotlib.org/3.5.0/gallery/misc/packed_bubbles.html
class BubbleChart:
    def __init__(self, area, bubble_spacing=0):
        """
        Setup for bubble collapse.

        Parameters
        ----------
        area : array-like
            Area of the bubbles.
        bubble_spacing : float, default: 0
            Minimal spacing between bubbles after collapsing.

        Notes
        -----
        If "area" is sorted, the results might look weird.
        """
        area = np.asarray(area)
        r = np.sqrt(area / np.pi)

        self.bubble_spacing = bubble_spacing
        self.bubbles = np.ones((len(area), 4))
        self.bubbles[:, 2] = r
        self.bubbles[:, 3] = area
        self.maxstep = 2 * self.bubbles[:, 2].max() + self.bubble_spacing
        self.step_dist = self.maxstep / 2

        # calculate initial grid layout for bubbles
        length = np.ceil(np.sqrt(len(self.bubbles)))
        grid = np.arange(length) * self.maxstep
        gx, gy = np.meshgrid(grid, grid)
        self.bubbles[:, 0] = gx.flatten()[:len(self.bubbles)]
        self.bubbles[:, 1] = gy.flatten()[:len(self.bubbles)]

        self.com = self.center_of_mass()

    def center_of_mass(self):
        return np.average(
            self.bubbles[:, :2], axis=0, weights=self.bubbles[:, 3]
        )

    def center_distance(self, bubble, bubbles):
        return np.hypot(bubble[0] - bubbles[:, 0],
                        bubble[1] - bubbles[:, 1])

    def outline_distance(self, bubble, bubbles):
        center_distance = self.center_distance(bubble, bubbles)
        return center_distance - bubble[2] - \
            bubbles[:, 2] - self.bubble_spacing

    def check_collisions(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return len(distance[distance < 0])

    def collides_with(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        idx_min = np.argmin(distance)
        return idx_min if type(idx_min) == np.ndarray else [idx_min]

    def collapse(self, n_iterations=50):
        """
        Move bubbles to the center of mass.

        Parameters
        ----------
        n_iterations : int, default: 50
            Number of moves to perform.
        """
        for _i in range(n_iterations):
            moves = 0
            for i in range(len(self.bubbles)):
                rest_bub = np.delete(self.bubbles, i, 0)
                # try to move directly towards the center of mass
                # direction vector from bubble to the center of mass
                dir_vec = self.com - self.bubbles[i, :2]

                # shorten direction vector to have length of 1
                dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))

                # calculate new bubble position
                new_point = self.bubbles[i, :2] + dir_vec * self.step_dist
                new_bubble = np.append(new_point, self.bubbles[i, 2:4])

                # check whether new bubble collides with other bubbles
                if not self.check_collisions(new_bubble, rest_bub):
                    self.bubbles[i, :] = new_bubble
                    self.com = self.center_of_mass()
                    moves += 1
                else:
                    # try to move around a bubble that you collide with
                    # find colliding bubble
                    for colliding in self.collides_with(new_bubble, rest_bub):
                        # calculate direction vector
                        dir_vec = rest_bub[colliding, :2] - self.bubbles[i, :2]
                        dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                        # calculate orthogonal vector
                        orth = np.array([dir_vec[1], -dir_vec[0]])
                        # test which direction to go
                        new_point1 = (self.bubbles[i, :2] + orth *
                                      self.step_dist)
                        new_point2 = (self.bubbles[i, :2] - orth *
                                      self.step_dist)
                        dist1 = self.center_distance(
                            self.com, np.array([new_point1]))
                        dist2 = self.center_distance(
                            self.com, np.array([new_point2]))
                        new_point = new_point1 if dist1 < dist2 else new_point2
                        new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                        if not self.check_collisions(new_bubble, rest_bub):
                            self.bubbles[i, :] = new_bubble
                            self.com = self.center_of_mass()

            if moves / len(self.bubbles) < 0.1:
                self.step_dist = self.step_dist / 2

    def plot(self, ax, labels, colors):
        """
        Draw the bubble plot.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
        labels : list
            Labels of the bubbles.
        colors : list
            Colors of the bubbles.
        """
        for i in range(len(self.bubbles)):
            circ = plt.Circle(
                self.bubbles[i, :2], self.bubbles[i, 2], color=colors[i])
            ax.add_patch(circ)
            ax.text(*self.bubbles[i, :2], labels[i],
                    horizontalalignment='center', verticalalignment='center')

overall = [('services', 33062), ('cms', 28732), ('patients', 22148), ('health', 19614), ('care', 18837), ('medicare', 17899), ('access', 16054), ('cuts', 15917), ('management', 15208), ('therapy', 13823)]

adjs = [('behavioral', 8567), ('physical', 7607), ('mental', 7132), ('new', 5060), ('patient', 4928), ('underserved', 4749), ('additional', 4053), ('remote', 3828), ('digital', 3632), ('rural', 3571)]

nouns = [('services', 32921), ('patients', 22113), ('health', 19471), ('care', 18588), ('management', 15206), ('therapy', 13821), ('access', 13364), ('cuts', 13313), ('codes', 13282), ('psychologists', 10406)]

verbs = [('proposed', 12374), ('urge', 6682), ('provided', 6444), ('ensure', 5038), ('allow', 4672), ('support', 4426), ('ask', 3921), ('appreciate', 3022), ('recognize', 2741), ('underutilized', 2739)]

##overall 
word_dict = {}
colors = ['#5A69AF', '#579E65', '#F9C784', '#FC944A',
              '#F24C00', '#00B825', '#FC944A', '#EF4026',
              'goldenrod','green', '#F9C784', '#FC944A',
              'coral']
keys = [i[0] for i in overall]
values = [i[1]/18837 for i in overall]
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






#========================spyder chart
# import plotly.graph_objects as go
# df = pd.read_pickle('data7_0_1')

# categories = df['facility_id'].tolist()
# categories = [i.split(".")[0] for i in categories]
# df['facility_id'] = categories

# categories = df['facility_id'].drop_duplicates().sort_values().tolist()[:10]

# #first trace: avg los
# avgLos = df.groupby(['facility_id'])['length_of_stay'].agg('mean').to_frame('avgLos').reset_index()

# #second trace: %long stay
# countdf = df.groupby(['facility_id'])['length_of_stay'].agg('count').to_frame('count').reset_index()
# longdf = df.groupby(['facility_id'])['long_stay'].agg('sum').to_frame('long').reset_index()
# aggdf = pd.merge(countdf, longdf, on='facility_id', how='outer')
# aggdf['percentage_long_stay'] = aggdf["long"]/aggdf["count"] *100

# #third trace: totalcost
# avgTC = df.groupby(['facility_id'])['total_costs'].agg('mean').to_frame('avgTC').reset_index()

# fig = go.Figure()

# fig.add_trace(go.Scatterpolar(
#       r=avgLos['avgLos'].tolist()[:10],
#       theta=categories,
#       fill='toself',
#       name='AvgLOS'
# ))

# fig.add_trace(go.Scatterpolar(
#       r=aggdf['percentage_long_stay'].tolist()[:10],
#       theta=categories,
#       fill='toself',
#       name='%LongLOS'
# ))

# fig.add_trace(go.Scatterpolar(
#       r=[i/1000 for i in avgTC['avgTC'].tolist()[:10]],
#       theta=categories,
#       fill='toself',
#       name='AvgTotalCost'
# ))
# fig.update_layout(
#   polar=dict(
#     radialaxis=dict(
#       visible=True,
#       range=[0, 55]
#     )),
#   showlegend=True
# )

# fig.show()




# import plotly.express as px
# import pandas as pd

# categories = ['Rolling Resistance','Comfort','Noise',
#             'Wear', 'Traction','Handling']
# fig = go.Figure()

# #product 1
# fig.add_trace(go.Scatterpolar(
#       r=[105, 100, 100, 110, 95, 100],
#       theta=categories,
#       fill='toself',
#       name='Product A'
# ))

# #product 2
# fig.add_trace(go.Scatterpolar(
#       r=[95, 100, 100, 100, 105, 100],
#       theta=categories,
#       fill='toself',
#       name='Product B'
# ))

# #product 3
# fig.add_trace(go.Scatterpolar(
#       r=[100, 100, 95, 100, 100, 110],
#       theta=categories,
#       fill='toself',
#       name='Product B'
# ))

# #customization of chart
# fig.update_layout(
#   polar=dict(
#     radialaxis=dict(
#       visible=True,
#       range=[90, 115]
#     )),
#   showlegend=False
# )


# fig.show()

# st.pyplot(fig)
