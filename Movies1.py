import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
"""Questions:
1- What is the most popular genre over years?
2- How movies production changed each year??
3- What is most common runtime?
4- Does the runtime affect popularity? 
5- What is the correlation between revenue and (popularity/ vote average)?
6- Which months of the year are common in release ?

"""

"""Step1: load data (movies)"""
df_movies=pd.read_csv('tmdb-movies.csv')

"""Step 2: Assess data"""
pd.set_option('display.max_columns', None)
print(df_movies.head())       #Column names are separated by(_): ok
print(df_movies.shape)
print(df_movies.info())       #Get info about data
print(df_movies.describe())

print('***************END_2***************')

"""Step 3: Wrangling:"""
# 1-Check for Missing data (NaN values)
print(df_movies.isna().sum())                # Get NaN values in each column
df_movies.dropna(axis = 0, inplace= True)    #remove all rows with NaN values to deal with other values
print(df_movies.isnull().sum().any())        #Check no NaN rows
print(df_movies.shape)


# 2-Check for Duplicated data and drop unwanted columns
print(df_movies.duplicated().sum())          #find number of duplicated rows
df_movies.drop(columns=['id','homepage','cast','original_title',
                        'keywords', 'production_companies','tagline','vote_count','overview']
               , axis=1, inplace=True)       #For my questions I dont need these columns
print(df_movies.columns)                     #Check dropped columns

print('***************END_3.2***************')


# 3-Check for data dtype and fix if found, split strings
print(df_movies.dtypes)                      #Check current types

df_movies['release_date'] = pd.to_datetime(df_movies['release_date'])   #Convert release_date from string to datetime
df_movies['release_month'] = df_movies['release_date'].dt.month       #Extract month to new column
df_movies.drop(columns=['release_date'], axis=1, inplace=True)       #Remove release date column
print(df_movies.columns)                     #Check new columns


df_movies["genres"] = df_movies["genres"].str.split("|")              #Split different values of genres
df_movies = df_movies.explode('genres')                              #expand splitted genres
df_movies= df_movies.reset_index(drop=True)                          #reset index number

df_movies["director"] = df_movies["director"].str.split("|")              #Split different values of directors
df_movies = df_movies.explode('director')                              #expand splitted genres
df_movies= df_movies.reset_index(drop=True)                          #reset index number

pd.set_option('display.max_columns', None)                           #display all columns
print(df_movies.head())
print( 0 in df_movies.values)                                        #check zero values >> found

df_movies.replace(0, np.nan, inplace=True)                          #replace zero values with NaN to prevent analysis miscalculation
print( 0 in df_movies.values)                                       #check zero values >> no

df_movies.to_csv('movies_cleaned.csv', index=False)                 #Cleaned dataset
df_movies = pd.read_csv ('movies_cleaned.csv')                      #recall the clean new dataset

print('***************END_3***************')

"""Step 4: Exploratory Data Analysis:Visualization"""

"""1- What is the most popular genre over years and for each year ?"""
# For all years:
df_movies['genres'].value_counts().plot(kind='bar')
plt.xlabel('Genre', loc= 'left')
plt.tick_params(axis='x', labelsize=7)
plt.ylabel('Number')
plt.title('Genres popularity over years')
plt.show()                                          #drama is the most popular genre over years

"""2- How movies production changed each year?"""

print(df_movies[['release_year','imdb_id']].groupby('release_year').nunique())
df_movies[['release_year','imdb_id']].groupby('release_year').nunique()\
    .plot(kind='bar', title='No. Movies Each year', color = 'orange')
plt.xlabel('Year')
plt.tick_params(axis='x', labelsize=5)
plt.ylabel('No. of movies')
plt.yticks(np.arange(0, 240, 20))
plt.tick_params(axis='y', labelsize=7)
plt.legend('Movies No.', fontsize = 10)
plt.show()


"""3- What is most common runtime?"""

plt.hist(df_movies['runtime'], edgecolor='black', bins=np.arange(25,250,25))    #exclude very low and high values
plt.title("Histogram of Runtime")
plt.xlabel("Runtime")
plt.ylabel("Frequency")
plt.show()                          # The most common movies are those having average runtime (100:125)min


"""4- Does the runtime affect popularity?"""
df_movies.plot(x='runtime', y='popularity', kind="scatter");
plt.xlabel('Runtime')
plt.xlim([25, 250])
plt.ylabel('Popularity')
plt.title('Runtime effect on Popularity')
plt.show()                         #No apparent correlation can be seen between the runtime and popularity‎

"""5- What is the correlation between revenue and (popularity/ vote average) ?"""
df_movies.plot(x="revenue", y="popularity", kind="scatter");
plt.xlabel('Revenue')
plt.xlim([100, max(df_movies['revenue'])])
plt.ylabel('Popularity')
plt.title('Rev. Vs Pop')
plt.show()                              #I can say that there is no correlation between revenue and popularity

df_movies.plot(x="revenue", y="vote_average", kind="scatter");
plt.xlabel('Revenue')
plt.xlim([100, max(df_movies['revenue'])])
plt.ylabel('Vote Average')
plt.title('Rev. Vs Vote Av')
plt.show()                              #I can say that there is no correlation between revenue and vote average


"""6- Which months of the year are common in release ?"""
print(df_movies[['release_month','imdb_id']].groupby('release_month')['imdb_id'].nunique())
df_movies[['release_month','imdb_id']].groupby('release_month')['imdb_id'].nunique()\
    .plot(kind='pie', y='Movies release for months', autopct='%1.0f%%')
plt.suptitle("Movies release per month")
plt.show()


"""Helping Resources"""
#https://github.com/lakshanagv/Complete-guide-to-data-analysis-using-Python---IMDB-movies-data/blob/main/Quick%20guide%20to%20Data%20Analysis%20using%20Pandas.ipynb
#https://medium.com/datactw/imdb-dataset-visualization-data-analytics-using-pandas-97b5c6f03c6d
#https://stackoverflow.com/questions/50767452/check-if-dataframe-has-a-zero-element
#https://www.statology.org/pandas-replace-0-with-nan/
#https://www.geeksforgeeks.org/changing-the-tick-frequency-on-x-or-y-axis-in-matplotlib/
#https://www.statology.org/matplotlib-bin-size/
#https://www.geeksforgeeks.org/how-to-create-pie-chart-from-pandas-dataframe/
#Asking friends

