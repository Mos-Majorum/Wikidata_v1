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
User_group = np.zeros([len(article_list),6])
Raw_Count_per_group = np.zeros([6,6])

for user_index in np.arange(0,len(article_list),1):
    for article_index in np.arange(0,len(article_list[user_index]),1):
        local_group = page_group[page_list.index(article_list[user_index][article_index])]
        User_group[user_index,local_group]+=edit_list[user_index][article_index]

for user_index in np.arange(0,len(article_list),1):
    Raw_Count_per_group[0,0]+=User_group[user_index,0]
    Raw_Count_per_group[1,1]+=User_group[user_index,1]
    Raw_Count_per_group[2,2]+=User_group[user_index,2]
    Raw_Count_per_group[3,3]+=User_group[user_index,3]
    Raw_Count_per_group[4,4]+=User_group[user_index,4]
    Raw_Count_per_group[5,5]+=User_group[user_index,5]
    if (User_group[user_index,0]>0)and(User_group[user_index,1]>0):
        Raw_Count_per_group[0,1]+=(User_group[user_index,1]+User_group[user_index,0])*0.5
    if (User_group[user_index,0]>0)and(User_group[user_index,2]>0):
        Raw_Count_per_group[0,2]+=(User_group[user_index,2]+User_group[user_index,0])*0.5
    if (User_group[user_index,0]>0)and(User_group[user_index,3]>0):
        Raw_Count_per_group[0,3]+=(User_group[user_index,3]+User_group[user_index,0])*0.5
    if (User_group[user_index,0]>0)and(User_group[user_index,4]>0):
        Raw_Count_per_group[0,4]+=(User_group[user_index,4]+User_group[user_index,0])*0.5
    if (User_group[user_index,0]>0)and(User_group[user_index,5]>0):
        Raw_Count_per_group[0,5]+=(User_group[user_index,5]+User_group[user_index,0])*0.5   
    if (User_group[user_index,1]>0)and(User_group[user_index,2]>0):
        Raw_Count_per_group[1,2]+=(User_group[user_index,2]+User_group[user_index,1])*0.5
    if (User_group[user_index,1]>0)and(User_group[user_index,3]>0):
        Raw_Count_per_group[1,3]+=(User_group[user_index,3]+User_group[user_index,1])*0.5
    if (User_group[user_index,1]>0)and(User_group[user_index,4]>0):
        Raw_Count_per_group[1,4]+=(User_group[user_index,4]+User_group[user_index,1])*0.5
    if (User_group[user_index,1]>0)and(User_group[user_index,5]>0):
        Raw_Count_per_group[1,5]+=(User_group[user_index,5]+User_group[user_index,1])*0.5
    if (User_group[user_index,2]>0)and(User_group[user_index,3]>0):
        Raw_Count_per_group[2,3]+=(User_group[user_index,3]+User_group[user_index,2])*0.5
    if (User_group[user_index,2]>0)and(User_group[user_index,4]>0):
        Raw_Count_per_group[2,4]+=(User_group[user_index,4]+User_group[user_index,2])*0.5
    if (User_group[user_index,2]>0)and(User_group[user_index,5]>0):
        Raw_Count_per_group[2,5]+=(User_group[user_index,5]+User_group[user_index,2])*0.5
    if (User_group[user_index,3]>0)and(User_group[user_index,4]>0):
        Raw_Count_per_group[3,4]+=(User_group[user_index,4]+User_group[user_index,3])*0.5
    if (User_group[user_index,3]>0)and(User_group[user_index,5]>0):
        Raw_Count_per_group[3,5]+=(User_group[user_index,5]+User_group[user_index,3])*0.5
    if (User_group[user_index,4]>0)and(User_group[user_index,5]>0):
        Raw_Count_per_group[4,5]+=(User_group[user_index,5]+User_group[user_index,4])*0.5
  
Normalized_Count_per_group = Raw_Count_per_group
Normalized_Count_per_group[0,:] = Normalized_Count_per_group[0,:]/(Normalized_Count_per_group[0,0])
Normalized_Count_per_group[1,:] = Normalized_Count_per_group[1,:]/(Normalized_Count_per_group[1,1])
Normalized_Count_per_group[2,:] = Normalized_Count_per_group[2,:]/(Normalized_Count_per_group[2,2])
Normalized_Count_per_group[3,:] = Normalized_Count_per_group[3,:]/(Normalized_Count_per_group[3,3])
Normalized_Count_per_group[4,:] = Normalized_Count_per_group[4,:]/(Normalized_Count_per_group[4,4])
Normalized_Count_per_group[5,:] = Normalized_Count_per_group[5,:]/(Normalized_Count_per_group[5,5])

x_group = ["Feminisme","LGBT","Racisme","TheorieWoke","CritiqueWoke","Groupe_Temoin"]
y_group = ["Feminisme","LGBT","Racisme","TheorieWoke","CritiqueWoke","Groupe_Temoin"]
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(Normalized_Count_per_group, interpolation='nearest', cmap="gray")
for i in np.arange(0,6,1):
    for j in np.arange(0,6,1):
        c = np.round(Normalized_Count_per_group[j,i],3)
        ax.text(i, j, str(c), va='center', ha='center')
fig.colorbar(cax)
#fig.colorbar.set_label('# of edits', rotation=270)

ax.set_xticklabels(['']+x_group)
ax.set_yticklabels(['']+y_group)
plt.setp(ax.get_xticklabels(), rotation=45, ha='left')
plt.show()