import math
from careers.career_base import CareerBase
from cnrealisticsalaries.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CareerBase, CareerBase.get_hourly_pay.__name__)
def _rs_get_hourly_pay(original, *_, **__) -> float:
    original_pay = original(*_, **__)
    return math.ceil(original_pay * 0.6)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CareerBase, CareerBase.get_assignment_pay.__name__)
def _rs_get_assignment_pay(original, self, *_, **__) -> float:
    original_pay = original(self, *_, **__)
    return math.ceil(original_pay * 0.6)
