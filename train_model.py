import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE

# Load dataset
df = pd.read_csv("brain_stroke.csv")

# Select ONLY required features
df = df[['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi', 'stroke']]

# Rename for consistency
df.rename(columns={'avg_glucose_level': 'glucose'}, inplace=True)

# Handle missing values
df['bmi'].fillna(df['bmi'].mean(), inplace=True)

# Features & Target
X = df[['age', 'hypertension', 'heart_disease', 'glucose', 'bmi']]
y = df['stroke']

print("Before balancing:\n", y.value_counts())

# Apply SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

print("\nAfter balancing:\n", pd.Series(y_resampled).value_counts())

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy}")

# Save model
joblib.dump(model, "model.pkl")

print("\n✅ Model trained successfully with 5 features!")