import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from datasets import load_dataset
import matplotlib.pyplot as plt

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
y = df['output_class'].values    # Target: binary class based on output_length threshold

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the feature (input_length) to have zero mean and unit variance
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize the SVM model with a linear kernel
model = SVC(kernel='linear', C=1.0, random_state=42, class_weight='balanced')

# Train the SVM model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Confusion Matrix:")
print(conf_matrix)
print("Classification Report:")
print(report)


# Plotting the distribution of the output_class
df['output_class'].value_counts().plot(kind='bar', color=['blue', 'orange'])
plt.title('Class Distribution in Dataset')
plt.xlabel('Class')
plt.ylabel('Number of Samples')
plt.xticks([0, 1], ['Class 0', 'Class 1'], rotation=0)
plt.show()

plt.hist(df['input_length'], bins=50, color='green', alpha=0.7)
plt.title('Distribution of Input Lengths')
plt.xlabel('Input Length')
plt.ylabel('Frequency')
plt.show()
