from cnhaterskeephatin.modinfo import ModInfo
from sims4communitylib.enums.relationship_tracks_enum import CommonRelationshipTrackId
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interaction.events.interaction_queued import S4CLInteractionQueuedEvent
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _hkh_check_if_nice_interaction(event_data: S4CLInteractionQueuedEvent):
    interaction_sim = event_data.interaction.sim
    interaction_target = event_data.interaction.target
    if not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
        return True
    sim_info = CommonSimUtils.get_sim_info(interaction_sim)
    target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
    if event_data.interaction.is_user_directed:
        return True
    friendship_track = CommonRelationshipUtils.get_relationship_level_of_sims(sim_info, target_sim_info, CommonRelationshipTrackId.FRIENDSHIP)
    if friendship_track > -50.0:
        return True
    interaction_game_tags = event_data.interaction.get_category_tags()
    if CommonGameTag.INTERACTION_FRIENDLY in interaction_game_tags or CommonGameTag.INTERACTION_FUNNY in interaction_game_tags or CommonGameTag.SOCIAL_FLIRTY in interaction_game_tags:
        return False
    return True
