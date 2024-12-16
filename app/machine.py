import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from pandas import DataFrame


class Machine:
    def __init__(self, df: DataFrame):
       
        if df.empty:
            raise ValueError("The provided DataFrame is empty.")
        
        # Splitting features and target
        self.target_column = 'target'  # Change this to your actual target column name
        if self.target_column not in df.columns:
            raise ValueError(f"The DataFrame does not contain the target column: {self.target_column}")

        X = df.drop(columns=[self.target_column])
        y = df[self.target_column]
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train the default model
        self.model = RandomForestClassifier(random_state=42)
        self.model.fit(self.X_train, self.y_train)
        self.accuracy = self.model.score(self.X_test, self.y_test)

    def __call__(self, feature_basis: DataFrame):
       
        if feature_basis.empty:
            raise ValueError("The feature basis DataFrame is empty.")

        predictions = self.model.predict(feature_basis)
        probabilities = self.model.predict_proba(feature_basis)
        return predictions, probabilities

    def save(self, filepath: str):
       
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def open(filepath: str):
       
        with open(filepath, 'rb') as file:
            return pickle.load(file)

    def info(self):
       
        return {
            "model_type": type(self.model).__name__,
            "target_column": self.target_column,
            "train_accuracy": self.model.score(self.X_train, self.y_train),
            "test_accuracy": self.accuracy,
            "features": list(self.X_train.columns),
        }
