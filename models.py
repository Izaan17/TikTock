from enum import Enum


class TikTokActivityType(Enum):
    """Types of TikTok activities that can be extracted."""
    FAVORITES = "Favorite Videos"
    LIKES = "Like List"

    @classmethod
    def get_all_types(cls) -> list[str]:
        """Returns a list of all activity type values."""
        return [activity_type.value for activity_type in cls]

    @classmethod
    def from_string(cls, value: str) -> 'TikTokActivityType':
        """Converts a string to a TikTokActivityType enum."""
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"Invalid activity type: {value}")
