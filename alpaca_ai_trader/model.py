from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

scaler = StandardScaler()
model = RandomForestClassifier(n_estimators=100)

def train_model(X, y):
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, shuffle=False)
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    print(f"Model Accuracy: {acc:.2f}")
    joblib.dump(model, 'model.pkl')
    joblib.dump(scaler, 'scaler.pkl')

def load_model():
    return joblib.load('model.pkl'), joblib.load('scaler.pkl')