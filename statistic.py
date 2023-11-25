import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("orders.csv", sep=",")

grouped_data = df.groupby('Dish Name')['Quantity'].sum()

grouped_data.plot(kind = 'bar')
plt.xlabel('Dish Name')
plt.xticks(rotation=45) 
plt.ylabel('Quantity Sold')
plt.title('Total Selling Quantity for Each Dish')
plt.show()

grouped_data = df.groupby('Dish Name')['Selling($)'].sum()

grouped_data.plot(kind = 'bar')
plt.xlabel('Dish Name')
plt.xticks(rotation=45) 
plt.ylabel('Total Selling ($)')
plt.title('Total Selling($) for Each Dish')
plt.show()
