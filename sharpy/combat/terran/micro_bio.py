from genericpath import exists
from sc2.dicts.unit_abilities import UNIT_ABILITIES
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sharpy.combat import Action, GenericMicro
from sc2.ids.buff_id import BuffId
from sc2.unit import Unit
from sc2.units import Units
from sharpy.plans.require import enemy_unit_exists
from sc2.game_info import GameInfo
from sc2.game_data import GameData
from sc2.game_state import GameState

class MicroBio(GenericMicro):
    def __init__(self):
        super().__init__()
        self.stim_required = 0

    def group_solve_combat(self, units: Units, current_command: Action) -> Action:
        self.stim_required = self.engaged_power.power
        for unit in units:
            if self.has_stim(unit):
                if unit.type_id == UnitTypeId.MARAUDER:
                    self.stim_required -= 2
                else:
                    self.stim_required -= 1

        return super().group_solve_combat(units, current_command)

    def unit_solve_combat(self, unit: Unit, current_command: Action) -> Action:

        if self.stim_required > 0 and not self.has_stim(unit) and unit.shield_health_percentage > 0.5:
            if unit.type_id == UnitTypeId.MARAUDER and self.cd_manager.is_ready(
                unit.tag, AbilityId.EFFECT_STIM_MARAUDER
            ):
                self.stim_required -= 2
                return Action(None, False, AbilityId.EFFECT_STIM_MARAUDER)
            elif unit.type_id == UnitTypeId.MARINE and self.cd_manager.is_ready(unit.tag, AbilityId.EFFECT_STIM_MARINE):
                self.stim_required -= 1
                return Action(None, False, AbilityId.EFFECT_STIM_MARINE)

        return super().unit_solve_combat(unit, current_command)

    def has_stim(self, unit: Unit) -> bool:
        return unit.has_buff(BuffId.STIMPACK) or unit.has_buff(BuffId.STIMPACKMARAUDER)
