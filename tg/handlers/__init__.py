from .start import start_router
from .make_report import report_router
from .profile import profile_router
from .statistics import stats_router


routers = [
    start_router,
    profile_router,
    stats_router,
    report_router
]