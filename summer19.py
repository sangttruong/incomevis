from sklearn import linear_model
from google.colab import drive
drive.mount('/content/gdrive')
root_path = 'gdrive/My Drive/Colab Notebooks/'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  
# %matplotlib inline

df = pd.read_csv(root_path+"student_scores.csv")
df.shape
df.head()
df.describe()
df.plot(x="Hours",y="Scores",style="o")
plt.title("Hours vs Percentage")
plt.xlabel("Hours")
plt.ylabel("Percentage")
plt.show()

x = df.iloc[:, :-1].values
y = df.iloc[:, 1].values
print(x)
print(y)


# x = df["Hours"]
# y = df["Scores"]
# print(x)
# print(y)

from sklearn.model_selection import train_test_split  
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
from sklearn.linear_model import LinearRegression  
regressor = LinearRegression()  
regressor.fit(x_train, y_train)
print(regressor.intercept_)
print(regressor.coef_)

df
# x = df["Hours"].values

x = df.iloc[:,:1].values
y = df.iloc[:,0].values

print(x)
