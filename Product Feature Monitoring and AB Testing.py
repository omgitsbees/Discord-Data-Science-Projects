import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Generate a Simulated Dataset
np.random.seed(0)

# Simulate user data
user_ids = range(1, 1001)
groups = np.random.choice(['A', 'B'], size=1000, p=[0.5, 0.5])  # A = Control, B = Test
age = np.random.randint(18, 50, size=1000)
region = np.random.choice(['North America', 'Europe', 'Asia'], size=1000)

# Simulate engagement metrics
pre_session_count = np.random.poisson(lam=3, size=1000)
post_session_count = pre_session_count + np.random.poisson(lam=1, size=1000) + (groups == 'B').astype(int)  # Small boost for Test group
pre_time_spent = np.random.normal(loc=30, scale=5, size=1000)
post_time_spent = pre_time_spent + np.random.normal(loc=2, scale=2, size=1000) + (groups == 'B').astype(int) * 2  # Slightly more for Test group
feature_interactions = (groups == 'B').astype(int) * np.random.poisson(lam=2, size=1000)  # Test group interactions

# Create DataFrame
data = pd.DataFrame({
    'user_id': user_ids,
    'group': groups,
    'age': age,
    'region': region,
    'pre_session_count': pre_session_count,
    'post_session_count': post_session_count,
    'pre_time_spent': pre_time_spent,
    'post_time_spent': post_time_spent,
    'feature_interactions': feature_interactions
})

# Step 2: Calculate Baseline and Post-Exposure Metrics
# Calculate averages pre and post exposure for each group
control = data[data['group'] == 'A']
test = data[data['group'] == 'B']

# Baseline metrics
print("Baseline Metrics:")
avg_pre_control = control['pre_time_spent'].mean()
avg_pre_test = test['pre_time_spent'].mean()
print(f"Control Group - Avg Time Spent (Pre): {avg_pre_control}")
print(f"Test Group - Avg Time Spent (Pre): {avg_pre_test}")

# Post-exposure metrics
print("\nPost-Exposure Metrics:")
avg_post_control = control['post_time_spent'].mean()
avg_post_test = test['post_time_spent'].mean()
print(f"Control Group - Avg Time Spent (Post): {avg_post_control}")
print(f"Test Group - Avg Time Spent (Post): {avg_post_test}")

# Step 3: Conduct A/B Testing Analysis (T-Test)
t_stat, p_value = ttest_ind(control['post_time_spent'], test['post_time_spent'])
print("\nA/B Test Results:")
print(f"T-Statistic: {t_stat}, P-Value: {p_value}")

if p_value < 0.05:
    print("The difference is statistically significant.")
else:
    print("No statistically significant difference detected.")

# Step 4: Visualization of Results
# Plotting distributions of time spent for Control and Test groups
sns.histplot(control['post_time_spent'], color="blue", label="Control", kde=True)
sns.histplot(test['post_time_spent'], color="red", label="Test", kde=True)
plt.title("Time Spent - Control vs Test Groups")
plt.xlabel("Time Spent (Post-Exposure)")
plt.legend()
plt.show()

# Boxplot for side-by-side comparison of engagement by group
sns.boxplot(x='group', y='post_time_spent', data=data)
plt.title("User Engagement by Group (Post-Exposure)")
plt.ylabel("Time Spent (Post-Exposure)")
plt.show()
