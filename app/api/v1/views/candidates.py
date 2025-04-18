from fastapi import APIRouter, Depends, Query, Response, status

from app.api.v1.dependancies import UUIDCandidate
from app.api.v1.dependancies.validate_authorization import get_current_user
from app.api.v1.serializers import candidates as candidates_serializers
from app.api.v1.repositories import candidates as candidates_repo
from core.constants import ResponseMessages
from core.utils import response_handler

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "/all-candidates",
    response_model=candidates_serializers.SearchCandidatesOut,
)
async def search_candidates(
    search: candidates_serializers.CandidatesSearchSerializer = Depends(),
):
    """
    API endpoint to get all candidates based on the provided search criteria.
    """
    return response_handler(
        data=await candidates_repo.get_all_candidates(search),
        status=status.HTTP_200_OK,
        message=ResponseMessages.Retrieved,
    )


@router.get("/generate-report")
async def generate_report(page_size: int = Query(100), page: int = Query(1)):
    """
    API endpoint to generate candidates report.
    """
    # background_tasks.add_task(candidates_repo.generate_report)

    return Response(
        content=await candidates_repo.generate_report(page_size, page),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=candidates_report.csv"},
    )


@router.post("/", response_model=candidates_serializers.CandidateOut)
async def create_candidate(payload: candidates_serializers.RegisterCandidateSerializer):
    """
    API endpoint to create new candidate.
    """

    return response_handler(
        data=await candidates_repo.create_candidate(payload),
        status=status.HTTP_201_CREATED,
        message=ResponseMessages.Created,
    )


@router.get("/{candidate_uuid}", response_model=candidates_serializers.CandidateOut)
async def get_candidate_by_uuid(candidate: UUIDCandidate):
    """
    API endpoint to get current candidate information.
    """

    return response_handler(
        data=candidates_serializers.Candidates(**candidate.model_dump()),
        status=status.HTTP_200_OK,
        message=ResponseMessages.Retrieved,
    )


@router.patch(
    "/{candidate_uuid}",
    response_model=candidates_serializers.CandidateOut,
)
async def update_user(
    candidate: UUIDCandidate,
    paylaod: candidates_serializers.UpdateCandidateSerializer,
):
    """
    API endpoint to update candidate information.
    """

    return response_handler(
        data=await candidates_repo.update_candidate(candidate, paylaod),
        status=status.HTTP_202_ACCEPTED,
        message=ResponseMessages.Updated,
    )


@router.delete(
    "/{candidate_uuid}",
    response_model=candidates_serializers.DeleteCandidateOut,
)
async def delete_candidate(candidate: UUIDCandidate):
    """
    API endpoint to delete candidate.
    """

    return response_handler(
        data=await candidates_repo.delete_candidate(candidate),
        status=status.HTTP_202_ACCEPTED,
        message=ResponseMessages.Deleted,
    )
