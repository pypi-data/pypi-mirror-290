from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, List, Optional, Union
from uuid import UUID

import yaml
from pydantic import ConfigDict, Field, field_validator
from typing_extensions import Annotated

from ..core import HLBaseModel
from .gql_client import HLClient

__all__ = [
    "find_or_create_evaluation_metric",
    "create_evaluation_metric_result",
    "EvaluationMetricCodeEnum",
    "EvaluationMetricResult",
    "EvaluationMetric",
]


class EvaluationMetricCodeEnum(str, Enum):
    Dice = "Dice"
    mAP = "mAP"
    MaAD = "MaAD"
    MeAD = "MeAD"
    Other = "Other"
    AP = "AP"


class EvaluationMetric(HLBaseModel):
    model_config = ConfigDict(use_enum_values=True)

    chart: Optional[str] = None
    code: EvaluationMetricCodeEnum
    description: Optional[str] = None
    id: int
    iou: Optional[float] = None
    name: str
    object_class_uuid: Optional[Union[UUID, str]] = None
    weighted: Optional[bool] = False

    def dict(self, *args, **kwargs):
        d = super().model_dump(*args, **kwargs)
        if "object_class_uuid" in d:
            d["object_class_uuid"] = str(d["object_class_uuid"])
        return d


class EvaluationMetricResult(HLBaseModel, extra="forbid"):
    experiment_id: Optional[int] = None
    research_plan_metric_id: int
    result: float
    object_class_id: Optional[int] = None
    object_class_uuid: Optional[Union[UUID, str]] = None

    # iso datetime str will be generated at instantiation
    # if not supplied manually.
    occured_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def from_yaml(cls, path: Union[Path, str]):
        path = Path(path)
        with path.open("r") as f:
            data = yaml.safe_load(f)
        return cls(**data)


def get_existing_evaluation_metrics(client: HLClient, evaluation_id: int):
    class QueryReturnType(HLBaseModel):
        research_plan_metrics: List[EvaluationMetric]

    query_return_type: QueryReturnType = client.researchPlan(return_type=QueryReturnType, id=evaluation_id)

    return query_return_type.research_plan_metrics


def find_or_create_evaluation_metric(
    client: HLClient,
    evaluation_id: int,
    code: Union[EvaluationMetricCodeEnum, str],
    name: str,
    description: Optional[str] = None,
    iou: Optional[float] = None,
    weighted: Optional[bool] = False,
    object_class_uuid: Optional[Union[UUID, str]] = None,
) -> EvaluationMetric:
    existing_evaluation_metrics = {r.name: r for r in get_existing_evaluation_metrics(client, evaluation_id)}

    if name in existing_evaluation_metrics:
        return existing_evaluation_metrics[name]
    else:
        # ToDo: Have the GQL accept s uuid not an id
        if isinstance(object_class_uuid, UUID):
            object_class_uuid = str(object_class_uuid)

        code = EvaluationMetricCodeEnum(code) if isinstance(code, str) else code

        class CreateResearchPlanMetricReturnType(HLBaseModel):
            errors: Any = None
            research_plan_metric: Optional[EvaluationMetric] = None

        kwargs = EvaluationMetric(
            id=-1,
            code=code,
            name=name,
            description=description,
            iou=iou,
            weighted=weighted,
            object_class_uuid=object_class_uuid,
        ).dict(exclude_none=True)
        _ = kwargs.pop("id")
        kwargs["researchPlanId"] = evaluation_id

        result = client.createResearchPlanMetric(
            return_type=CreateResearchPlanMetricReturnType, **kwargs
        ).research_plan_metric
        assert result is not None
        return result


def create_evaluation_metric_result(
    client: HLClient,
    evaluation_id: int,
    result: float,
    object_class_uuid: Optional[UUID] = None,
    evaluation_metric_id: Optional[int] = None,
    evaluation_metric_name: Optional[str] = None,
    occured_at: Optional[Union[datetime, str]] = None,
    baseline_dataset_id: Optional[int] = None,
    comparison_dataset_id: Optional[int] = None,
    overlap_threshold: Optional[Annotated[float, Field(ge=0, le=1)]] = None,  # type: ignore
    entity_attribute_id: Optional[UUID] = None,
    experiment_id: Optional[int] = None,
    training_run_id: Optional[int] = None,
):
    if occured_at is None:
        occured_at = datetime.now()
    elif isinstance(occured_at, str):
        occured_at = datetime.fromisoformat(occured_at)

    if evaluation_metric_id is None:
        assert evaluation_metric_name is not None
        existing_evaluation_metrics = {
            e.name: e for e in get_existing_evaluation_metrics(client, evaluation_id)
        }
        evaluation_metric = existing_evaluation_metrics.get(evaluation_metric_name, None)
        if evaluation_metric is None:
            raise KeyError(
                f"Evaluation Metric '{evaluation_metric_name}' not in evaluation {evaluation_id}. Got: {existing_evaluation_metrics}"
            )
        evaluation_metric_id = evaluation_metric.id

    class CreateEvaluationMetricPayload(HLBaseModel):
        research_plan_metric_id: int
        experiment_id: Optional[int] = None
        training_run_id: Optional[int] = None
        occured_at: datetime
        result: float
        object_class_uuid: Optional[Union[UUID, str]] = None
        baseline_dataset_id: Optional[int] = None
        comparison_dataset_id: Optional[int] = None
        overlap_threshold: Optional[Annotated[float, Field(ge=0, le=1)]] = None  # type: ignore
        entity_attribute_id: Optional[Union[UUID, str]] = None

        @field_validator("object_class_uuid", "entity_attribute_id")
        @classmethod
        def validate_uuid(cls, v):
            if v is None:
                return v
            if isinstance(v, UUID):
                return str(v)
            try:
                uuid_obj = UUID(v)
            except ValueError:
                raise ValueError("Invalid UUID")
            return str(uuid_obj)

    kwargs = CreateEvaluationMetricPayload(
        research_plan_metric_id=evaluation_metric_id,
        experiment_id=experiment_id,
        training_run_id=training_run_id,
        occured_at=occured_at,
        result=result,
        object_class_uuid=object_class_uuid,
        baseline_dataset_id=baseline_dataset_id,
        comparison_dataset_id=comparison_dataset_id,
        overlap_threshold=overlap_threshold,
        entity_attribute_id=entity_attribute_id,
    ).gql_dict()

    kwargs["occuredAt"] = kwargs["occuredAt"].isoformat()

    class CreateExperimentResultReturnType(HLBaseModel):
        errors: Any = None
        experiment_result: Optional[EvaluationMetricResult] = None

    _result: CreateExperimentResultReturnType = client.createExperimentResult(
        return_type=CreateExperimentResultReturnType, **kwargs
    )

    if _result.errors:
        raise ValueError(f"Errors: {result}")

    return _result.experiment_result
