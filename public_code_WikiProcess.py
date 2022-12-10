# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 14:44:39 2022

@author: MOSM
"""

## IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# %% SETTINGS

seuil_contribution=10
user_list = []
article_list = []
edit_list = []
edit_count = []
page_list = []
page_weight = []
page_group = []
path = os.getcwd().replace('\\','//')+"//" #Default : local path

subpathlist = ["Feminisme","LGBT","Racisme","TheorieWoke","CritiqueWoke","Groupe_Temoin"]

# %% IMPORT DATA FROM FILES
for subpath in subpathlist:
    fullpath = path+subpath+"//"
    for root, directories, file_list in os.walk(fullpath):
     	for file in file_list:
             #print('file detected')
             if file.endswith(".json"):
                 pathtif = (str(root)+str(file))
                 df = pd.read_json(pathtif,orient="top_editors")
                 page_list.append(df.loc[0,:].page)
                 page_weight.append(0)
                 page_group.append(subpathlist.index(subpath))
                 local_page_weight=0
                 for i in np.arange(0,len(df),1):
                     page_name = df.loc[i,:].page
                     user_add = df.loc[i,:].top_editors["username"]
                     local_count = df.loc[i,:].top_editors["count"]
                     local_page_weight+=local_count
                     if user_list.count(user_add)>0:
                         user_index = user_list.index(user_add)
                         article_list[user_index].append(page_name)
                         edit_list[user_index].append(local_count)
                         edit_count[user_index]+=local_count
                     else:
                        user_list.append(user_add)
                        article_list.append([page_name])
                        edit_list.append([local_count])
                        edit_count.append(local_count)
                 page_weight.append(local_page_weight)
             else:
                 print("Non-JSON file skipped")

# %% CREATE BAYESIAN PROBABILITIES
Intersection_per_group = np.zeros([len(subpathlist),len(subpathlist)])
Union_per_group = np.zeros([len(subpathlist),len(subpathlist)])
for user_index in np.arange(0,len(article_list),1):
    for i in np.arange(0,len(subpathlist),1):
        for j in np.arange(0,len(subpathlist),1):
            if i==j:
                Intersection_per_group[i,i]+=User_group[user_index,i]
                Union_per_group[i,i]+=User_group[user_index,i]
            else:
                if (j>i)and((User_group[user_index,i]>0)and(User_group[user_index,j]>0)):
                    Intersection_per_group[i,j]+=(User_group[user_index,i]+User_group[user_index,j])
                if (j>i)and((User_group[user_index,i]>0)or(User_group[user_index,j]>0)):
                    Union_per_group[i,j]+=(User_group[user_index,i]+User_group[user_index,j])

Normalized_Count_per_group = np.zeros([len(subpathlist),len(subpathlist)])
for i in np.arange(0,len(subpathlist),1):
    for j in np.arange(0,len(subpathlist),1):
        Normalized_Count_per_group[i,j]=Intersection_per_group[i,j]/Union_per_group[i,j]

# %% CREATE USER ANALYSIS
#define data
data = []
for i in np.arange(0,len(subpathlist),1):
    data.append(page_group.count(i))

#create heatmap
fig = px.imshow(np.round(Normalized_Count_per_group,3), labels=dict(x="Groupe d'origine", y="Probabilité de contribution", color="Probabilité"),
                x=subpathlist, y=subpathlist,text_auto=True)
fig.update_layout(title_text="Bayesian probability of cross-contribution", font_size=10)
fig.write_html('plot_edit_map.html', auto_open=False)

#create pie chart
fig = go.Figure(data=[go.Pie(labels=subpathlist, values=data)])
fig.update_layout(title_text="Article base distribution", font_size=10)
fig.write_html('plot_pie_groups.html', auto_open=False)

#create pie chart
top_contributors = []
top_edits = []
top = 30
for i in np.arange(0,top,1):
    top_contributors.append(user_list[np.argsort(edit_count)[-i]])
    top_edits.append(edit_count[np.argsort(edit_count)[-i]])
top_contributors.append("OTHERS")
top_edits.append(np.sum(edit_count)-np.sum(top_edits))
fig = go.Figure(data=[go.Pie(labels=top_contributors, values=top_edits)])
fig.update_layout(title_text="Top "+str(top)+" contributors", font_size=10)
fig.write_html('plot_top_contributors.html', auto_open=False)
