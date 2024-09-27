#install libraries matplotlib, scikit-learn
#pip install matplotlib scikit-learn

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Simulated sales data (Months and Sales in USD)

months = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]).reshape(-1, 1)
sales = np.array([2000, 24002, 23003, 25004, 26005, 300066, 310066, 340066, 3500666, 37006666, 40006666, 42006666])

# Step 1: Plot the original data points
plt.scatter(months, sales, color='Green', label='Sales Data')

# Step 2: Create and fit the linear regression model
model = LinearRegression()
model.fit(months, sales)

# Step 3: Predict sales based on the model (regression line)
predicted_sales = model.predict(months)

# Step 4: Plot the regression line
plt.plot(months, predicted_sales, color='orange', label='Trend Line')

# Step 5: Add labels and title
plt.title('Sales Regression for Small Business')
plt.xlabel('Month')
plt.ylabel('Sales (USD)')
plt.legend()

# Display the plot
plt.show()
