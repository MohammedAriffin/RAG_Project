import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pymc as pm
import numpy as np
from datasets import load_dataset
import arviz as az
import matplotlib as plt

# Load the dataset
dataset = load_dataset("ignmilton/ign_clean_instruct_dataset_500k")

# Convert the dataset to a pandas DataFrame for easier manipulation
df = pd.DataFrame(dataset['train'])

# Create new columns for the length of input and output text
df['input_length'] = df['input'].apply(len)
df['output_length'] = df['output'].apply(len)

# Set a threshold to classify the output length
threshold = 100  # Adjust based on your dataset
df['output_class'] = (df['output_length'] > threshold).astype(int)

# Prepare the data
X = df[['input_length']].values  # Feature: input_length
y = df['output_class'].values   # Target: binary class based on output_length threshold

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the feature (input_length)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define the Bayesian Logistic Regression model using PyMC
with pm.Model() as model:
    # Priors for unknown model parameters
    intercept = pm.Normal('intercept', mu=0, sigma=10)
    coef = pm.Normal('coef', mu=0, sigma=10, shape=(1,))

    # Linear combination
    linear_combination = intercept + pm.math.dot(X_train, coef)

    # Likelihood (observed data)
    probability = pm.Deterministic('probability', pm.math.sigmoid(linear_combination))
    observed = pm.Bernoulli('observed', p=probability, observed=y_train)

    # Inference
    trace = pm.sample(3000, tune=1000, target_accept=0.95, return_inferencedata=True)

# Posterior predictive checks
with model:
    ppc = pm.sample_posterior_predictive(trace, var_names=["observed"])

# Evaluate on the test set
with pm.Model() as test_model:
    # Use mean of the posterior distribution as point estimates
    intercept_test = pm.Normal('intercept_test', mu=trace.posterior['intercept'].mean(), sigma=10)
    coef_test = pm.Normal('coef_test', mu=trace.posterior['coef'].mean(axis=(0, 1)), sigma=10, shape=(1,))
    
    linear_combination_test = intercept_test + pm.math.dot(X_test, coef_test)
    probability_test = pm.Deterministic('probability_test', pm.math.sigmoid(linear_combination_test))
    
    predictions = pm.sample_posterior_predictive(trace, var_names=["probability_test"], samples=1000)

# Taking mean prediction as the final prediction
y_pred_proba = predictions.posterior_predictive['probability_test'].mean(axis=0)
y_pred = (y_pred_proba > 0.5).astype(int)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Confusion Matrix:")
print(conf_matrix)
print("Classification Report:")
print(report)

# Plot the results
az.plot_trace(trace)
plt.show()

# Posterior Predictive Check Plot
az.plot_ppc(ppc)
plt.show()
