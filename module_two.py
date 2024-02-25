"""
Module 2 - Assignment
    Code to run the graph(s).
"""

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Load the CSV file into a DataFrame
df = pd.read_csv("Index__Violent__Property__and_Firearm_Rates_By_County__Beginning_1990.csv")

#filter the data for the year 2022
df_2022 = df[df['Year'] == 2022]

# Calculate the average Index Rate for each county over the year 2022
average_index_rate_2022 = df_2022.groupby('County')['Index Rate'].mean()

# Get the top 10 counties with the highest average Index Rate in 2022
top_10_counties_2022 = average_index_rate_2022.nlargest(10)

# Plotting the horizontal bar graph with switched axes
# First graph to show which counties have the highest crime rates in 2022
plt.figure(figsize=(10, 6))
top_10_counties_2022.sort_values().plot(kind='barh', color='skyblue')  # Switched to horizontal bar graph
plt.title('Top 10 Counties with Highest Average Crime Rates in 2022')
plt.xlabel('Crime Rate per 100,000 Population')
plt.ylabel('County')  # Switched to y-axis label for County
plt.show()

# Second graph to provide more detailed information, sorted in ascending order.
#shows the population of the top ten counties with highest average crime rates
top_10_population_2022 = df_2022.groupby('County')['Population'].max().loc[top_10_counties_2022.index]
plt.barh(top_10_population_2022.index, top_10_population_2022.sort_values() / 1000, color='orange', alpha=0.7, label='Population (scaled)')
plt.barh(top_10_population_2022.index, top_10_population_2022.sort_values(), color='orange')
plt.title('Population of Top 10 Counties with Highest Average Crime Rates in 2022')
plt.xlabel('Population')
plt.ylabel('County')
plt.show()


#last graph.
#need some graph to make node connections, nodes, edges, etc.
"""
This script creates a directed network graph where each node represents a county, and edges represent connections between counties.
Node attributes include population and firearm rate. 
The size of the nodes is proportional to the population, and the labels show both the population and firearm rate. 
"""
data = df_2022[['County', 'Population', 'Firearm Rate']]

# Create a directed graph
G = nx.DiGraph()

# Add nodes (counties) with attributes for the top 10 counties
for county in top_10_counties_2022.index:
    row = df_2022[df_2022['County'] == county].iloc[0]
    G.add_node(county, population=row['Population'], firearm_rate=row['Firearm Rate'])

# Add edges between the top 10 counties based on firearm rates
for county1 in top_10_counties_2022.index:
    for county2 in top_10_counties_2022.index:
        if county1 != county2:
            if G.nodes[county1]['firearm_rate'] > G.nodes[county2]['firearm_rate']:
                G.add_edge(county1, county2)

# Visualize the graph with arrows indicating firearm rate relationships
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', edge_color='gray', width=0.5, connectionstyle='arc3,rad=0.1', arrowsize=15)

# Add labels
labels = {county: f"Pop: {G.nodes[county]['population']}\nFR: {G.nodes[county]['firearm_rate']}" for county in G.nodes}
nx.draw_networkx_labels(G, pos, labels, font_size=6)

plt.title('Directed Network Graph: Firearm Rate vs Population by County (Top 10 Counties with Highest Average Crime Rates in 2022)')
plt.show()