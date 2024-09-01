# -*- coding: utf-8 -*-
"""Kalpataru Home Buyer Preference MVA - Model

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xcD99ZPTJHjH8yWmd8qfLfBFFQNinRDQ
"""

!pip install --upgrade pandas cufflinks plotly google-auth gspread seaborn matplotlib scikit-learn --quiet

# Import the libraries
import pandas as pd
import cufflinks as cf
import plotly.express as px
import gspread
from google.colab import auth
from google.auth import default
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Authenticate and connect to Google Sheet - responses
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# Google Sheet URL
sheet_url = 'https://docs.google.com/spreadsheets/d/1MvcoTQqHV8RLJYK0r51rvCYzyNHAt0zMsLysQoeRxLk/edit?usp=sharing'
sheet = gc.open_by_url(sheet_url)
worksheet = sheet.worksheet('Encoded Data')
data = worksheet.get_all_records()

# Convert data to a DataFrame
df = pd.DataFrame(data)
print(df.head())

# Standardize data
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(df_scaled)
df['PCA1'] = pca_result[:, 0]
df['PCA2'] = pca_result[:, 1]

# K-means clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(df[['PCA1', 'PCA2']])
print(df.head())

# Ensure 'Cluster' is a string type for proper hue handling
df['Cluster'] = df['Cluster'].astype(str)

# Reset the plotting environment to clear any previous issues
plt.clf()
plt.close('all')

# Set Seaborn plot style
sns.set(style="whitegrid")

# Create scatter plot for PCA components colored by clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x='PCA1', y='PCA2', hue='Cluster', data=df, palette='Set2', s=100, alpha=0.8)

# Add titles and labels
plt.title('Clusters Based on PCA Components')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')

# Show the plot
plt.show()

#Correlations
import seaborn as sns
import matplotlib.pyplot as plt

# Calculate correlations between the original parameters
correlation_matrix = df.iloc[:, :7].corr()
# Display correlation matrix
print("\nCorrelation Matrix:")
print(correlation_matrix)

# Visualize the correlation matrix with a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap of Homebuyer Preferences')
plt.show()

# Cluster
for cluster in df['Cluster'].unique():
    print(f"\nDetailed Analysis of Cluster {cluster}:")
    cluster_data = df[df['Cluster'] == cluster]
    print(cluster_data.describe())  # Summary statistics for each cluster

    # Additional visualizations per cluster (e.g., histograms, box plots)
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=cluster_data.iloc[:, :7])  # Visualize distribution of original parameters
    plt.title(f'Distribution of Preferences in Cluster {cluster}')
    plt.xticks(rotation=45)
    plt.show()

#Linear Regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Updated Example: Predicting 'Developer Reputation' preference based on other parameters
X = df[['Prime Location', 'Sea Views/Open Views', 'Privacy and Exclusivity',
        'Spacious Layouts', 'Range of Amenities', 'Like-minded Neighbors']]
y = df['Developer Reputation']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and fit the regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model's performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nLinear Regression Analysis: Predicting 'Developer Reputation'")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")

# Display model coefficients to understand the impact of each feature
coefficients = pd.DataFrame({'Feature': X.columns, 'Coefficient': model.coef_})
print("\nModel Coefficients:")
print(coefficients)

# Visualize predicted vs. actual values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Actual Developer Reputation')
plt.ylabel('Predicted Developer Reputation')
plt.title('Predicted vs Actual Developer Reputation')
plt.show()

# Summary of Interpretations for All Analyses

# Summary of Clustering Analysis
print("\n--- Clustering Analysis Summary ---")

# Cluster Sizes
cluster_counts = df['Cluster'].value_counts()
print("\nCluster Sizes:")
print(cluster_counts)

# Cluster Means
cluster_means = df.groupby('Cluster').mean()
print("\nCluster Means (Key Characteristics of Each Cluster):")
print(cluster_means)

# Cluster Interpretation with Specific Insights
print("\nInterpretation of Clusters:")
for cluster, size in cluster_counts.items():
    print(f"\nCluster {cluster} (Size: {size}):")
    pca_mean_1 = cluster_means.loc[cluster, 'PCA1']
    pca_mean_2 = cluster_means.loc[cluster, 'PCA2']
    print(f"  - Average PCA1: {pca_mean_1:.2f}")
    print(f"  - Average PCA2: {pca_mean_2:.2f}")

    print("  - Key characteristics based on original parameters:")
    cluster_details = cluster_means.loc[cluster]
    for column in df.columns[:7]:  # Adjust range if more parameters are added
        value = cluster_details[column]
        print(f"    - {column}: {value:.2f}")

    # Specific Insights from Data
    if cluster_details['Prime Location'] > 3:
        print("  - Insight: This cluster values prime locations highly.")
    if cluster_details['Privacy and Exclusivity'] < 2:
        print("  - Insight: This cluster places less importance on privacy and exclusivity.")
    # Add similar conditions to highlight specific patterns

# Summary Correlation Analysis
print("\n--- Correlation Analysis Summary ---")

# Correlation Matrix
correlation_matrix = df.iloc[:, :7].corr()  # Use only original parameters
print("\nCorrelation Matrix:")
print(correlation_matrix)

# Identify and interpret strong correlations
high_corr = correlation_matrix[(correlation_matrix > 0.5) & (correlation_matrix != 1)].stack().reset_index()
high_corr.columns = ['Feature 1', 'Feature 2', 'Correlation']
print("\nHigh Correlations (above 0.5):")
print(high_corr)

# Specific Insights from Correlations
print("\nInterpretation of Correlations:")
for _, row in high_corr.iterrows():
    print(f"  - {row['Feature 1']} and {row['Feature 2']} have a strong correlation of {row['Correlation']:.2f}.")
    if row['Feature 1'] == 'Prime Location' or row['Feature 2'] == 'Prime Location':
        print("    - Insight: Prime Location is significantly related to this parameter, suggesting it's a key factor.")

# Summary of Regression Analysis
print("\n--- Regression Analysis Summary ---")

# Perform regression and evaluate results
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

X = df[['Prime Location', 'Sea Views/Open Views', 'Privacy and Exclusivity',
        'Spacious Layouts', 'Range of Amenities', 'Like-minded Neighbors']]
y = df['Developer Reputation']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

coefficients = pd.DataFrame({'Feature': X.columns, 'Coefficient': model.coef_})

print(f"\nLinear Regression Analysis: Predicting 'Developer Reputation'")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")
print("\nModel Coefficients:")
print(coefficients)

# Specific Insights from Regression Coefficients
print("\nInterpretation of Regression Coefficients:")
for index, row in coefficients.iterrows():
    if row['Coefficient'] > 0.5:
        print(f"  - {row['Feature']} has a strong positive impact on Developer Reputation with a coefficient of {row['Coefficient']:.2f}.")
    elif row['Coefficient'] < -0.5:
        print(f"  - {row['Feature']} has a strong negative impact on Developer Reputation with a coefficient of {row['Coefficient']:.2f}.")

# Step 4: Summary Additional Cluster Analysis
print("\n--- Additional Cluster Analysis Summary ---")

# Detailed Examination of Each Cluster
for cluster in df['Cluster'].unique():
    print(f"\nDetailed Analysis of Cluster {cluster}:")
    cluster_data = df[df['Cluster'] == cluster]
    cluster_summary = cluster_data.describe()
    print(cluster_summary)

    # Specific Insights based on data
    high_mean_features = cluster_summary.loc['mean'][cluster_summary.loc['mean'] > 3.5]
    low_mean_features = cluster_summary.loc['mean'][cluster_summary.loc['mean'] < 2.0]
    print("\nHigh Mean Features (values > 3.5):")
    print(high_mean_features)
    print("\nLow Mean Features (values < 2.0):")
    print(low_mean_features)
    print("  - Insights: These are the distinct preferences for this cluster.")