# This file is a wrapper of the API in python, it just implements usefull functions.

import http.client
import json
from base64 import b64encode, b64decode 
from datetime import date, datetime
import hashlib
from user_agent import generate_navigator

from typing import Any

SO_WE_SIGN = http.client.HTTPSConnection("app.sowesign.com")

SIMULATE_REALISTIC_REQUESTS = False

def __populate_header_with_realistic_content(header: dict[str, Any]) -> dict[str, str]:
    ua = generate_navigator()
    populated = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en",
        "Connection": "keep-alive",
        "Host": "app.sowesign.com",
        "Referer": "https://app.sowesign.com/student/loading",
        "sec-ch-ua": f'"Not A;Brand";v="99", "{ua["app_name"]}";v="{ua["build_version"]}", "{ua["app_code_name"]}";v="{ua["build_version"]}"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": f"{ua['platform']}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": f"{ua['user_agent']}"
    }
    populated.update(header)  
    return populated

def __read_and_decode_http_response() -> Any:
    """Just to remove repeated code

    Returns:
        Any: The result of the previous request decoded and loaded by json.
    """
    
    res = SO_WE_SIGN.getresponse()\
                         .read()\
                         .decode("utf-8")
                         
    res = json.loads(res)
    return res

def __decode_token(token: str) -> dict[str, Any]:
    """Decodes the given token.
    
    The token is encoded in base64.
    We isolate the second part of the token, replace all '-' by '+' and '_' by '/', and decode.

    Args:
        token (str): The token.

    Returns:
        dict: The content of the token.
    """
    
    return json.loads(b64decode(token.split(".")[1].replace("-", "+").replace("_", "/")))

def __encode_token(infos: dict[str, Any]) -> str:
    """Encodes a given dict and creates a token.

    Args:
        infos (dict[str, Any]): The information to encode.
        
        it is this format:
        {
            'aud': 'https://app.sowesign.com',
            'client': {
                'corporateConnector': None,
                'id': 0000,
                'name': 'NAME',
                'sqlVarNumber': None,
                'token': 'M',
                'type': 'standard'
            },
            'entity': {
                'firstName': 'John',
                'id': 0000,
                'lastName': 'Doe',
                'type': 'student'
            },
            'exp': 1111111111, in UNIX time
            'iat': 1111111111, in UNIX time
            'iss': 'https://app.sowesign.com',
            'type': 'student'
        }

    Returns:
        str: The generated token.
    """
    header: dict[str, str] = {'alg': 'HS256', 'typ': 'JWT'}
    
    header_string = b64encode(json.dumps(header).encode()).decode()

    info_string = b64encode(json.dumps(infos).encode()).decode()\
                                                                  .replace("+", "-")\
                                                                  .replace("/", "_")

    return f"{header_string}.{info_string}"
    

def get_token_with_digits(institution_code: int, login_code: int, login_pin: int) -> dict[str, Any]:
    """Sends a token request for the given account ids.
    
    SWS sticks all the codes together and encodes it in base64, this constitutes the sent data to get a valid token.

    Args:
        institution_code (int): The institution identifier
        login_code (int): The personal identifier 
        login_pin (int): The personal pin

    Returns:
        tuple[str, str, str]: The response of the API given by this format : 
        {
            token, (The users temporary token of 4h)
            type, (The token type, always 'Bearer')
            refreshToken (The refresh token)
        }
    """
    
    pass_code:str = str(institution_code) + str(login_code) + str(login_pin)
    
    pass_code_encoded: str = b64encode(pass_code.encode()).decode("ascii")
    
    headers = {
        "Authorization": "JBAuth " + pass_code_encoded
    }
    if (SIMULATE_REALISTIC_REQUESTS):
        headers = __populate_header_with_realistic_content(headers)
    
    SO_WE_SIGN.request("POST",
                       "/api/portal/authentication/token",
                       headers=headers,
                       body="") 
    
    return __read_and_decode_http_response()


def get_sws_id_from_token(token: str) -> int:
    return __decode_token(token)["entity"]["id"]


def get_datetime_from_string(string_datetime: str) -> datetime:
    """Parses the time format given by the API to a datetime object.
    
    The format follows this form : "2024-01-19T14:10:33.571Z"

    Args:
        string_datetime (str): The given time by the API.

    Returns:
        datetime: The datetime object resulting.
    """
    return datetime.strptime(string_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")


def get_server_datetime() -> datetime:
    """Pings the server to know its local time.

    Returns:
        datetime: The servers time.
    """

    SO_WE_SIGN.request("GET",
                       "/api/ping")
    
    res = __read_and_decode_http_response()
    
    server_time = res['time']
    
    return get_datetime_from_string(server_time)
    

def get_courses_starting_from_today(token: str, number_of_courses=4) -> list[dict[str, Any]]:
    """Gets a list of courses assigned to the given token starting from the same day the function is called.

    Args:
        token (str): The user token
        number_of_courses (int, optional): The number of courses to request. Defaults to 4.

    Returns:
        list[dict]: The list of requested courses.
    """
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    if (SIMULATE_REALISTIC_REQUESTS):
        headers = __populate_header_with_realistic_content(headers)
    
    SO_WE_SIGN.request("GET",
                       f"/api/student-portal/future-courses?limit={number_of_courses}", 
                       headers=headers)
    
    return __read_and_decode_http_response()


def get_courses_between_dates(token: str, date_from: date, date_to: date) -> list[dict[str, Any]]:
    """Gets a list of courses between two dates for a given token.

    Args:
        token (str): The user token
        date_from (date): The start date.
        date_to (date): The end date.

    Returns:
        list[dict]: The list of requested courses.
    """
    
    fmt = "%Y-%m-%d"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    if (SIMULATE_REALISTIC_REQUESTS):
        headers = __populate_header_with_realistic_content(headers)
    
    SO_WE_SIGN.request("GET", 
                       f"api/student-portal/courses?from={date_from.strftime(fmt)}&to={date_to.strftime(fmt)}", 
                       headers=headers)
    
    return __read_and_decode_http_response()
    

def get_course_details(token: str, course_id: str) -> dict[str, Any]:
    """Get the detail of a course

    Args:
        token (str): The user token
        course_id (str): The id of the course

    Returns:
        dict: If the course is signed it will respond with information, if not the response will be empty.
    """
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    if (SIMULATE_REALISTIC_REQUESTS):
        headers = __populate_header_with_realistic_content(headers)
    
    SO_WE_SIGN.request("GET", 
                       f"api/student-portal/courses/{course_id}/assiduity", 
                       headers=headers)
    
    return __read_and_decode_http_response()


def check_course_code(token: str, course_id: str, code: str) -> bool:
    """[TODO]Checks if the given code unlocks the course signature.

    Args:
        token (str): The user token
        course_id (str): The course
        code (str): The code to test

    Returns:
        dict: The response from the API.
    """
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    body = {
        "code": code,
        "type": 2
    }
    body = json.dumps(body)
    
    if (SIMULATE_REALISTIC_REQUESTS):
        headers = __populate_header_with_realistic_content(headers)
        

    SO_WE_SIGN.request("POST", 
                       f"api/student-portal/courses/{course_id}/checkcode", 
                       body=body, headers=headers)
    
    return __read_and_decode_http_response()["something"] # TODO to check
    

def send_signature(token: str, course_id: str, png_signature_path: str, place_id: str = "-1") -> None:
    """Sends a signature for a specific course.

    Args:
        token (str): The user token
        course_id (str): The course id
        png_signature_path (str): The path of a png image
        place_id (int, optional): _description_. Defaults to -1.
    """
    
    with open(png_signature_path, 'rb') as image:
        encoded_image: str = "data:image/png;base64," + b64encode(image.read()).decode('ascii')
        
    hashed_encoded_image = hashlib.md5(encoded_image.encode()).hexdigest()
        
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    body = {
        "signedOn": f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}+01:00",
        "collectedOn": f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}+01:00",
        "md5": f"{hashed_encoded_image}",
        "status": "present",
        "signer": get_sws_id_from_token(token=token),
        "course": course_id,
        "file": f"{encoded_image}"
    }
    
    if (SIMULATE_REALISTIC_REQUESTS):
        
        headers = __populate_header_with_realistic_content(headers)
        
        assert place_id != "-1", "To simulate, you MUST indicate the place_id"
        
        body.update({
            "place": place_id,
            "campus": None,
            "collectMode": "studentPortal", # or studentApp for simulating phone app
        })
        
    body = json.dumps(body)
    
    SO_WE_SIGN.request("POST", 
                       "/api/student-portal/signatures", 
                       body, 
                       headers)
    

def get_institution_infos(token: str) -> dict[str, Any]:
    """Gets institution code from token.

    Args:
        token (str): The user token.

    Returns:
        dict[str, Any]: The API result.
    """
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    if (SIMULATE_REALISTIC_REQUESTS):
        headers = __populate_header_with_realistic_content(headers)
    
    SO_WE_SIGN.request("GET", 
                       f"/api/student-portal/institutions/main", 
                       headers=headers)
    
    return __read_and_decode_http_response()