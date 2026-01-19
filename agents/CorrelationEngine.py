import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from scipy import stats

class CorrelationEngine:
    def __init__(self):
        self.model = LinearRegression()
        self.pca = PCA(n_components=2)
        self.p_values = None
        self.r_squared = None
        self.pca_explained_variance = None

    def calculate_p_values(self, X, y, predictions):
        """Calculate p-values for regression coefficients using t-tests"""
        n = len(y)
        k = X.shape[1]
        
        # Calculate residuals
        residuals = y - predictions
        residual_std_error = np.sqrt(np.sum(residuals**2) / (n - k - 1))
        
        # Calculate standard errors for coefficients
        X_with_intercept = np.column_stack([np.ones(n), X])
        try:
            var_covar_matrix = residual_std_error**2 * np.linalg.inv(X_with_intercept.T @ X_with_intercept)
            std_errors = np.sqrt(np.diag(var_covar_matrix))
            
            # Calculate t-statistics
            coefficients = np.concatenate([[self.model.intercept_], self.model.coef_])
            t_stats = coefficients / std_errors
            
            # Calculate p-values (two-tailed)
            p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), df=n - k - 1))
            return p_values[1:]  # Return p-values for features (exclude intercept)
        except:
            return None

    def run_regression(self, X, y):
        """
        Run Multivariate Regression and PCA analysis with statistical significance.
        Returns: Outcome Correlation Index with R², P-values, and PCA variance explained.
        """
        if len(X) < 2:
            print("⚠️ Not enough samples for correlation. Provide N ≥ 2.")
            return {"r_squared": np.nan, "p_values": None, "significance": "Insufficient data"}
        
        # Calculate feature variances to detect problematic data
        feature_names = ["TCR", "SPI", "DCR", "CI"]
        variances = np.var(X, axis=0)
        
        print("\n📊 Feature Statistics:")
        for i, name in enumerate(feature_names):
            print(f"   {name}: mean={np.mean(X[:, i]):.4f}, std={np.std(X[:, i]):.4f}, var={variances[i]:.6f}")
        
        # Fit Linear Regression model
        self.model.fit(X, y)
        predictions = self.model.predict(X)
        
        # Calculate R² score
        self.r_squared = self.model.score(X, y)
        
        # Calculate p-values for statistical significance
        self.p_values = self.calculate_p_values(X, y, predictions)
        
        # Perform PCA analysis
        try:
            self.pca.fit(X)
            self.pca_explained_variance = self.pca.explained_variance_ratio_
        except:
            self.pca_explained_variance = None
        
        # Determine overall significance (if any p-value < 0.05)
        if self.p_values is not None:
            significant_features = []
            for i, (name, p_val) in enumerate(zip(feature_names, self.p_values)):
                if p_val < 0.05:
                    significant_features.append(f"{name} (p={p_val:.4f})")
            
            if significant_features:
                significance = f"Significant features: {', '.join(significant_features)}"
            else:
                significance = "No significant features (all p >= 0.05)"
        else:
            significance = "Unable to calculate p-values"
        
        # Print detailed results
        print("\n📈 Regression Analysis Results:")
        print(f"   R² Score: {self.r_squared:.4f}")
        print(f"   Significance: {significance}")
        
        if self.p_values is not None:
            print("\n   Feature Analysis:")
            for i, name in enumerate(feature_names):
                coef = self.model.coef_[i]
                p_val = self.p_values[i]
                sig_marker = "✓" if p_val < 0.05 else "✗"
                print(f"   {sig_marker} {name}: coef={coef:.6f}, p-value={p_val:.6f}")
        
        # Create Outcome Correlation Index report
        outcome_correlation_index = {
            "r_squared": round(self.r_squared, 4),
            "p_values": [round(p, 6) for p in self.p_values] if self.p_values is not None else None,
            "significance": significance,
            "feature_names": feature_names,
            "coefficients": [round(c, 6) for c in self.model.coef_],
            "variances": [round(v, 6) for v in variances],
            "pca_variance": [round(v, 4) for v in self.pca_explained_variance] if self.pca_explained_variance is not None else None
        }
        
        return outcome_correlation_index