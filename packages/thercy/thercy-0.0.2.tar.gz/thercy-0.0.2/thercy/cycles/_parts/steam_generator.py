from thercy.constants import PartType, Property, PropertyInfo
from thercy.state import StateCycle, StateGraph

from .base_part import BasePart, Connection


class SteamGenerator(BasePart):
    """
    Steam generator part where the outlet is at ``value`` of the property
    ``prop`` with the same pressure as the inlet.

    Parameters
    ----------
    label : str
        Label for this part.
    prop : str
        Known property at the outlet.
    value : float
        Value of the known property.
    connections : list[Connection]
        List of connections for this part.
    """
    def __init__(self, label, prop, value, connections=None):
        super().__init__(
            label,
            PartType.HEAT_SOURCE,
            connections,
        )

        self._prop = PropertyInfo.get_strkey(prop)
        self._value = value
        self._deltaH = 0.0

    @property
    def deltaH(self):
        return self._deltaH

    def solve(self, graph: StateGraph, inlets: list[str]):
        outlets = {}

        inlet_label = inlets[0]
        inlet_state = graph.get_state((inlet_label, self.label))

        outlet_state = StateCycle.new_empty_state()
        outlet_state[PropertyInfo.get_intkey(self._prop)] = self._value
        outlet_state[Property.P.value] = inlet_state[Property.P.value]
        StateCycle.calculate_props(outlet_state, graph.fluid, self._prop, 'P')
        # outlet_state[Property.Y.value] = inlet_state[Property.Y.value]

        self._deltaH = (outlet_state[Property.H.value] - inlet_state[Property.H.value]) * inlet_state[Property.Y.value]

        for outlet in self.get_outlets(inlet_label):
            outlets[outlet.label] = outlet_state.copy()

        return outlets
