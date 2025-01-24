import sys
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import create_logger
from sklearn.metrics import f1_score, precision_score, recall_score
logger = create_logger(__name__)

def get_classification_score(y_true, y_pred)->ClassificationMetricArtifact:
    try:
        f1_score_value = f1_score(y_true, y_pred)
        precision_score_value = precision_score(y_true, y_pred)
        recall_score_value = recall_score(y_true, y_pred)

        classification_metric = ClassificationMetricArtifact(
            f1_score=f1_score_value,
            precision_score=precision_score_value,
            recall_score=recall_score_value)
        return classification_metric
    
    except Exception as e:
        raise NetworkSecurityException(e, sys.exc_info())
