import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("ignmilton/ign_clean_instruct_dataset_500k")

# Convert the dataset to a pandas DataFrame for easier manipulation
df = pd.DataFrame(dataset['train'])  # Assuming you're using the 'train' split

# Create new columns for the length of input and output text
df['input_length'] = df['input'].apply(len)
df['output_length'] = df['output'].apply(len)

# Prepare the data
X = df[['input_length']]  # Feature: input_length
y = df['output_length']   # Target: output_length

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Plot the results
import matplotlib.pyplot as plt

plt.scatter(X_test, y_test, color='black')
plt.plot(X_test, y_pred, color='blue', linewidth=3)
plt.xlabel('Input Length')
plt.ylabel('Output Length')
plt.title('Linear Regression: Input Length vs. Output Length')
plt.show()
 