from io import StringIO
from datetime import datetime, timezone
from typing import Dict


import pandas as pd
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI(title="CSV Column Type Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DashboardMeta(BaseModel):
    rows: int
    columns: int
    generated_at: str


class DashboardSummaryItem(BaseModel):
    title: str
    value: float


class DashboardChart(BaseModel):
    chart_type: str
    columns: list[str]
    reason: str


class DashboardAnomalyItem(BaseModel):
    column: str
    count: int


class DashboardResponse(BaseModel):
    meta: DashboardMeta
    summary: list[DashboardSummaryItem]
    charts: list[DashboardChart]
    insights: list[str]
    anomalies: list[DashboardAnomalyItem]


def detect_column_type(series: pd.Series) -> str:
    clean = series.dropna()
    if clean.empty:
        return "text"

    if pd.api.types.is_numeric_dtype(clean):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(clean):
        return "date"

    as_str = clean.astype(str)

    parsed_dates = pd.to_datetime(as_str, errors="coerce")
    if parsed_dates.notna().mean() >= 0.8:
        return "date"

    parsed_numbers = pd.to_numeric(as_str, errors="coerce")
    if parsed_numbers.notna().mean() >= 0.8:
        return "numeric"

    unique_count = as_str.nunique(dropna=True)
    total_count = len(as_str)
    avg_length = as_str.str.len().mean()

    max_categorical_unique = min(50, max(2, int(total_count * 0.2)))
    if unique_count <= max_categorical_unique and avg_length <= 40:
        return "categorical"

    return "text"


def detect_types_from_csv_text(csv_text: str) -> Dict[str, Dict[str, str]]:
    dataframe = parse_csv_text(csv_text)

    detected_types = {
        column: detect_column_type(dataframe[column]) for column in dataframe.columns
    }
    return {"column_types": detected_types}


def parse_csv_text(csv_text: str) -> pd.DataFrame:
    try:
        return pd.read_csv(StringIO(csv_text))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid CSV content: {exc}")


def build_data_audit(dataframe: pd.DataFrame) -> Dict[str, object]:
    missing_values_per_column = {
        column: int(count)
        for column, count in dataframe.isna().sum().to_dict().items()
    }
    duplicate_rows = int(dataframe.duplicated().sum())
    total_cells = int(dataframe.shape[0] * dataframe.shape[1])
    missing_cells = int(dataframe.isna().sum().sum())

    if total_cells == 0:
        completeness = 0.0
    else:
        completeness = (total_cells - missing_cells) / total_cells

    health_score = round(completeness * 100, 2)
    return {
        "missing_values_per_column": missing_values_per_column,
        "duplicate_rows_count": duplicate_rows,
        "health_score": health_score,
    }


def build_anomaly_report(dataframe: pd.DataFrame) -> Dict[str, Dict[str, object]]:
    anomalies: Dict[str, Dict[str, object]] = {}

    for column in dataframe.columns:
        numeric_series = pd.to_numeric(dataframe[column], errors="coerce")
        valid = numeric_series.dropna()
        if valid.empty:
            continue

        mean_value = float(valid.mean())
        std_dev = float(valid.std(ddof=0))
        threshold = mean_value + (2 * std_dev)
        anomaly_mask = numeric_series > threshold

        anomaly_indices = anomaly_mask[anomaly_mask].index.tolist()
        anomaly_values = [float(v) for v in numeric_series[anomaly_mask].tolist()]

        anomalies[column] = {
            "mean": round(mean_value, 4),
            "std_dev": round(std_dev, 4),
            "threshold": round(threshold, 4),
            "anomaly_count": len(anomaly_values),
            "anomaly_indices": anomaly_indices,
            "anomaly_values": [round(v, 4) for v in anomaly_values],
        }

    return anomalies


def build_insights(
    dataframe: pd.DataFrame,
    audit: Dict[str, object],
    stats: Dict[str, Dict[str, float]],
    anomalies: Dict[str, Dict[str, object]],
) -> list[str]:
    insights: list[str] = []

    missing_per_column = audit.get("missing_values_per_column", {})
    row_count = max(int(dataframe.shape[0]), 1)

    # Missing data insight: flag columns with >= 20% missing values.
    for column, missing_count in missing_per_column.items():
        missing_ratio = float(missing_count) / row_count
        if missing_ratio >= 0.2:
            insights.append(
                f"High missing data in '{column}': {missing_count} missing values ({round(missing_ratio * 100, 2)}%)."
            )

    # Variability insight: coefficient of variation >= 1.0 suggests high spread.
    for column, metrics in stats.items():
        mean_value = float(metrics.get("mean", 0.0))
        max_value = float(metrics.get("max", 0.0))
        min_value = float(metrics.get("min", 0.0))
        spread = max_value - min_value
        if mean_value > 0 and spread / mean_value >= 1.0:
            insights.append(
                f"High variability in numeric column '{column}' (range {round(spread, 4)} vs mean {round(mean_value, 4)})."
            )

    # Anomaly insight: mention columns with detected outliers.
    for column, report in anomalies.items():
        anomaly_count = int(report.get("anomaly_count", 0))
        threshold = report.get("threshold")
        if anomaly_count > 0:
            insights.append(
                f"Detected {anomaly_count} anomalies in '{column}' above threshold {threshold}."
            )

    # Dominant categorical pattern: low-cardinality column with a dominant mode.
    for column in dataframe.columns:
        series = dataframe[column].dropna()
        if series.empty:
            continue

        as_str = series.astype(str)
        unique_count = as_str.nunique()
        if unique_count <= 10:
            mode = as_str.mode()
            if not mode.empty:
                dominant_value = mode.iloc[0]
                dominant_ratio = float((as_str == dominant_value).mean())
                if dominant_ratio >= 0.5:
                    insights.append(
                        f"Categorical pattern in '{column}': '{dominant_value}' appears in {round(dominant_ratio * 100, 2)}% of non-null rows."
                    )

    if not insights:
        insights.append("No major data quality or distribution issues detected.")

    return insights


def build_chart_suggestions(column_types: Dict[str, str]) -> list[Dict[str, object]]:
    suggestions: list[Dict[str, object]] = []

    categorical_columns = [
        column for column, detected_type in column_types.items() if detected_type == "categorical"
    ]
    numeric_columns = [
        column for column, detected_type in column_types.items() if detected_type == "numeric"
    ]
    date_columns = [column for column, detected_type in column_types.items() if detected_type == "date"]

    # Single-column recommendations
    for column in categorical_columns:
        suggestions.append(
            {
                "chart_type": "bar",
                "columns": [column],
                "reason": f"'{column}' is categorical, so a bar chart is suitable.",
            }
        )
    for column in numeric_columns:
        suggestions.append(
            {
                "chart_type": "histogram",
                "columns": [column],
                "reason": f"'{column}' is numeric, so a histogram is suitable.",
            }
        )
    for column in date_columns:
        suggestions.append(
            {
                "chart_type": "line",
                "columns": [column],
                "reason": f"'{column}' is date-like, so a line chart is suitable for trends.",
            }
        )

    # Pair recommendations: categorical + numeric
    for categorical_column in categorical_columns:
        for numeric_column in numeric_columns:
            suggestions.append(
                {
                    "chart_type": "pie_or_grouped_bar",
                    "columns": [categorical_column, numeric_column],
                    "reason": (
                        f"'{categorical_column}' (categorical) with '{numeric_column}' (numeric) "
                        "fits a pie chart or grouped bar chart."
                    ),
                }
            )

    if not suggestions:
        suggestions.append(
            {
                "chart_type": "table",
                "columns": [],
                "reason": "No clear chart recommendation based on detected column types.",
            }
        )

    return suggestions


def analyze_dataframe(dataframe: pd.DataFrame) -> Dict[str, object]:
    column_types = {
        column: detect_column_type(dataframe[column]) for column in dataframe.columns
    }
    audit = build_data_audit(dataframe)
    stats = build_numeric_stats(dataframe)
    anomalies = build_anomaly_report(dataframe)
    return {
        "column_types": column_types,
        "audit": audit,
        "stats": stats,
        "anomalies": anomalies,
        "insights": build_insights(dataframe, audit, stats, anomalies),
        "chart_suggestions": build_chart_suggestions(column_types),
    }


def build_dashboard_config(dataframe: pd.DataFrame) -> Dict[str, object]:
    analysis = analyze_dataframe(dataframe)
    audit = analysis["audit"]
    anomalies = analysis["anomalies"]
    missing_values = audit.get("missing_values_per_column", {})
    total_missing = int(sum(int(value) for value in missing_values.values()))
    rows = int(dataframe.shape[0])
    columns = int(dataframe.shape[1])
    generated_at = datetime.now(timezone.utc).isoformat()

    anomaly_highlights = [
        {"column": column_name, "count": int(report.get("anomaly_count", 0))}
        for column_name, report in anomalies.items()
        if int(report.get("anomaly_count", 0)) > 0
    ]

    return {
        "meta": {
            "rows": rows,
            "columns": columns,
            "generated_at": generated_at,
        },
        "summary": [
            {"title": "Health Score", "value": audit.get("health_score", 0)},
            {"title": "Duplicate Rows", "value": audit.get("duplicate_rows_count", 0)},
            {"title": "Total Missing Values", "value": total_missing},
        ],
        "charts": analysis.get("chart_suggestions", []),
        "insights": analysis.get("insights", []),
        "anomalies": anomaly_highlights,
    }


def build_numeric_stats(dataframe: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    numeric_stats: Dict[str, Dict[str, float]] = {}

    for column in dataframe.columns:
        numeric_series = pd.to_numeric(dataframe[column], errors="coerce").dropna()
        if numeric_series.empty:
            continue

        numeric_stats[column] = {
            "mean": round(float(numeric_series.mean()), 4),
            "min": round(float(numeric_series.min()), 4),
            "max": round(float(numeric_series.max()), 4),
            "total": round(float(numeric_series.sum()), 4),
        }

    return numeric_stats


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(RequestValidationError)
async def upload_validation_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    if request.url.path in {"/upload", "/audit", "/analyze", "/stats", "/dashboard"}:
        return JSONResponse(
            status_code=400,
            content={"detail": "Please choose a CSV file in field 'file'."},
        )
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
) -> Dict[str, Dict[str, str]]:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    content = await file.read()
    try:
        csv_text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded.")
    return detect_types_from_csv_text(csv_text)


@app.post("/audit")
async def audit_csv(file: UploadFile = File(...)) -> Dict[str, object]:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    content = await file.read()
    try:
        csv_text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded.")

    dataframe = parse_csv_text(csv_text)
    return build_data_audit(dataframe)


@app.post("/analyze")
async def analyze_csv(file: UploadFile = File(...)) -> Dict[str, object]:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    content = await file.read()
    try:
        csv_text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded.")

    dataframe = parse_csv_text(csv_text)
    return analyze_dataframe(dataframe)


@app.post("/stats")
async def stats_csv(file: UploadFile = File(...)) -> Dict[str, Dict[str, Dict[str, float]]]:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    content = await file.read()
    try:
        csv_text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded.")

    dataframe = parse_csv_text(csv_text)
    return {"numeric_column_stats": build_numeric_stats(dataframe)}


@app.post("/dashboard", response_model=DashboardResponse)
async def dashboard_csv(file: UploadFile = File(...)) -> DashboardResponse:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    content = await file.read()
    try:
        csv_text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded.")

    dataframe = parse_csv_text(csv_text)
    return DashboardResponse(**build_dashboard_config(dataframe))


def custom_openapi() -> Dict:
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="Upload CSV and detect column types.",
        routes=app.routes,
    )
    upload_post = schema.get("paths", {}).get("/upload", {}).get("post", {})
    upload_responses = upload_post.get("responses", {})
    upload_responses.pop("422", None)
    upload_post["responses"] = upload_responses

    audit_post = schema.get("paths", {}).get("/audit", {}).get("post", {})
    audit_responses = audit_post.get("responses", {})
    audit_responses.pop("422", None)
    audit_post["responses"] = audit_responses

    analyze_post = schema.get("paths", {}).get("/analyze", {}).get("post", {})
    analyze_responses = analyze_post.get("responses", {})
    analyze_responses.pop("422", None)
    analyze_post["responses"] = analyze_responses

    stats_post = schema.get("paths", {}).get("/stats", {}).get("post", {})
    stats_responses = stats_post.get("responses", {})
    stats_responses.pop("422", None)
    stats_post["responses"] = stats_responses

    dashboard_post = schema.get("paths", {}).get("/dashboard", {}).get("post", {})
    dashboard_responses = dashboard_post.get("responses", {})
    dashboard_responses.pop("422", None)
    dashboard_post["responses"] = dashboard_responses

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi
