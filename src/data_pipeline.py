"""Data ingestion, normalization, and quality checks for job matching data."""

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from src.models import ExperienceLevel, Opportunity, Seeker, WorkMode, WorkType


@dataclass
class DataQualityReport:
    """Counts and warnings produced while loading a dataset."""

    source: str
    records_loaded: int = 0
    duplicate_keys: List[str] = field(default_factory=list)
    missing_fields: Dict[str, int] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "records_loaded": self.records_loaded,
            "duplicate_keys": self.duplicate_keys,
            "missing_fields": self.missing_fields,
            "warnings": self.warnings,
        }


def _load_collection(path: str, collection_key: str) -> Tuple[List[Dict[str, Any]], DataQualityReport]:
    """Load a JSON collection and retain basic quality metadata."""
    source = str(Path(path))
    report = DataQualityReport(source=source)
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    records = payload.get(collection_key, payload) if isinstance(payload, dict) else payload
    if not isinstance(records, list):
        raise ValueError(f"Expected a list under '{collection_key}' in {path}")

    report.records_loaded = len(records)
    return records, report


def _count_missing(records: Iterable[Dict[str, Any]], fields: Sequence[str], report: DataQualityReport) -> None:
    for field_name in fields:
        count = sum(1 for record in records if record.get(field_name) in (None, "", []))
        if count:
            report.missing_fields[field_name] = count


def _deduplicate(records: Iterable[Dict[str, Any]], key_field: str, report: DataQualityReport) -> List[Dict[str, Any]]:
    unique: Dict[str, Dict[str, Any]] = {}
    for record in records:
        key = str(record.get(key_field, "")).strip().lower()
        if not key:
            report.warnings.append(f"Record is missing identifier '{key_field}'")
            continue
        if key in unique:
            report.duplicate_keys.append(key)
        unique[key] = record
    return list(unique.values())


def _enum_value(enum_type: Any, value: Any, default: Any) -> Any:
    if isinstance(value, enum_type):
        return value
    try:
        return enum_type(str(value).strip().lower())
    except (ValueError, TypeError):
        return default


def load_seekers(path: str) -> Tuple[List[Seeker], DataQualityReport]:
    """Load, validate, normalize, and convert seeker records."""
    records, report = _load_collection(path, "seekers")
    _count_missing(records, ["name", "skills", "career_goals", "experience_level"], report)
    records = _deduplicate(records, "name", report)

    seekers: List[Seeker] = []
    for record in records:
        salary = record.get("salary_expectation") or {}
        seekers.append(
            Seeker(
                name=str(record.get("name", "Unnamed seeker")).strip(),
                email=record.get("email"),
                phone=record.get("phone"),
                career_goals=record.get("career_goals") or [],
                industry_interests=record.get("industry_interests") or [],
                experience_level=_enum_value(ExperienceLevel, record.get("experience_level"), ExperienceLevel.JUNIOR),
                skills=record.get("skills") or [],
                certifications=record.get("certifications") or [],
                education=record.get("education") or "",
                preferred_locations=record.get("preferred_locations") or [],
                willing_to_relocate=bool(record.get("willing_to_relocate", False)),
                work_mode_preference=[_enum_value(WorkMode, mode, WorkMode.ONSITE) for mode in record.get("work_mode_preference", [])],
                work_type_preference=[_enum_value(WorkType, kind, WorkType.FULL_TIME) for kind in record.get("work_type_preference", [])],
                salary_expectation_min=salary.get("min"),
                salary_expectation_max=salary.get("max"),
                availability_days=record.get("availability_days"),
            )
        )
    report.records_loaded = len(seekers)
    return seekers, report


def load_opportunities(path: str) -> Tuple[List[Opportunity], DataQualityReport]:
    """Load, validate, normalize, and convert opportunity records."""
    records, report = _load_collection(path, "opportunities")
    _count_missing(records, ["job_id", "title", "required_skills", "experience_level_required"], report)
    records = _deduplicate(records, "job_id", report)

    opportunities: List[Opportunity] = []
    for record in records:
        salary = record.get("salary") or {}
        opportunities.append(
            Opportunity(
                job_id=str(record.get("job_id", "UNKNOWN")).strip(),
                title=str(record.get("title", "Untitled role")).strip(),
                company=str(record.get("company", "Unknown company")).strip(),
                description=record.get("description"),
                responsibilities=record.get("responsibilities") or [],
                required_skills=record.get("required_skills") or [],
                preferred_skills=record.get("preferred_skills") or [],
                experience_level_required=_enum_value(ExperienceLevel, record.get("experience_level_required"), ExperienceLevel.JUNIOR),
                experience_years_required=int(record.get("experience_years_required") or 0),
                education_required=record.get("education_required"),
                certifications_required=record.get("certifications_required") or [],
                locations=record.get("locations") or [],
                allows_relocation=bool(record.get("allows_relocation", False)),
                work_mode=_enum_value(WorkMode, record.get("work_mode"), WorkMode.ONSITE),
                work_type=_enum_value(WorkType, record.get("work_type"), WorkType.FULL_TIME),
                salary_min=salary.get("min"),
                salary_max=salary.get("max"),
                benefits=record.get("benefits") or [],
                posted_date=record.get("posted_date"),
                application_deadline=record.get("application_deadline"),
            )
        )
    report.records_loaded = len(opportunities)
    return opportunities, report


def load_dataset(seekers_path: str, opportunities_path: str) -> Tuple[List[Seeker], List[Opportunity], Dict[str, Any]]:
    """Load both collections and return typed records plus quality reports."""
    seekers, seeker_report = load_seekers(seekers_path)
    opportunities, opportunity_report = load_opportunities(opportunities_path)
    return seekers, opportunities, {
        "seekers": seeker_report.to_dict(),
        "opportunities": opportunity_report.to_dict(),
    }
