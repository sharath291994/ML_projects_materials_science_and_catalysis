
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import math
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# ===============================
# Load and clean data
# ===============================
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

# ===============================
# Helper: create output folders
# ===============================
def create_output_dirs(base_path):
    corr_dir = os.path.join(base_path, "correlation_matrices")
    freq_dir = os.path.join(base_path, "frequency_distributions")
    CE_fit_dir = os.path.join(base_path, "CE_fit")
    
    os.makedirs(corr_dir, exist_ok=True)
    os.makedirs(freq_dir, exist_ok=True)
    os.makedirs(CE_fit_dir, exist_ok=True)
    
    return corr_dir, freq_dir, CE_fit_dir

# ===============================
# Correlation Analysis
# ===============================
def correlation_analysis(df, output_dir, methods=["pearson", "kendall", "spearman"], n_cols=None):
    df = df.iloc[:, 1:]    
    if n_cols:
        df = df.iloc[:, :n_cols]

    results = {}
    for method in methods:
        corr_matrix = df.corr(method=method)
        results[method] = corr_matrix

        # Save correlation matrix to Excel
        corr_file = os.path.join(output_dir, f"correlation_{method}.xlsx")
        corr_matrix.to_excel(corr_file)
        
        # Plot heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True)
        plt.title(f"Correlation Matrix ({method.capitalize()})")
        plt.savefig(os.path.join(output_dir, f"correlation_{method}.png"))
        plt.close()
    return results

# ===============================
# Frequency Distributions
# ===============================
def frequency_distributions(df, output_dir):
    df = df.iloc[:, 1:-1]
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col], bins=20, kde=True, color="blue")
        plt.title(f"Frequency Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.savefig(os.path.join(output_dir, f"{col}_frequency.png"))
        plt.close()

# ====================================================
# CE fit - Least squares regression technique
# ====================================================

def CE_fit(df, output_dir):
    """
    Fits the last row (as target) with all other rows (as features)
    using a Linear Regression model.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        output_dir (str): Directory to save regression results
        
    Returns:
        dict: Model coefficients, intercept, R² score, and predictions
    """
    
    # Transpose so rows become samples and columns become features
    df = pd.read_excel('Amat_Bvec.xlsx')

    df = df.iloc[:, 1:]
 
    # Features: all columns except the last one
    X = df.iloc[:, :-1].values

    # Target: values of the last column
    y = df.iloc[:,-1].values

    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)

    # Predictions
    y_pred = model.predict(X)
 
    # Compute metrics
    r2 = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = math.sqrt(mse)

    # Store results
    results = {
        "coefficients": model.coef_,
        "intercept": model.intercept_,
        "r2_score": r2,
        "rmse": rmse,
        "predictions": y_pred
    }

    # Optional: Plot predictions vs actual
    plt.figure(figsize=(6, 6))
    plt.scatter(y, y_pred, color='blue', edgecolor='k', alpha=0.7)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)  # 45-degree reference line
    plt.xlabel("DFT values (eV)", fontsize=14)
    plt.ylabel("CE model predictions (eV)", fontsize=14)
    plt.title("CE model Parity plot", fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "CE_fit_plot.png"))
    plt.close()
    return results

# ===============================
# Main utility function
# ===============================
def run_analysis(file_path, n_cols=None, corr_methods=["pearson", "kendall", "spearman"],
                 do_correlation=True, do_frequency=True, do_ce_fit=True):
    
    base_dir = os.path.dirname(os.path.abspath(file_path))
    corr_dir, freq_dir, CE_fit_dir = create_output_dirs(base_dir)
    
    df = load_data(file_path)
    
    if do_correlation:
        correlation_analysis(df, corr_dir, methods=corr_methods, n_cols=n_cols)
    
    if do_frequency:
        frequency_distributions(df, freq_dir)
          
    if do_ce_fit:
     CE_fit(df, CE_fit_dir)
                     
    print("Analysis complete. Results saved in subfolders of:", base_dir)

print("Module loaded successfully.")

