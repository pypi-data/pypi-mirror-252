from .api import get_datetime_from_string
from typing import Any

class Course:
    def __init__(self, json_course: dict[str, Any]) -> None:
        
        self.id: str = json_course['id']
        self.name: str = json_course['name']
        
        # Just get the important id and name fields.
        if ('place' in json_course.keys()):
            self.place: dict[str, str] = {k:v for (k,v) in json_course['place'].items() if k in 'id name'}
        
        self.start = get_datetime_from_string(f"{json_course['date']}T{json_course['start'][:-6]}.0000Z")
        self.end = get_datetime_from_string(f"{json_course['date']}T{json_course['end'][:-6]}.0000Z")