from collections import Iterator
from typing import Any, Callable
from cnnorelationshipdecay.modinfo import ModInfo
from relationships.relationship_track import RelationshipTrack
from sims.household import Household
from sims.sim_info import SimInfo
from sims4.commands import Command, CommandType, CheatOutput
from cnnorelationshipdecay.save_and_load import NRDSettings, NRDSettingUtils
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class _NRDRelationshipUtils(CommonService, HasLog):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'nrd_relationships'

    def update_relationship_decay(self, sim_info_list: Iterator[SimInfo]=()):
        """ Update the relationship decay for friendship and romance. """
        friendship_decay_percentage = self._as_percentage(NRDSettingUtils().get_setting(NRDSettings.FRIENDSHIP_DECAY, variable_type=float))
        romance_decay_percentage = self._as_percentage(NRDSettingUtils().get_setting(NRDSettings.ROMANCE_DECAY, variable_type=float))
        all_sims = sim_info_list or CommonSimUtils.get_sim_info_for_all_sims_generator()
        for sim_info in all_sims:
            if sim_info is None:
                continue
            relationships = sim_info.relationship_tracker
            for relationship in relationships:
                target_id = relationship.sim_id_a
                relationship_tracks = sim_info.relationship_tracker.relationship_tracks_gen(target_id)
                for relationship_track in relationship_tracks:
                    if relationship_track.stat_type == relationship_track.FRIENDSHIP_TRACK:
                        self._modify_decay_rate(relationship_track, friendship_decay_percentage)
                    elif relationship_track.stat_type == relationship_track.ROMANCE_TRACK:
                        self._modify_decay_rate(relationship_track, romance_decay_percentage)

    def show_relationships(self, sim_info_list: Iterator[SimInfo], redirect_log: Callable[[str], Any]=None):
        """ Show the relationships of the specified Sims. """
        if redirect_log is None:
            redirect_log = self.log.debug

        for sim_info in sim_info_list:
            relationships = sim_info.relationship_tracker
            for relationship in relationships:
                target_id = relationship.sim_id_a
                target_sim_info = CommonSimUtils.get_sim_info(target_id)
                tracks = sim_info.relationship_tracker.relationship_tracks_gen(target_id)
                for track in tracks:
                    if track.stat_type == track.ROMANCE_TRACK:
                        decay = track.get_decay_rate_modifier() * 100
                        redirect_log("Decay rate for {}'s romance bar with {} is {} percent of normal rate".format(CommonSimNameUtils.get_full_name(sim_info), CommonSimNameUtils.get_full_name(target_sim_info), decay))
                    elif track.stat_type == track.FRIENDSHIP_TRACK:
                        decay = track.get_decay_rate_modifier() * 100
                        redirect_log("Decay rate for {}'s friendship bar with {} is {} percent of normal rate".format(CommonSimNameUtils.get_full_name(sim_info), CommonSimNameUtils.get_full_name(target_sim_info), decay))

    def _modify_decay_rate(self, relationship_track: RelationshipTrack, percentage_amount: float):
        romance_decay = relationship_track.get_decay_rate_modifier()
        relationship_track.remove_decay_rate_modifier(romance_decay)
        relationship_track.add_decay_rate_modifier(percentage_amount)

    def _as_percentage(self, statistic: float) -> float:
        if statistic is None:
            statistic = 0.0
        if statistic > 0.0:
            percentage = statistic / 100.0
        else:
            percentage = 0.0
        return percentage


# noinspection PyMissingOrEmptyDocstring
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Household, Household._on_sim_added.__name__)
def _nrd_set_relationship_decay_on_sim_added_to_household(original, self: Household, sim_info: SimInfo, *_, **__):
    original(self, sim_info, *_, **__)
    _NRDRelationshipUtils().update_relationship_decay(sim_info_list=(sim_info,))


# noinspection PyMissingOrEmptyDocstring
@Command('nrd.set_friendship_decay', command_type=CommandType.Live)
def set_friendship_decay(new_friendship_decay: int=None, _connection: int=None):
    output = CheatOutput(_connection)
    if new_friendship_decay is None:
        output("Usage: friendship.decay [positive number 1-100]")
        return
    if new_friendship_decay < 0:
        output("You have typed in a negative value! Don't type negative values or I'll personally send ninjas after you.")
        return
    NRDSettingUtils().set_setting(NRDSettings.FRIENDSHIP_DECAY, new_friendship_decay)
    _NRDRelationshipUtils().update_relationship_decay()
    output("Done! You have modified friendship decay for all sims to {} percent of the normal rate.".format(new_friendship_decay))


@Command('nrd.set_romance_decay', command_type=CommandType.Live)
def _nrd_set_romance_decay(new_romance_decay: int=None, _connection: int=None):
    output = CheatOutput(_connection)
    if new_romance_decay is None:
        output("Usage: romance.decay [positive number 1-100]")
        return
    if new_romance_decay < 0:
        output("You have typed in a negative value! Don't type negative values or I'll personally send ninjas after you.")
        return
    NRDSettingUtils().set_setting(NRDSettings.ROMANCE_DECAY, new_romance_decay)
    _NRDRelationshipUtils().update_relationship_decay()
    output("Done! You have modified romance decay for all sims to {} percent of the normal rate.".format(new_romance_decay))


@Command('nrd_testing.show_household_relationship_decay', command_type=CommandType.Live)
def _nrd_testing_show_household_relationship_decay(_connection: int=None):
    output = CheatOutput(_connection)
    output('Showing Household Relationship Decay Values.')
    _NRDRelationshipUtils().show_relationships(CommonHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator())
    output('Done')


@Command('nrd_testing.show_relationship_decay', command_type=CommandType.Live)
def _nrd_testing_show_relationship_decay(_connection: int=None):
    output = CheatOutput(_connection)
    output('Showing Relationship Decay Values.')
    _NRDRelationshipUtils().show_relationships(CommonSimUtils.get_sim_info_for_all_sims_generator())
    output('Done')


@Command('nrd_testing.get_decay_values', command_type=CommandType.Live)
def _nrd_testing_get_decay_values(_connection: int=None):
    output = CheatOutput(_connection)
    output('Showing Friendship and Romance decay settings.')
    friendship = NRDSettingUtils().get_setting(NRDSettings.FRIENDSHIP_DECAY, int)
    romance = NRDSettingUtils().get_setting(NRDSettings.ROMANCE_DECAY, int)
    output('Decay Constants for this mod are: GL_FRIENDSHIP_DECAY = {} | GL_ROMANCE_DECAY = {}'.format(friendship, romance))
