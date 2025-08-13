"""Support for tracking FindMy devices."""

from homeassistant.components.device_tracker import TrackerEntity
from homeassistant.components.device_tracker.const import SourceType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import FindMyConfigEntry
from .coordinator import FindMyUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: FindMyConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a FindMy config entry."""
    async_add_entities([FindMyDeviceTracker(entry, entry.runtime_data)])


class FindMyDeviceTracker(CoordinatorEntity[FindMyUpdateCoordinator], TrackerEntity):
    """Representation of a FindMy device tracker."""

    def __init__(
        self, config_entry: ConfigEntry, coordinator: FindMyUpdateCoordinator
    ) -> None:
        """Initialize the FindMy device tracker."""
        super().__init__(coordinator)

        self.config_entry = config_entry
        self._attr_unique_id = coordinator.hub.accessory.identifier
        self._attr_name = coordinator.hub.accessory.name
        self._attr_source_type = SourceType.GPS
        self._attr_extra_state_attributes = {"timestamp": self.timestamp}

    @property
    def location_accuracy(self):
        """Return the location accuracy of the device."""
        return self.coordinator.data.accuracy

    @property
    def latitude(self):
        """Return latitude value of the device."""
        return self.coordinator.data.latitude

    @property
    def longitude(self):
        """Return longitude value of the device."""
        return self.coordinator.data.longitude

    @property
    def timestamp(self):
        """Return the last update timestamp."""
        return self.coordinator.data.timestamp
