import sys
import numpy as np
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import create_logger
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
logger = create_logger(__name__)


def evaluate_models(X_train:np.array, y_train:np.array, X_test:np.array, y_test:np.array, models:dict, params:dict):
    try:
        reports= {}
        for model_name, model in models.items():
            param = params[model_name]

            gs = GridSearchCV(model, param, cv=3)
            gs.fit(X_train, y_train)
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            train_r2_score = r2_score(y_train, model.predict(X_train))
            test_r2_score = r2_score(y_test, y_pred)
            reports[model_name] = [train_r2_score, test_r2_score]

        return reports
    except Exception as e:
        raise NetworkSecurityException(e, sys.exc_info())