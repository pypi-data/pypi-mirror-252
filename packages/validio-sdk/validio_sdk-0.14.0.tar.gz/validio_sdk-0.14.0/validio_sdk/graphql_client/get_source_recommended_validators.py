from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import (
    JsonFilterExpression,
    JsonTypeDefinition,
    SourceId,
    ValidatorId,
)

from .base_model import BaseModel
from .enums import (
    CategoricalDistributionMetric,
    NumericAnomalyMetric,
    NumericDistributionMetric,
    NumericMetric,
    RelativeTimeMetric,
    RelativeVolumeMetric,
    SourceState,
    ValidatorState,
    VolumeMetric,
)
from .fragments import ReferenceSourceConfigDetails, SegmentationSummary, TagDetails


class GetSourceRecommendedValidators(BaseModel):
    source: Optional["GetSourceRecommendedValidatorsSource"]


class GetSourceRecommendedValidatorsSource(BaseModel):
    state: SourceState
    recommended_validators: List[
        Annotated[
            Union[
                "GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidator",
                "GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidator",
                "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidator",
                "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidator",
                "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidator",
                "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidator",
                "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidator",
                "GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="recommendedValidators")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidator(BaseModel):
    typename__: Literal["FreshnessValidator", "SqlValidator", "Validator"] = Field(
        alias="__typename"
    )
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    state: ValidatorState
    progress: Optional[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorProgress"
    ]
    stats: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorStats"
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    source_config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    tags: List["GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorTags"]


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorProgress(
    BaseModel
):
    percentage: float
    processed: int
    total: int


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorStats(
    BaseModel
):
    last_artifact_at: Optional[datetime] = Field(alias="lastArtifactAt")
    last_incident_at: Optional[datetime] = Field(alias="lastIncidentAt")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorSourceConfig(
    BaseModel
):
    source: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorSourceConfigSource"
    segmentation: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorSourceConfigSegmentation(
    SegmentationSummary
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorTags(
    TagDetails
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidator(
    BaseModel
):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    state: ValidatorState
    progress: Optional[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorProgress"
    ]
    stats: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorStats"
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    source_config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    tags: List[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorTags"
    ]
    config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorConfig"
    reference_source_config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorReferenceSourceConfig" = Field(
        alias="referenceSourceConfig"
    )


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorProgress(
    BaseModel
):
    percentage: float
    processed: int
    total: int


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorStats(
    BaseModel
):
    last_artifact_at: Optional[datetime] = Field(alias="lastArtifactAt")
    last_incident_at: Optional[datetime] = Field(alias="lastIncidentAt")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorSourceConfig(
    BaseModel
):
    source: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorSourceConfigSource"
    segmentation: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorSourceConfigSegmentation(
    SegmentationSummary
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorTags(
    TagDetails
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorConfig(
    BaseModel
):
    categorical_distribution_metric: CategoricalDistributionMetric = Field(
        alias="categoricalDistributionMetric"
    )


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorReferenceSourceConfig(
    ReferenceSourceConfigDetails
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidator(
    BaseModel
):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    state: ValidatorState
    progress: Optional[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorProgress"
    ]
    stats: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorStats"
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    source_config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    tags: List[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorTags"
    ]
    config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorConfig"
    reference_source_config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorReferenceSourceConfig" = Field(
        alias="referenceSourceConfig"
    )


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorProgress(
    BaseModel
):
    percentage: float
    processed: int
    total: int


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorStats(
    BaseModel
):
    last_artifact_at: Optional[datetime] = Field(alias="lastArtifactAt")
    last_incident_at: Optional[datetime] = Field(alias="lastIncidentAt")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorSourceConfig(
    BaseModel
):
    source: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorSourceConfigSource"
    segmentation: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorSourceConfigSegmentation(
    SegmentationSummary
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorTags(
    TagDetails
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorConfig(
    BaseModel
):
    numeric_anomaly_metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorReferenceSourceConfig(
    ReferenceSourceConfigDetails
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidator(
    BaseModel
):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    state: ValidatorState
    progress: Optional[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorProgress"
    ]
    stats: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorStats"
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    source_config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    tags: List[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorTags"
    ]
    config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorConfig"
    reference_source_config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorReferenceSourceConfig" = Field(
        alias="referenceSourceConfig"
    )


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorProgress(
    BaseModel
):
    percentage: float
    processed: int
    total: int


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorStats(
    BaseModel
):
    last_artifact_at: Optional[datetime] = Field(alias="lastArtifactAt")
    last_incident_at: Optional[datetime] = Field(alias="lastIncidentAt")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorSourceConfig(
    BaseModel
):
    source: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorSourceConfigSource"
    segmentation: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorSourceConfigSegmentation(
    SegmentationSummary
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorTags(
    TagDetails
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorConfig(
    BaseModel
):
    distribution_metric: NumericDistributionMetric = Field(alias="distributionMetric")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorReferenceSourceConfig(
    ReferenceSourceConfigDetails
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidator(
    BaseModel
):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    state: ValidatorState
    progress: Optional[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorProgress"
    ]
    stats: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorStats"
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    source_config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    tags: List[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorTags"
    ]
    config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorConfig"


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorProgress(
    BaseModel
):
    percentage: float
    processed: int
    total: int


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorStats(
    BaseModel
):
    last_artifact_at: Optional[datetime] = Field(alias="lastArtifactAt")
    last_incident_at: Optional[datetime] = Field(alias="lastIncidentAt")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorSourceConfig(
    BaseModel
):
    source: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorSourceConfigSource"
    segmentation: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorSourceConfigSegmentation(
    SegmentationSummary
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorTags(
    TagDetails
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorConfig(
    BaseModel
):
    metric: NumericMetric


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidator(
    BaseModel
):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    state: ValidatorState
    progress: Optional[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorProgress"
    ]
    stats: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorStats"
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    source_config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    tags: List[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorTags"
    ]
    config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorConfig"


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorProgress(
    BaseModel
):
    percentage: float
    processed: int
    total: int


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorStats(
    BaseModel
):
    last_artifact_at: Optional[datetime] = Field(alias="lastArtifactAt")
    last_incident_at: Optional[datetime] = Field(alias="lastIncidentAt")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorSourceConfig(
    BaseModel
):
    source: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorSourceConfigSource"
    segmentation: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorSourceConfigSegmentation(
    SegmentationSummary
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorTags(
    TagDetails
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorConfig(
    BaseModel
):
    relative_time_metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidator(
    BaseModel
):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    state: ValidatorState
    progress: Optional[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorProgress"
    ]
    stats: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorStats"
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    source_config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    tags: List[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorTags"
    ]
    config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorConfig"
    reference_source_config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorReferenceSourceConfig" = Field(
        alias="referenceSourceConfig"
    )


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorProgress(
    BaseModel
):
    percentage: float
    processed: int
    total: int


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorStats(
    BaseModel
):
    last_artifact_at: Optional[datetime] = Field(alias="lastArtifactAt")
    last_incident_at: Optional[datetime] = Field(alias="lastIncidentAt")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorSourceConfig(
    BaseModel
):
    source: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorSourceConfigSource"
    segmentation: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorSourceConfigSegmentation(
    SegmentationSummary
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorTags(
    TagDetails
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorConfig(
    BaseModel
):
    relative_volume_metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorReferenceSourceConfig(
    ReferenceSourceConfigDetails
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidator(
    BaseModel
):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    state: ValidatorState
    progress: Optional[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorProgress"
    ]
    stats: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorStats"
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    source_config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    tags: List[
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorTags"
    ]
    config: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorConfig"


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorProgress(
    BaseModel
):
    percentage: float
    processed: int
    total: int


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorStats(
    BaseModel
):
    last_artifact_at: Optional[datetime] = Field(alias="lastArtifactAt")
    last_incident_at: Optional[datetime] = Field(alias="lastIncidentAt")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorSourceConfig(
    BaseModel
):
    source: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorSourceConfigSource"
    segmentation: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorSourceConfigSegmentation(
    SegmentationSummary
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorTags(
    TagDetails
):
    pass


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorConfig(
    BaseModel
):
    volume_metric: VolumeMetric = Field(alias="volumeMetric")


GetSourceRecommendedValidators.model_rebuild()
GetSourceRecommendedValidatorsSource.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidator.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorProgress.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorStats.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorSourceConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorSourceConfigSource.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorSourceConfigSegmentation.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsValidatorTags.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidator.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorProgress.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorStats.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorSourceConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorTags.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidator.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorProgress.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorStats.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorSourceConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorSourceConfigSource.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorTags.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidator.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorProgress.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorStats.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorSourceConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorSourceConfigSource.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorTags.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidator.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorProgress.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorStats.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorSourceConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorSourceConfigSource.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorSourceConfigSegmentation.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorTags.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsNumericValidatorConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidator.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorProgress.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorStats.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorSourceConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorSourceConfigSource.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorTags.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeTimeValidatorConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidator.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorProgress.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorStats.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorSourceConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorSourceConfigSource.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorTags.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidator.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorProgress.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorStats.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorSourceConfig.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorSourceConfigSource.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorTags.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsVolumeValidatorConfig.model_rebuild()
