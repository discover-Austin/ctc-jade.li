"""
Technical service bulletins, recalls, and common problems API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.base import get_db
from app.models.technical import TechnicalBulletin, Recall, CommonProblem
from pydantic import BaseModel
from datetime import date, datetime

router = APIRouter()


class TSBResponse(BaseModel):
    """Technical Service Bulletin response schema."""
    tsb_id: UUID
    vehicle_id: UUID
    bulletin_number: str
    issue_date: Optional[date]
    title: str
    category: Optional[str]
    symptom_description: Optional[str]
    condition_description: Optional[str]
    root_cause: Optional[str]
    correction_procedure: Optional[str]
    manufacturer_official: bool

    class Config:
        from_attributes = True


class RecallResponse(BaseModel):
    """Recall response schema."""
    recall_id: UUID
    vehicle_id: UUID
    nhtsa_campaign_number: Optional[str]
    manufacturer_recall_number: Optional[str]
    recall_date: Optional[date]
    recall_type: Optional[str]
    component: Optional[str]
    summary: Optional[str]
    consequence: Optional[str]
    remedy: Optional[str]
    recall_status: Optional[str]

    class Config:
        from_attributes = True


class CommonProblemResponse(BaseModel):
    """Common problem response schema."""
    problem_id: UUID
    vehicle_id: UUID
    problem_title: str
    problem_category: Optional[str]
    symptoms: Optional[str]
    prevalence: Optional[str]
    detailed_description: Optional[str]
    root_cause: Optional[str]
    diagnosis_procedure: Optional[str]
    solution: Optional[str]
    estimated_repair_cost: Optional[str]
    community_reports: int
    verified: bool
    upvotes: int

    class Config:
        from_attributes = True


@router.get("/tsbs/{vehicle_id}", response_model=List[TSBResponse])
async def get_technical_bulletins(
    vehicle_id: UUID,
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Retrieve Technical Service Bulletins (TSBs) for a vehicle.

    Optional filters:
    - **category**: Filter by category (Engine, Transmission, Electrical, etc.)
    - **search**: Search in bulletin title and description
    - **limit**: Maximum results
    - **offset**: Pagination offset

    Returns manufacturer TSBs including:
    - Bulletin number and issue date
    - Symptom and condition descriptions
    - Root cause analysis
    - Correction procedures
    - Required parts and tools
    - Related DTC codes
    """
    query = db.query(TechnicalBulletin).filter(
        TechnicalBulletin.vehicle_id == vehicle_id
    )

    if category:
        query = query.filter(TechnicalBulletin.category.ilike(f"%{category}%"))

    if search:
        query = query.filter(
            TechnicalBulletin.title.ilike(f"%{search}%") |
            TechnicalBulletin.symptom_description.ilike(f"%{search}%")
        )

    tsbs = query.order_by(TechnicalBulletin.issue_date.desc()).offset(offset).limit(limit).all()

    return tsbs


@router.get("/tsbs/detail/{tsb_id}")
async def get_tsb_detail(
    tsb_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get detailed information for a specific TSB.

    Returns complete TSB information including:
    - Full correction procedure
    - Parts list with OEM numbers
    - Special tools required
    - Warranty information
    - Related DTC codes
    - Superseded bulletins
    """
    tsb = db.query(TechnicalBulletin).filter(
        TechnicalBulletin.tsb_id == tsb_id
    ).first()

    if not tsb:
        raise HTTPException(status_code=404, detail="TSB not found")

    return tsb


@router.get("/recalls/{vehicle_id}", response_model=List[RecallResponse])
async def get_recalls(
    vehicle_id: UUID,
    active_only: bool = Query(True, description="Show only active recalls"),
    recall_type: Optional[str] = Query(None, description="Filter by type (Safety, Compliance, Emissions)"),
    db: Session = Depends(get_db)
):
    """
    Retrieve safety recalls and campaigns for a vehicle.

    Optional filters:
    - **active_only**: Show only active recalls (default: true)
    - **recall_type**: Filter by type (Safety, Compliance, Emissions)

    Returns NHTSA recalls including:
    - Campaign numbers
    - Component affected
    - Safety consequence
    - Remedy description
    - Affected VIN ranges
    - Recall status
    """
    query = db.query(Recall).filter(Recall.vehicle_id == vehicle_id)

    if active_only:
        query = query.filter(Recall.recall_status == 'Active')

    if recall_type:
        query = query.filter(Recall.recall_type == recall_type)

    recalls = query.order_by(Recall.recall_date.desc()).all()

    return recalls


@router.get("/recalls/detail/{recall_id}")
async def get_recall_detail(
    recall_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get detailed information for a specific recall.

    Returns complete recall information including:
    - Full consequence and remedy descriptions
    - Affected VIN ranges
    - Affected quantity
    - Remedy availability date
    - Official bulletin PDF
    """
    recall = db.query(Recall).filter(Recall.recall_id == recall_id).first()

    if not recall:
        raise HTTPException(status_code=404, detail="Recall not found")

    return recall


@router.get("/common-problems/{vehicle_id}", response_model=List[CommonProblemResponse])
async def get_common_problems(
    vehicle_id: UUID,
    category: Optional[str] = Query(None, description="Filter by category"),
    sort_by: str = Query("prevalence", description="Sort by: prevalence, reports, upvotes"),
    verified_only: bool = Query(False, description="Show only verified problems"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Retrieve common problems and solutions for a vehicle.

    Optional filters:
    - **category**: Filter by problem category
    - **sort_by**: Sort by prevalence, reports, or upvotes
    - **verified_only**: Show only verified problems
    - **limit**: Maximum results
    - **offset**: Pagination offset

    Returns community-reported problems including:
    - Problem description and symptoms
    - Prevalence rating
    - Root cause analysis
    - Diagnosis procedure
    - Solution and repair costs
    - Related DTCs and TSBs
    - Community reports and votes
    """
    query = db.query(CommonProblem).filter(CommonProblem.vehicle_id == vehicle_id)

    if category:
        query = query.filter(CommonProblem.problem_category.ilike(f"%{category}%"))

    if verified_only:
        query = query.filter(CommonProblem.verified == True)

    # Apply sorting
    if sort_by == "prevalence":
        query = query.order_by(CommonProblem.prevalence.desc())
    elif sort_by == "reports":
        query = query.order_by(CommonProblem.community_reports.desc())
    elif sort_by == "upvotes":
        query = query.order_by(CommonProblem.upvotes.desc())

    problems = query.offset(offset).limit(limit).all()

    return problems


@router.get("/common-problems/detail/{problem_id}")
async def get_common_problem_detail(
    problem_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get detailed information for a specific common problem.

    Returns complete problem information including:
    - Full diagnosis procedure
    - Detailed solution steps
    - Parts typically needed
    - Prevention tips
    - Related DTCs and TSBs
    - Community statistics
    """
    problem = db.query(CommonProblem).filter(
        CommonProblem.problem_id == problem_id
    ).first()

    if not problem:
        raise HTTPException(status_code=404, detail="Common problem not found")

    return problem


@router.post("/common-problems/{problem_id}/upvote")
async def upvote_common_problem(
    problem_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Upvote a common problem to indicate it affected your vehicle.

    This helps identify the most common issues for each vehicle model.
    """
    problem = db.query(CommonProblem).filter(
        CommonProblem.problem_id == problem_id
    ).first()

    if not problem:
        raise HTTPException(status_code=404, detail="Common problem not found")

    problem.upvotes += 1
    problem.community_reports += 1
    db.commit()

    return {
        "message": "Problem upvoted successfully",
        "problem_id": problem_id,
        "upvotes": problem.upvotes,
        "community_reports": problem.community_reports
    }


@router.get("/categories")
async def get_technical_categories():
    """
    Get list of all technical categories for TSBs and common problems.

    Returns standard categories used across TSBs, recalls, and common problems.
    """
    return {
        "categories": [
            "Engine",
            "Transmission",
            "Brakes",
            "Suspension",
            "Steering",
            "Electrical",
            "HVAC",
            "Fuel System",
            "Exhaust",
            "Cooling System",
            "Body",
            "Interior",
            "Safety Systems",
            "Infotainment",
            "Emissions",
            "Lighting",
            "Wipers/Washers"
        ]
    }
