import pandas as pd
import statsmodels.api as sm
import logging
import warnings

warnings.simplefilter("ignore")  # Ignore specific warnings during fitting
logging.basicConfig(level=logging.INFO)

def fit_linear_regression(X, y, columns, method):
    try:
        model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[columns]))).fit(method=method)
        return model
    except Exception as e:
        logging.error(f"Error fitting linear regression model using method {method}: {e}")
        return None

def drop_worst_feature(X, y, included_features, threshold_out, dropped_variables, method):
    model = fit_linear_regression(X, y, included_features, method)
    if model:
        pvalues = model.pvalues.iloc[1:]
        worst_pval = pvalues.max()
        if worst_pval > threshold_out:
            worst_feature = pvalues.idxmax()
            included_features.remove(worst_feature)
            dropped_variables.append(worst_feature)
            logging.info(f'Dropped feature {worst_feature} with p-value {worst_pval}')
            return True
    return False

def backward_regression(X, y, initial_list=[], threshold_in=0.01, threshold_out=0.05, include_interactions=True, verbose=True, method='pinv'):
    included_features = list(X.columns) if not initial_list else initial_list
    dropped_variables = []
    
    iteration = 1
    while True:
        changed = drop_worst_feature(X, y, included_features, threshold_out, dropped_variables, method)
        
        if not changed:
            break
        
        iteration += 1
        if verbose:
            logging.info(f"Iteration {iteration}: Current features: {included_features}")

    if include_interactions:
        included_with_interactions = included_features.copy()
        for i in range(len(included_features)):
            for j in range(i + 1, len(included_features)):
                interaction_term = f"{included_features[i]} * {included_features[j]}"
                X[interaction_term] = X[included_features[i]] * X[included_features[j]]
                
                model = fit_linear_regression(X, y, included_with_interactions + [interaction_term], method)
                if model:
                    pval_interaction = model.pvalues.get(interaction_term, 1)
                    
                    if pval_interaction < threshold_in:
                        included_with_interactions.append(interaction_term)
                        logging.info(f'Included interaction term {interaction_term} with p-value {pval_interaction}')
                    else:
                        X.drop(columns=[interaction_term], inplace=True)
                        dropped_variables.append(interaction_term)
                        logging.info(f'Dropped interaction term {interaction_term} with p-value {pval_interaction}')
        
        return included_with_interactions, dropped_variables
    else:
        return included_features, dropped_variables
