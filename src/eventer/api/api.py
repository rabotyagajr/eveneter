from eventer.api import (
    user_router,
    event_router,
    team_router,
    team_members_router,
    city_router,
    organization_router,
    event_members_router,
    stage_router,
    eventdays_router,
    event_teams_router,
    stage_team_transitions_router,
    stage_score_router,
    score_details_router,
    certificate_router,
    document_router,
    leaderboard_router,
    parameter_router,
)
from fastapi import APIRouter

api_router = APIRouter(prefix="/api")

api_router.include_router(user_router)
api_router.include_router(event_router)
api_router.include_router(team_router)
api_router.include_router(team_members_router)
api_router.include_router(city_router)
api_router.include_router(organization_router)
api_router.include_router(event_members_router)
api_router.include_router(stage_router)
api_router.include_router(eventdays_router)
api_router.include_router(event_teams_router)
api_router.include_router(stage_team_transitions_router)
api_router.include_router(stage_score_router)
api_router.include_router(score_details_router)
api_router.include_router(certificate_router)
api_router.include_router(document_router)
api_router.include_router(leaderboard_router)
api_router.include_router(parameter_router)
