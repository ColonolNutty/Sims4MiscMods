"""
This file is part of Change Motives licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnchangemotives.utils.motive_utils import CMMotiveUtils
from server_commands.argument_helpers import OptionalSimInfoParam, get_optional_target
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


@Command('cm.help', command_type=CommandType.Live)
def _cm_help(opt_sim: OptionalSimInfoParam=None, _connection: int=None):
    output = CheatOutput(_connection)
    output('Motive values range from -100.0 to 100.0. With 0.0 being 50% of the Motive bar.')
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is not None:
        output('Available Motives for the current Sim:')
        output('Hygiene is the same as Hydration for Mermaids.')
        output('Social is the same as Affection for Pets.')
        for motive in CMMotiveUtils().get_valid_motives(sim_info):
            output('- {}'.format(motive))
    output('Available Commands:')
    output('cm.set <motive_name> <level>')
    output('    | Set the motive level of a Sim. "level" can be -100.0 to 100.0')
    output('cm.max <motive_name>')
    output('    | Set the motive level of a Sim to its maximum 100.0.')
    output('cm.min <motive_name>')
    output('    | Set the motive level of a Sim to its minimum -100.0.')
    output('cm.min_all')
    output('    | Set all motives of a Sim to their minimum -100.0.')
    output('cm.max_all')
    output('    | Set all motives of a Sim to their maximum 100.0.')


@Command('cm.set', command_type=CommandType.Live)
def _cm_set_motive(motive_name: str, level: float, opt_sim: OptionalSimInfoParam=None, _connection: int=None):
    output = CheatOutput(_connection)
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is None:
        output('Failed, No Sim found!')
        return False
    if not CMMotiveUtils().can_translate_motive(sim_info, motive_name):
        output('Invalid motive: Valid motives for \'{}\' are as follows:'.format(CommonSimNameUtils.get_full_name(sim_info)))
        for motive in CMMotiveUtils().get_valid_motives(sim_info):
            output('- {}'.format(motive))
        return False
    output('Setting motive \'{}\' to \'{}\' for \'{}\''.format(motive_name, level, CommonSimNameUtils.get_full_name(sim_info)))
    result = CMMotiveUtils().change_motive_level(sim_info, motive_name, level)
    if not result:
        output('Failed to set motive level.')
    else:
        output('Success!')
    output('Done')


@Command('cm.max', command_type=CommandType.Live)
def _cm_max_motive(motive_name: str, opt_sim: OptionalSimInfoParam=None, _connection: int=None):
    output = CheatOutput(_connection)
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is None:
        output('Failed, No Sim found!')
        return False
    if not CMMotiveUtils().can_translate_motive(sim_info, motive_name):
        output('Invalid motive: Valid motives for \'{}\' are as follows:'.format(CommonSimNameUtils.get_full_name(sim_info)))
        for motive in CMMotiveUtils().get_valid_motives(sim_info):
            output('- {}'.format(motive))
        return False
    output('Setting motive \'{}\' to \'{}\' for \'{}\''.format(motive_name, 100.0, CommonSimNameUtils.get_full_name(sim_info)))
    result = CMMotiveUtils().change_motive_level(sim_info, motive_name, 100.0)
    if not result:
        output('Failed to set motive level.')
    else:
        output('Success!')
    output('Done')


@Command('cm.min', command_type=CommandType.Live)
def _cm_min_motive(motive_name: str, opt_sim: OptionalSimInfoParam=None, _connection: int=None):
    output = CheatOutput(_connection)
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is None:
        output('Failed, No Sim found!')
        return False
    if not CMMotiveUtils().can_translate_motive(sim_info, motive_name):
        output('Invalid motive: Valid motives for \'{}\' are as follows:'.format(CommonSimNameUtils.get_full_name(sim_info)))
        for motive in CMMotiveUtils().get_valid_motives(sim_info):
            output('- {}'.format(motive))
        return False
    output('Setting motive \'{}\' to \'{}\' for \'{}\''.format(motive_name, -100.0, CommonSimNameUtils.get_full_name(sim_info)))
    result = CMMotiveUtils().change_motive_level(sim_info, motive_name, -100.0)
    if not result:
        output('Failed to set motive level.')
    else:
        output('Success!')
    output('Done')


@Command('cm.min_all', command_type=CommandType.Live)
def _cm_min_all_motives(opt_sim: OptionalSimInfoParam=None, _connection: int=None):
    output = CheatOutput(_connection)
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is None:
        output('Failed, No Sim found!')
        return False
    output('Setting all motives to minimum for \'{}\''.format(CommonSimNameUtils.get_full_name(sim_info)))
    result = CMMotiveUtils().min_all_motives(sim_info)
    if not result:
        output('Failed to set motive level.')
    else:
        output('Success!')
    output('Done')


@Command('cm.max_all', command_type=CommandType.Live)
def _cm_max_all_motives(opt_sim: OptionalSimInfoParam=None, _connection: int=None):
    output = CheatOutput(_connection)
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is None:
        output('Failed, No Sim found!')
        return False
    output('Setting all motives to maximum for \'{}\''.format(CommonSimNameUtils.get_full_name(sim_info)))
    result = CMMotiveUtils().max_all_motives(sim_info)
    if not result:
        output('Failed to set motive level.')
    else:
        output('Success!')
    output('Done')
