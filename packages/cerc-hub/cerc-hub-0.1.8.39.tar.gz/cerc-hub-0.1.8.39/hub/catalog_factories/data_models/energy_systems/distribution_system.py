"""
Energy System catalog distribution system
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""


class DistributionSystem:
  """
  Distribution system class
  """

  def __init__(self, system_id, name, system_type, supply_temperature, distribution_consumption_fix_flow,
               distribution_consumption_variable_flow, heat_losses):
    self._system_id = system_id
    self._name = name
    self._type = system_type
    self._supply_temperature = supply_temperature
    self._distribution_consumption_fix_flow = distribution_consumption_fix_flow
    self._distribution_consumption_variable_flow = distribution_consumption_variable_flow
    self._heat_losses = heat_losses

  @property
  def id(self):
    """
    Get system id
    :return: float
    """
    return self._system_id

  @property
  def name(self):
    """
    Get name
    :return: string
    """
    return self._name

  @property
  def type(self):
    """
    Get type from [air, water, refrigerant]
    :return: string
    """
    return self._type

  @property
  def supply_temperature(self):
    """
    Get supply_temperature in degree Celsius
    :return: float
    """
    return self._supply_temperature

  @property
  def distribution_consumption_fix_flow(self):
    """
    Get distribution_consumption if the pump or fan work at fix mass or volume flow in ratio over peak power (W/W)
    :return: float
    """
    return self._distribution_consumption_fix_flow

  @property
  def distribution_consumption_variable_flow(self):
    """
    Get distribution_consumption if the pump or fan work at variable mass or volume flow in ratio
    over energy produced (J/J)
    :return: float
    """
    return self._distribution_consumption_variable_flow

  @property
  def heat_losses(self):
    """
    Get heat_losses in ratio over energy produced in J/J
    :return: float
    """
    return self._heat_losses

  def to_dictionary(self):
    """Class content to dictionary"""
    content = {
      'Layer': {
        'id': self.id,
        'name': self.name,
        'type': self.type,
        'supply temperature [Celsius]': self.supply_temperature,
        'distribution consumption if fix flow over peak power [W/W]': self.distribution_consumption_fix_flow,
        'distribution consumption if variable flow over peak power [J/J]': self.distribution_consumption_variable_flow,
        'heat losses per energy produced [J/J]': self.heat_losses
      }
    }
    return content
