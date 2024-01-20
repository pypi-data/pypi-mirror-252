from .api import get_token_with_digits,\
                            get_sws_id_from_token,\
                            get_courses_starting_from_today,\
                            send_signature, \
                            check_course_code
                                
from datetime import datetime
from .Course import Course

import sws_api_wrapper.api as api
api.SIMULATE_REALISTIC_REQUESTS = True

class User:
        
    def __init__(self, institution_code: int, login_code: int, login_pin: int) -> None:        
        
        self.token = get_token_with_digits(institution_code, login_code, login_pin)["token"]
        
        self.id = get_sws_id_from_token(self.token)
        
        
    def get_future_courses(self, number_of_courses: int = 4):
        
        return list(map(
            lambda json_course: Course(json_course), 
            get_courses_starting_from_today(self.token, number_of_courses)
        ))
    
    def get_todays_courses(self):
        
        return list(filter(
            lambda course: course.end.date() == datetime.today().date(),
            self.get_future_courses(5)
        ))
        
    def check_code(self, course: Course, code: str):
        
        return check_course_code(self.token, course.id, code)
    
    def sign(self, course: Course, image_path: str):
        
        send_signature(self.token, course.id, image_path, course.place['id'])
            