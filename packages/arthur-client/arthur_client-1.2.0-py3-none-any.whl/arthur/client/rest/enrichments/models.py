# generated by datamodel-codegen:
#   filename:  enrichments.yaml
#   timestamp: 2024-01-19T17:36:03+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from arthur.client.rest.common.models import Page, PageSize, TotalCount, TotalPages
from arthur.client.types import ByteField
from pydantic import BaseModel, Extra, Field


class Status(str, Enum):
    """
    The enrichment pipeline status
    """

    Disabled = 'Disabled'
    Pending = 'Pending'
    Training = 'Training'
    Ready = 'Ready'
    Failed = 'Failed'


class EnrichmentStatus(BaseModel):
    status: Optional[Status] = Field(None, example='Disabled')
    """
    The enrichment pipeline status
    """


class AnomalyDetectionEnrichmentConfiguration(BaseModel):
    enabled: bool
    """
    Whether or not the enrichment is enabled
    """


class BiasMitigationEnrichmentConfiguration(AnomalyDetectionEnrichmentConfiguration):
    pass


class ExplanationAlgo(str, Enum):
    """
    Explainability algorithm to use in the model server. Current options are "lime" or "shap", default is "lime"
    """

    LIME = 'lime'
    SHAP = 'shap'


class Config(BaseModel):
    python_version: Optional[str] = Field(None, example='3.8.17')
    """
    Python version number user project users
    """
    sdk_version: Optional[str] = Field(None, example='3.26.0')
    """
    SDK version number user project uses
    """
    streaming_explainability_enabled: Optional[bool] = Field(None, example=True)
    """
    Set to true if explainability should be calculated for all inferences in a streaming manner and set to false if explainability should only be calculated when requested.
    """
    user_predict_function_import_path: Optional[str] = Field(
        None, example='path/to/import/function.py'
    )
    """
    Import path of the user model predict function in the project directory
    """
    shap_expected_values: Optional[List[float]] = Field(None, example=[1, 2, 3])
    """
    If using SHAP, these are the expected values generated when the explainer is created
    """
    model_server_cpu: Optional[str] = Field('2', example='2')
    """
    Number of cpus to assign to explanation server.
    """
    model_server_memory: Optional[str] = Field('1500Mi', example='1Gi')
    """
    Amount of memory to assign explanation server in the format xMi or xGi.
    """
    model_server_max_replicas: Optional[int] = Field(30, example=30)
    """
    Max number of model server instances.
    """
    explanation_nsamples: Optional[int] = Field(2000, example=2000)
    """
    Explainability algorithms create sample data points when explaining inferences. The number of samples created per explanation can be configured here. There is a trade off between accuracy and computing power and time for this configuration.
    """
    explanation_algo: Optional[ExplanationAlgo] = Field('lime', example='lime')
    """
    Explainability algorithm to use in the model server. Current options are "lime" or "shap", default is "lime"
    """
    inference_consumer_cpu: Optional[str] = Field('500m', example='500m')
    """
    Number of cpus to assign to the inference reader
    """
    inference_consumer_memory: Optional[str] = Field('512Mi', example='512Mi')
    """
    Amount of memory to assign to the inference reader in the format xMi or xGi.
    """
    inference_consumer_score_percent: Optional[float] = Field(1.0, example=0.1)
    """
    Sampling rate for inferences to explain
    """
    inference_consumer_thread_pool_size: Optional[int] = Field(5, example=5)
    """
    Number of threads in the inference consumer pool
    """


class ExplainabilityEnrichmentConfiguration(BaseModel):
    """
    JSON-formatted configuration options for the Explainability Enrichment. See the ExplainabilityEnrichmentConfiguration for schema.
    """

    enabled: Optional[bool] = Field(None, example=True)
    """
    Whether or not the enrichment is enabled
    """
    config: Optional[Config] = None


class HotspotsEnrichmentConfiguration(AnomalyDetectionEnrichmentConfiguration):
    pass


class EnrichmentsConfiguration(BaseModel):
    """
    A JSON-formatted enrichments configuration. See the EnrichmentsConfiguration object for schema
    """

    anomaly_detection: Optional[AnomalyDetectionEnrichmentConfiguration] = None
    bias_mitigation: Optional[BiasMitigationEnrichmentConfiguration] = None
    hotspots: Optional[HotspotsEnrichmentConfiguration] = None
    explainability: Optional[ExplainabilityEnrichmentConfiguration] = None


class AnomalyDetectionEnrichmentResponse(
    AnomalyDetectionEnrichmentConfiguration, EnrichmentStatus
):
    """
    The response object containing configuration and status of an on-by-default enrichment.
    """

    pass


class BiasMitigationEnrichmentResponse(
    BiasMitigationEnrichmentConfiguration, EnrichmentStatus
):
    """
    The response object containing configuration and status of an on-by-default enrichment.
    """

    pass


class ExplainabilityEnrichmentResponse(
    ExplainabilityEnrichmentConfiguration, EnrichmentStatus
):
    """
    The response object containing configuration and status of the explainability enrichment.
    """

    pass


class HotspotsEnrichmentResponse(HotspotsEnrichmentConfiguration, EnrichmentStatus):
    """
    The response object containing configuration and status of an on-by-default enrichment.
    """

    pass


class EnrichmentsResponse(BaseModel):
    """
    The response object containing configuration and status of all enrichments.
    """

    anomaly_detection: Optional[AnomalyDetectionEnrichmentResponse] = None
    bias_mitigation: Optional[BiasMitigationEnrichmentResponse] = None
    hotspots: Optional[HotspotsEnrichmentResponse] = None
    explainability: Optional[ExplainabilityEnrichmentResponse] = None


class ExplainabilityEnrichmentRequest(BaseModel):
    """
    Configures explainability. A multipart/form-data body with at least a `configuration` JSON body. If explainability is being enabled for the first time, artifacts must be supplied.
    """

    config: Optional[ExplainabilityEnrichmentConfiguration] = None
    """
    Explainability enrichment configuration
    """


class EnrichmentsRequest(BaseModel):
    """
    Configures multiple enrichments. A multipart/form-data body with at least a `configuration` JSON body. If explainability is being enabled for the first time, artifacts must be supplied.
    """

    config: Optional[EnrichmentsConfiguration] = None
    """
    Enrichments configuration
    """


class ExplanationValuesWhatIf(BaseModel):
    attribute_name: str = Field(..., example='feature_a')
    explanation_value: float = Field(..., example=0.12)


class FindHotspotsNode(BaseModel):
    left: Optional[FindHotspotsNode] = None
    right: Optional[FindHotspotsNode] = None
    rules: Dict[str, Any]
    """
    rules for the split on this node
    """
    gt_to_info: Optional[Dict[str, Any]] = None
    """
    info around ground truths at this node
    """
    precision: Optional[float] = None
    """
    precision for this node
    """
    recall: Optional[float] = None
    """
    recall for this node
    """
    f1: Optional[float] = None
    """
    f1 for this node
    """
    accuracy: float
    """
    accuracy for this node
    """
    impurity: float
    """
    impurity for this node
    """
    n_samples: int
    """
    n_samples used for this node
    """
    feature: str
    """
    name of feature this node was cut on
    """
    cutoff: Optional[float] = None
    """
    the cutoff for the node
    """


class ExpectedValues(BaseModel):
    predicted_attribute_name: str = Field(..., example='feature_a')
    expected_value: float = Field(..., example=0.12)


class TokenObject(BaseModel):
    token: str = Field(..., example='dog')
    """
    Token string which is generated from separating the input text by the model's given delimiter.
    """
    position: float = Field(..., example=0)
    """
    Integer representing the location of the token in the input text. 0 refers to the the first token in the input text.
    """
    explanation_value: float = Field(..., example=0.48)
    """
    Float explanation value for the specific token.
    """


class FindHotspotsResponse(BaseModel):
    data: List[FindHotspotsNode]
    """
    Contains all hotspots based on input
    """


class ExplanationInput(BaseModel):
    class Config:
        extra = Extra.allow

    __root__: Optional[Dict[str, Dict[str, Any]]] = None


class ExplanationValuesOnDemand(BaseModel):
    attribute_name: str = Field(..., example='feature_a')
    explanation_value: Optional[float] = Field(None, example=0.12)
    tokens: Optional[List[TokenObject]] = None
    """
    Only valid for NLP models, represents the list of tokens locations and explanation values
    """


class WhatIfAttributeRequest(BaseModel):
    """
    Attribute object for inference to be sent to what-if
    """

    attribute_name: str = Field(..., example='feature_a')
    attribute_value: Union[float, str, bool] = Field(..., example=1.0)


class ExplainabilityEnrichmentArtifacts(BaseModel):
    """
    Artifacts for enrichments
    """

    class Config:
        arbitrary_types_allowed = True

    user_project_zip: Optional[ByteField] = Field(None, alias='user_project.zip')
    """
    Zipped folder of model predict function and code dependencies
    """
    user_requirements_file_txt: Optional[ByteField] = Field(
        None, alias='user_requirements_file.txt'
    )
    """
    Text file containing python dependencies the project folder requires
    """
    explainer_pkl: Optional[ByteField] = Field(None, alias='explainer.pkl')
    """
    Serialized LIME or SHAP explainer object
    """


class WhatIfRequest(BaseModel):
    """
    Inference model pipeline input to get explanation for
    """

    model_pipeline_input: List[WhatIfAttributeRequest]


class EnrichmentStatusUpdate(EnrichmentStatus):
    """
    Updates status for an enrichment. A body with at least a `status` key.
    """

    status: Status = Field(..., example='Disabled')
    """
    The enrichment pipeline status
    """


class EnrichmentName(str, Enum):
    """
    Name of enrichment.
    """

    explainability = 'explainability'
    anomaly_detection = 'anomaly_detection'
    bias_mitigation = 'bias_mitigation'
    hotspots = 'hotspots'


class ExplanationsWhatIf(BaseModel):
    algorithm: str = Field(..., example='shap')
    predicted_attribute_name: str = Field(..., example='class_a')
    importance_scores: List[ExplanationValuesWhatIf]


class BiasMitigationDataPoints(BaseModel):
    x: float = Field(..., example=0.78)
    """
    x-coordinate of the point on the curve.
    """
    y: float = Field(..., example=0.28)
    """
    y-coordinate of the point on the curve.
    """
    threshold: float = Field(..., example=0.8)
    """
    Threshold associated with specific point on the curve.
    """


class ExplanationsOnDemand(BaseModel):
    algorithm: str = Field(..., example='shap')
    predicted_attribute_name: str = Field(..., example='class_a')
    importance_scores: List[ExplanationValuesOnDemand]


class BiasConstraintEnum(str, Enum):
    DemographicParity = 'demographic_parity'
    EqualOpportunity = 'equal_opportunity'
    EqualizedOdds = 'equalized_odds'


class BiasMitigationCurveResponse(BaseModel):
    id: str = Field(..., example='418c6939-8765-40fa-b04e-11ba57b7f21c')
    """
    UUID of the bias mitigation curve.
    """
    attribute_id: str = Field(..., example='418c6939-8765-40fa-b04e-11ba57b7f21c')
    """
    UUID of the attribute which the curve is associated with.
    """
    attribute_name: Optional[str] = Field(None, example='Gender')
    """
    Name of the attribute which the curve is associated with.
    """
    categorical_value: Optional[str] = Field(None, example='Male')
    """
    Categorical attribute value which the curve is associated with.
    """
    continuous_start: Optional[str] = Field(None, example='18')
    """
    Start of the range in which the curve is associated with for continuous attributes. Will only exist for continuous attributes and will always have a corresponding continuous_end. A none value denotes an open bound.
    """
    continuous_end: Optional[str] = Field(None, example='65')
    """
    End of the range in which the curve is associated with for continuous attributes. Will only exist for continuous attributes and will always have a corresponding continuous_end. A none value denotes an open bound.
    """
    constraint: str = Field(..., example='Demographic Parity')
    """
    Constraint value which the curve is associated with.
    """
    x_label: str = Field(..., example='Selection Rate')
    """
    X axis label of the curve, derived from constraint type.
    """
    y_label: str = Field(..., example='Accuracy')
    """
    Y axis label of the curve, derived from constraint type.
    """
    optimization_index: int
    """
    Index of the curve point which is most optimized according to the constraint.
    """
    data_points: List[BiasMitigationDataPoints]
    """
    Timestamp the file was last updated in the Arthur platform.
    """
    model_id: str
    """
    The UUID of the model with bias mitigation curves.
    """


class ExplainabilityResultOnDemand(BaseModel):
    explanation: List[ExplanationsOnDemand]
    expected_value: Optional[List[ExpectedValues]] = None


class ExplainabilityResultWhatIf(BaseModel):
    predicted_values: List[WhatIfAttributeRequest]
    explanation: List[ExplanationsWhatIf]
    expected_value: List[ExpectedValues]


class ExplainabilityEnrichmentMultipartRequestBody(ExplainabilityEnrichmentArtifacts):
    """
    When setting up explainability, a config must always be provided. The explainability enrichment artifact files may be provided all together, but a config must be provided as well, regardless of whether the config has already been set.
    """

    config: Optional[ExplainabilityEnrichmentConfiguration] = None


class PaginatedBiasMitigationCurves(BaseModel):
    data: List[BiasMitigationCurveResponse]
    """
    List of bias mitigation curves.
    """
    page: Page
    page_size: PageSize
    total_pages: TotalPages
    total_count: TotalCount


FindHotspotsNode.update_forward_refs()
