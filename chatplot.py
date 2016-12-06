# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from scipy import signal
import seaborn as sns
import matplotlib.pyplot as plt

# Histogram with the total number of interventions per user
def plot_total_interventions_users(interventions_users_days, title='Number of interventions per user'):
	interventions_users = interventions_users_days.sum(axis=0)
	interventions_users.sort_values(inplace=True, ascending=False)
	interventions_users.plot(kind='bar')
	plt.title(r""+title)
	plt.show()


# Scatter matrix of the interventions per day of all users
def chat_scatter_matrix(data, title):
	p = pd.tools.plotting.scatter_matrix(data, alpha=0.2, figsize=(6, 6), diagonal='kde')
	plt.suptitle(r""+title, fontsize=18)
	plt.show()


# Scatter matrix of the interventions per day of all users
def chat_scatter_matrix_density(data):
	g = sns.PairGrid(data, diag_sharey=False)
	g.map_lower(sns.kdeplot, cmap="Blues_d")
	g.map_upper(plt.scatter)
	g.map_diag(sns.kdeplot, lw=3)
	plt.title(r'Scatter plot together with estimated pair densities')
	#plt.suptitle(r""+title, fontsize=18)
	plt.show()


# Evolution of the total number of interventions per day
# Also provides a smoothed version using the Savitsky-Golay filter
def plot_interventions_per_day(interventions_users_days, ki='line'):
	# Number of interventions per date
	interventions_days = interventions_users_days.sum(axis=1)
	interventions_days.plot(kind=ki)
	# Apply Savitzky–Golay filter
	K = 15
	if (K>=len(interventions_days)):
		K =len(interventions_days)
		if (len(interventions_days)%2 ==0):
			K -= 1
	interventions_days_filtered = signal.savgol_filter(interventions_days,K,2)
	plt.plot(interventions_days_filtered,color='red')
	plt.title(r'Number of interventions per day')
	plt.show()


# Distribution of the total number interventions per day. 
# Plots a histogram and an estimation of its PDF
def plot_distribution_total_interventions_per_day(interventions_users_days):
	interventions_days = interventions_users_days.sum(axis=1)
	#print interventions_days
	sns.distplot(interventions_days)#interventions_days.plot(kind='bar')
	plt.title('PDF estimation of the interventions per day')
	plt.show()


# Violin plot of interventions of each user per day
def violinplot_users_days(interventions_users_days):
	sns.violinplot(data=interventions_users_days, palette="Set3", bw=.2, cut=1, linewidth=1)
	plt.title(r'Interventions per day')
	plt.show()


# Histogram with the number of interventions in the different hour ranges in a day
def plot_interventions_per_hour(interventions_users_hours):
	interventions_hours = interventions_users_hours.sum(axis=1)
	#print interventions_hours
	interventions_hours.plot(kind='bar')
	plt.title(r'Number of interventions per hour')
	plt.show()
