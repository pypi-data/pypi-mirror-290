""" 
Programa : Controller module for Canvas
Fecha Creacion : 12/08/2024
Version : 1.0.0
Author : Jaime Gomez
"""

import logging
from .base import BaseCanvas
from .account import Accounts
from .adda import BasicModuleCourseCanvasADDA
from .utils import remove_tilde


# Create a logger for this module
logger = logging.getLogger(__name__)

class Semester():
    
    #account_id = "788"           # Account for -->  Diseño y Desarrollo de Software (C24)
    #enrollment_term_id = "8083"  # Semester    -->  PFR L 2024 - 1
    def __init__(self, account_id, enrollment_term_id):
        self.account_id = account_id
        self.enrollment_term_id = enrollment_term_id


class Controller(BaseCanvas):

    def __init__(self, access_token):
        super().__init__(access_token)

    def valid_courses_adda_by_teacher_in_semester(self, teacher_id, semester ):

        accounts = Accounts(semester.account_id, self.access_token)

        courses = accounts.get_courses_by_enrollment_term(semester.enrollment_term_id)  
        logging.info(courses)

        teachers = accounts.get_teachers_by_enrollment_term(semester.enrollment_term_id)  
        #logging.info(teachers)
        for key, value in teachers.items():
            logging.info(f'{key} = {value} ')
        

    def valid_courses_adda_by_teacher_name_in_semester(self, teacher_name, semester ):

        response_adda = []
        
        search_teacher_name = remove_tilde(teacher_name).lower()
        
        accounts = Accounts(semester.account_id, self.access_token)

        accounts.set_courses(
            accounts.get_courses_by_enrollment_term(semester.enrollment_term_id))

        # Get teacher
        teachers = accounts.get_teachers_by_enrollment_term(semester.enrollment_term_id)  
        logging.debug(teachers)
        
        # TO DO : You must olny validate one teacher, no more two

        # Get courses of teacher
        courses_of_teacher = []
        for teacher_id, value in teachers.items():
            if search_teacher_name in value.get("name_search"):            
                    logging.info(f"Found '{teacher_name}' in teacher_id '{teacher_id}': {value.get('name')}")                                    
                    courses_of_teacher = accounts.get_courses_by_enrollment_term_and_teacher(semester.enrollment_term_id,teacher_id )

        # Validate Canvas
        for course in courses_of_teacher:
            logging.debug(course)
            mccsa = BasicModuleCourseCanvasADDA(str(course.get('id')), self.access_token)
            res = mccsa.is_valid_structure()   
            logging.debug(res.get('status_adda'))
            logging.debug(res.get('course'))
            response_adda.append(res)
            
        return response_adda