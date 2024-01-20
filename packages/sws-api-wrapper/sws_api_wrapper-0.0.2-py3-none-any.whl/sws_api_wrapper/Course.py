from sws_python_wrapper import get_datetime_from_string

class Course:
    def __init__(self, json_course) -> None:
        
        self.id: str = json_course['id']
        self.name: str = json_course['name']
        
        # Just get the important id and name fields.
        self.place: dict[str, str] = {k:v for (k,v) in json_course['place'].items() if k in 'id name'}
        
        self.start = get_datetime_from_string(f"{json_course['date']}T{json_course['start']}.0Z")
        self.end = get_datetime_from_string(f"{json_course['date']}T{json_course['end']}.0Z")