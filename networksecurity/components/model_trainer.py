import os
import sys
import numpy as np
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from networksecurity.constant.traning_pipeline import *
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import create_logger
from networksecurity.utils import save_object, load_object, save_numpy_array_data, load_numpy_array_data
from networksecurity.utils.ml_utils.metric.classification import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkSecurityModel
from networksecurity.utils.ml_utils.model.evaluation import evaluate_models
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier
)
import mlflow
import dagshub
dagshub.init(repo_owner='sadhiin', repo_name='network-security-mlops', mlflow=True)


  
  
logger = create_logger(__name__)


class ModelTrainer:
    def __init__(self,
                 model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())


    def __track_model_on_mlflow(self, model, classification_metric_train):
        with mlflow.start_run():
            f1_score = classification_metric_train.f1_score
            precision_score = classification_metric_train.precision_score
            recall_score = classification_metric_train.recall_score
            accuracy_score = classification_metric_train.accuracy_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.log_metric("accuracy_score", accuracy_score)
            mlflow.sklearn.log_model(model, "model")



    def _train_model(self, X_train:np.array, y_train:np.array, X_test:np.array, y_test:np.array)->ModelTrainerArtifact:
        try:
            models = {
                "LogisticRegression":LogisticRegression(verbose=1),
                "KNeighborsClassifier":KNeighborsClassifier(),
                "DecisionTreeClassifier":DecisionTreeClassifier(),
                "RandomForestClassifier":RandomForestClassifier(verbose=1),
                "AdaBoostClassifier":AdaBoostClassifier(),
                "GradientBoostingClassifier":GradientBoostingClassifier(verbose=1)
            }

            params = {
                "LogisticRegression": {
                    'penalty': ['l2'],
                    'C': [0.001, 0.01, 0.1, 1, 10],
                    'solver': ['lbfgs', 'liblinear'],
                    'max_iter': [500, 1000]
                },

                "KNeighborsClassifier": {
                    'n_neighbors': [3, 5, 7, 9],
                    'weights': ['uniform', 'distance'],
                    'algorithm': ['auto', 'ball_tree'],
                    'p': [1, 2]
                },

                "DecisionTreeClassifier": {
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [3, 5, 7, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                },

                "RandomForestClassifier": {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [None, 10, 20],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2],
                    'max_features': ['auto', 'sqrt', 'log2']
                },

                "AdaBoostClassifier": {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 1]
                },

                "GradientBoostingClassifier": {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 0.5],
                    'max_depth': [3, 5, 7, 11],
                    'min_samples_split': [2, 5],
                    'min_samples_leaf': [1, 2],
                    'subsample': [0.8, 0.9, 1.0],
                    'max_features': ['auto', 'sqrt']
                }
            }

            model_report = evaluate_models(X_train, y_train,
                                           X_test, y_test,
                                           models, params)

            ## to get the best model name from the report
            best_model_name = max(model_report, key=lambda x: model_report[x][1])
            best_model = models[best_model_name]
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            ## track the model and metrics on mlflow for both train and test data
            
            classification_metric_train = get_classification_score(y_train, y_train_pred)
            # self.__track_model_on_mlflow(best_model,classification_metric_train)
            classification_metric_test = get_classification_score(y_test, y_test_pred)
            self.__track_model_on_mlflow(best_model,classification_metric_test)


            _prerocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path= os.path.join(self.model_trainer_config.model_trainer_dir)
            os.makedirs(model_dir_path, exist_ok=True)
            model_file_path = os.path.join(model_dir_path, MODEL_FILE_NAME)

            network_security_model = NetworkSecurityModel(preprocessor=_prerocessor, model=best_model)
            save_object(model_file_path, network_security_model)

            save_object('final_model/model.pkl', best_model)
            save_object('final_model/preprocessor.pkl', _prerocessor)
            
            # model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=model_file_path,
                train_metircs_artifact=classification_metric_train,
                test_metircs_artifact=classification_metric_test
            )
            logger.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)
            X_train, y_train, X_test, y_test = train_array[:,:-1], train_array[:,-1], test_array[:,:-1], test_array[:,-1]

            model_trainer_artifact = self._train_model(X_train, y_train, X_test, y_test)

            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

