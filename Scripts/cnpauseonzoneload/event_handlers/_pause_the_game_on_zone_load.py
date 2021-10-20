"""
This file is part of Pause On Zone Load licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnpauseonzoneload.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from zone import Zone


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Zone, Zone._initialize_clock_speed.__name__)
def _pozl_pause_the_game_on_clock_initialize(original, self: Zone):
    original_result = original(self)
    CommonTimeUtils.pause_the_game()
    return original_result
