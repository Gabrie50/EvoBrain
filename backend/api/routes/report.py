import time

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/report/generate")
async def generate_report(type: str = Query("full", description="full|summary|detailed")):
    from main import evobrain

    if not evobrain.reporter:
        return {"report": "Report generator not available"}
    stats = evobrain.get_stats()
    if type == "summary":
        report = evobrain.reporter.generate_summary(stats)
    elif type == "detailed":
        report = evobrain.reporter.generate_detailed_analysis(stats)
    else:
        report = evobrain.generate_report()
    return {"type": type, "report": report, "timestamp": time.time()}


@router.get("/report/summary")
async def get_summary():
    from main import evobrain

    if not evobrain.reporter:
        return {"summary": "Report generator not available"}
    stats = evobrain.get_stats()
    summary = evobrain.reporter.generate_summary(stats)
    return {"summary": summary, "stats": {"accuracy": stats.get("simulation", {}).get("accuracy", 0)}}
