"""
AI Jobs Forecasting Model
=========================

Modeling Strategy:
- JOIN Database: Cross-sectional data (one year per country) - used as time-invariant predictors
- HAI Database: Panel data (multiple years per country) - used as target variables

Approach: Use JOIN country characteristics as fixed effects to predict HAI trends over time.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')


class AIJobsForecaster:
    """
    Model AI job trends using cross-sectional labor market data
    """

    def __init__(self, join_data, hai_data):
        """
        Initialize the forecaster with both datasets

        Parameters:
        -----------
        join_data : pd.DataFrame
            World Bank JOIN dataset (cross-sectional, one year per country)
        hai_data : pd.DataFrame
            HAI dataset (panel data, multiple years per country)
        """
        self.join_data = join_data.copy()
        self.hai_data = hai_data.copy()
        self.merged_data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()

    def merge_datasets(self):
        """
        Merge JOIN (cross-sectional) with HAI (panel) data

        Strategy:
        - JOIN provides time-invariant country characteristics
        - Each HAI country-year observation gets matched with its country's JOIN characteristics
        """
        # Find common countries
        common_countries = np.intersect1d(
            self.join_data['country_code'].unique(),
            self.hai_data['code'].unique()
        )

        print(f"Countries in JOIN: {len(self.join_data['country_code'].unique())}")
        print(f"Countries in HAI: {len(self.hai_data['code'].unique())}")
        print(f"Common countries: {len(common_countries)}")

        # Filter both datasets to common countries
        join_filtered = self.join_data[
            self.join_data['country_code'].isin(common_countries)
        ].copy()

        hai_filtered = self.hai_data[
            self.hai_data['code'].isin(common_countries)
        ].copy()

        # Merge: JOIN characteristics are repeated for each HAI year
        # This is a many-to-one merge (many HAI years to one JOIN observation)
        merged = hai_filtered.merge(
            join_filtered,
            left_on='code',
            right_on='country_code',
            how='inner',
            suffixes=('_hai', '_join')
        )

        print(f"\nMerged dataset shape: {merged.shape}")
        print(f"Years in merged data: {sorted(merged['publishyear'].unique())}")
        print(f"Countries in merged data: {merged['code'].nunique()}")

        self.merged_data = merged
        return merged

    def select_features(self, target_variable='ai_job_postings_perc_of_all_job_postings'):
        """
        Select relevant features for modeling

        Parameters:
        -----------
        target_variable : str
            Target variable from HAI dataset to predict

        Returns:
        --------
        X : pd.DataFrame
            Feature matrix
        y : pd.Series
            Target variable
        """
        if self.merged_data is None:
            raise ValueError("Must merge datasets first. Call merge_datasets()")

        # Define feature categories from JOIN dataset

        # Demographics
        demographic_features = [
            'total_population',
            'youth_aged_1524',
            'adult_aged_2564',
            'elderly_aged_65',
            'urban_population__of_total_population',
            'working_age_population_aged_1564'
        ]

        # Labor Force
        labor_force_features = [
            'labor_force_participation_rate_aged_1564',
            'female_labor_force_participation_rate_aged_1564',
            'not_in_labor_force_or_education_rate_among_youth_aged_1524',
            'employment_to_population_ratio_aged_1564',
            'unemployment_rate_aged_1564'
        ]

        # Education
        education_features = [
            'employed_with_primary_education_or_less_aged_1564',
            'employed_with_secondary_education_aged_1564',
            'employed_with_tertiary_education_aged_1564'
        ]

        # Sector
        sector_features = [
            'employment_in_agriculture_aged_1564',
            'employment_in_industry_aged_1564',
            'employment_in_services_aged_1564'
        ]

        # Combine all features
        all_features = (
            demographic_features +
            labor_force_features +
            education_features +
            sector_features
        )

        # Filter to features that exist in the dataset
        available_features = [f for f in all_features if f in self.merged_data.columns]

        print(f"\nFeatures selected: {len(available_features)}")
        print(f"Features not found: {set(all_features) - set(available_features)}")

        # Add time-related features from HAI
        time_features = ['publishyear']
        available_features += time_features

        # Create feature matrix
        X = self.merged_data[available_features].copy()

        # Create target variable
        if target_variable not in self.merged_data.columns:
            raise ValueError(f"Target variable '{target_variable}' not found in merged data")

        y = self.merged_data[target_variable].copy()

        # Handle missing values
        print(f"\nMissing values before imputation:")
        print(X.isnull().sum()[X.isnull().sum() > 0])

        # Drop rows with missing target
        valid_idx = ~y.isnull()
        X = X[valid_idx]
        y = y[valid_idx]

        # Impute missing features with median
        for col in X.columns:
            if X[col].isnull().sum() > 0:
                X[col].fillna(X[col].median(), inplace=True)

        print(f"\nFinal dataset: {X.shape[0]} observations, {X.shape[1]} features")

        self.feature_names = available_features
        self.target_name = target_variable

        return X, y

    def train_test_split_temporal(self, X, y, test_size=0.2, test_year=2021):
        """
        Split data into train/test sets using temporal split

        Strategy: Train on earlier years, test on recent years
        """
        # Get year from merged data
        years = self.merged_data.loc[X.index, 'publishyear']

        # Temporal split
        train_mask = years < test_year
        test_mask = years >= test_year

        X_train = X[train_mask]
        X_test = X[test_mask]
        y_train = y[train_mask]
        y_test = y[test_mask]

        print(f"\nTemporal Train-Test Split:")
        print(f"Train: {len(X_train)} observations (years < {test_year})")
        print(f"Test: {len(X_test)} observations (years >= {test_year})")

        # Standardize features
        X_train_scaled = pd.DataFrame(
            self.scaler.fit_transform(X_train),
            columns=X_train.columns,
            index=X_train.index
        )

        X_test_scaled = pd.DataFrame(
            self.scaler.transform(X_test),
            columns=X_test.columns,
            index=X_test.index
        )

        self.X_train = X_train_scaled
        self.X_test = X_test_scaled
        self.y_train = y_train
        self.y_test = y_test

        return X_train_scaled, X_test_scaled, y_train, y_test

    def train_models(self):
        """
        Train multiple models and compare performance
        """
        if self.X_train is None:
            raise ValueError("Must split data first. Call train_test_split_temporal()")

        # Define models
        models = {
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(alpha=1.0),
            'Lasso Regression': Lasso(alpha=0.1),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }

        print("\n" + "="*80)
        print("Training Models")
        print("="*80)

        for name, model in models.items():
            print(f"\n{name}...")

            # Train
            model.fit(self.X_train, self.y_train)

            # Predict
            y_train_pred = model.predict(self.X_train)
            y_test_pred = model.predict(self.X_test)

            # Evaluate
            train_r2 = r2_score(self.y_train, y_train_pred)
            test_r2 = r2_score(self.y_test, y_test_pred)
            train_rmse = np.sqrt(mean_squared_error(self.y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(self.y_test, y_test_pred))
            test_mae = mean_absolute_error(self.y_test, y_test_pred)

            # Store results
            self.models[name] = model
            self.results[name] = {
                'train_r2': train_r2,
                'test_r2': test_r2,
                'train_rmse': train_rmse,
                'test_rmse': test_rmse,
                'test_mae': test_mae,
                'predictions': y_test_pred
            }

            print(f"  Train R²: {train_r2:.4f}")
            print(f"  Test R²:  {test_r2:.4f}")
            print(f"  Test RMSE: {test_rmse:.4f}")
            print(f"  Test MAE:  {test_mae:.4f}")

        # Print summary
        print("\n" + "="*80)
        print("Model Comparison Summary")
        print("="*80)
        results_df = pd.DataFrame(self.results).T
        print(results_df[['train_r2', 'test_r2', 'test_rmse', 'test_mae']])

        return self.results

    def get_feature_importance(self, model_name='Random Forest', top_n=15):
        """
        Get feature importance from tree-based models
        """
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not trained yet")

        model = self.models[model_name]

        if not hasattr(model, 'feature_importances_'):
            print(f"{model_name} does not support feature importance")
            return None

        # Get importances
        importances = model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)

        print(f"\n{model_name} - Top {top_n} Most Important Features:")
        print("="*80)
        print(feature_importance_df.head(top_n).to_string(index=False))

        return feature_importance_df

    def plot_predictions(self, model_name='Random Forest', save_path=None):
        """
        Plot actual vs predicted values
        """
        if model_name not in self.results:
            raise ValueError(f"Model '{model_name}' not trained yet")

        y_pred = self.results[model_name]['predictions']

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Scatter plot
        axes[0].scatter(self.y_test, y_pred, alpha=0.6)
        axes[0].plot([self.y_test.min(), self.y_test.max()],
                     [self.y_test.min(), self.y_test.max()],
                     'r--', lw=2)
        axes[0].set_xlabel('Actual', fontsize=12)
        axes[0].set_ylabel('Predicted', fontsize=12)
        axes[0].set_title(f'{model_name}: Actual vs Predicted', fontsize=14)
        axes[0].text(0.05, 0.95, f'R² = {self.results[model_name]["test_r2"]:.3f}',
                     transform=axes[0].transAxes, va='top')

        # Residuals plot
        residuals = self.y_test - y_pred
        axes[1].scatter(y_pred, residuals, alpha=0.6)
        axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
        axes[1].set_xlabel('Predicted', fontsize=12)
        axes[1].set_ylabel('Residuals', fontsize=12)
        axes[1].set_title(f'{model_name}: Residuals Plot', fontsize=14)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")

        plt.show()

    def forecast_future(self, model_name='Random Forest', future_years=[2024, 2025]):
        """
        Generate forecasts for future years

        Note: Since JOIN data is static (one year), we assume country characteristics
        remain constant. Only the year variable changes.
        """
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not trained yet")

        model = self.models[model_name]

        # Get latest available data for each country
        latest_data = self.merged_data.loc[self.X_train.index.union(self.X_test.index)].copy()
        latest_by_country = latest_data.groupby('code').last().reset_index()

        # Create forecast dataframe
        forecasts = []

        for year in future_years:
            year_data = latest_by_country.copy()
            year_data['publishyear'] = year

            # Prepare features
            X_future = year_data[self.feature_names].copy()

            # Handle missing values
            for col in X_future.columns:
                if X_future[col].isnull().sum() > 0:
                    X_future[col].fillna(X_future[col].median(), inplace=True)

            # Scale
            X_future_scaled = pd.DataFrame(
                self.scaler.transform(X_future),
                columns=X_future.columns,
                index=X_future.index
            )

            # Predict
            predictions = model.predict(X_future_scaled)

            # Store results
            forecast_df = pd.DataFrame({
                'country_code': year_data['code'].values,
                'country_name': year_data['countryname'].values,
                'year': year,
                f'predicted_{self.target_name}': predictions
            })

            forecasts.append(forecast_df)

        forecast_results = pd.concat(forecasts, ignore_index=True)

        print(f"\nForecast Summary for {future_years}:")
        print(forecast_results.groupby('year')[f'predicted_{self.target_name}'].describe())

        return forecast_results


def main():
    """
    Main execution function
    """
    print("="*80)
    print("AI Jobs Forecasting Model - JobsLens AI")
    print("="*80)

    # Load and prepare data
    print("\n1. Loading datasets...")

    # Load JOIN dataset
    join_dataset = pd.read_excel('Team_Projects/JobsLens_AI/data/join_dataset.xlsx')
    join_dataset.columns = join_dataset.iloc[2]
    join_dataset = join_dataset.iloc[3:]
    join_dataset.columns = (
        join_dataset.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace(r'[^\w_]', '', regex=True)
    )

    # Filter subsample for 'Urban' only (as specified)
    join_dataset = join_dataset[join_dataset['subsample'] == 'Urban']

    # Filter to latest date for each country
    join_dataset['year_of_survey'] = join_dataset['year_of_survey'].astype(int)
    latest_date = join_dataset.groupby('country_code', as_index=False)['year_of_survey'].max()
    join_dataset = join_dataset.merge(latest_date, on=['country_code', 'year_of_survey'], how='inner')

    # Load HAI dataset
    hai_data = pd.read_csv('Team_Projects/JobsLens_AI/data/hai_full_database.csv')
    hai_data.columns = hai_data.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(r'[^\w_]', '', regex=True)

    print(f"JOIN dataset: {join_dataset.shape}")
    print(f"HAI dataset: {hai_data.shape}")

    # Initialize forecaster
    print("\n2. Initializing forecaster...")
    forecaster = AIJobsForecaster(join_dataset, hai_data)

    # Merge datasets
    print("\n3. Merging datasets...")
    merged = forecaster.merge_datasets()

    # Select features and target
    print("\n4. Selecting features and target variable...")
    X, y = forecaster.select_features(target_variable='ai_job_postings_perc_of_all_job_postings')

    # Train-test split (temporal)
    print("\n5. Splitting data (temporal split)...")
    X_train, X_test, y_train, y_test = forecaster.train_test_split_temporal(
        X, y, test_year=2021
    )

    # Train models
    print("\n6. Training models...")
    results = forecaster.train_models()

    # Feature importance
    print("\n7. Analyzing feature importance...")
    feature_importance = forecaster.get_feature_importance(model_name='Random Forest', top_n=15)

    # Plot predictions
    print("\n8. Generating visualizations...")
    forecaster.plot_predictions(
        model_name='Random Forest',
        save_path='Team_Projects/JobsLens_AI/visualizations/model_predictions.png'
    )

    # Generate forecasts
    print("\n9. Generating 2024-2025 forecasts...")
    forecasts = forecaster.forecast_future(
        model_name='Random Forest',
        future_years=[2024, 2025]
    )

    # Save results
    print("\n10. Saving results...")
    forecasts.to_csv('Team_Projects/JobsLens_AI/data/forecasts_2024_2025.csv', index=False)
    feature_importance.to_csv('Team_Projects/JobsLens_AI/data/feature_importance.csv', index=False)

    print("\n" + "="*80)
    print("Modeling complete!")
    print("="*80)
    print("\nOutputs:")
    print("  - Forecasts: Team_Projects/JobsLens_AI/data/forecasts_2024_2025.csv")
    print("  - Feature importance: Team_Projects/JobsLens_AI/data/feature_importance.csv")
    print("  - Predictions plot: Team_Projects/JobsLens_AI/visualizations/model_predictions.png")

    return forecaster, forecasts, feature_importance


if __name__ == "__main__":
    forecaster, forecasts, feature_importance = main()
