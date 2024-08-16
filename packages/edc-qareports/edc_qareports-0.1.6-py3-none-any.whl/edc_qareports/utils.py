from pathlib import Path

from django.apps import apps as django_apps
from django.conf import settings
from edc_auth.get_app_codenames import get_app_codenames

from .model_mixins import qa_reports_permissions


def read_unmanaged_model_sql(
    filename: str | None = None,
    app_name: str | None = None,
    fullpath: str | Path | None = None,
) -> str:
    """Wait, use DBView instead!!"""
    uuid_func = "uuid()"
    if settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
        uuid_func = "gen_random_uuid()"

    if not fullpath:
        fullpath = Path(settings.BASE_DIR) / app_name / "models" / "unmanaged" / filename
    else:
        fullpath = Path(fullpath)

    parsed_sql = []
    with fullpath.open("r") as f:
        for line in f:
            line = line.split("#", maxsplit=1)[0]
            line = line.split("-- ", maxsplit=1)[0]
            line = line.replace("\n", "")
            line = line.strip()
            if line:
                parsed_sql.append(line)

    sql = " ".join(parsed_sql)
    return sql.replace("uuid()", uuid_func)


def truncate_string(string: str, max_length: int) -> str:
    """Strips string of leading/trailing whitespace and truncates
    if > `max_length`.
    """
    string = string.strip()
    if len(string) > max_length:
        return string[: max_length - 1].strip() + "…"
    return string


def get_qareports_codenames(app_name: str, *note_models: str) -> list[str]:
    reports_codenames = []
    effect_reports = django_apps.get_app_config(app_name)
    report_models = [m._meta.label_lower for m in effect_reports.get_models()]
    for codename in get_app_codenames(
        app_name,
        permissions=qa_reports_permissions,
        exclude_models=note_models,
    ):
        reports_codenames.append(codename)
    exclude_models = [m for m in report_models if m not in note_models]
    reports_codenames.extend(
        [c for c in get_app_codenames(app_name, exclude_models=exclude_models)]
    )
    return list(set(reports_codenames))
