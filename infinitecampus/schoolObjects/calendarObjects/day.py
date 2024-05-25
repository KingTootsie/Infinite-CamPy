from datetime import datetime
from typing import (Union, Optional)

class Day(object):
    """Represents a school day in the calendar."""
    def __init__(
        self,
        date: Union[str, datetime],
        is_school_day: bool,
        requires_attendance: bool,
        day_id: int,
        calendar_id: int,
        structure_id: int,
        comment: Optional[str],

    ) -> None:
        self.date = date if isinstance(date, datetime) else datetime.fromisoformat(date)
        self.is_school_day: bool = is_school_day
        self.requires_attendance: bool = requires_attendance
        self.day_id = day_id
        self.calendar_id = calendar_id
        self.structure_id = structure_id
        self.comment = comment
