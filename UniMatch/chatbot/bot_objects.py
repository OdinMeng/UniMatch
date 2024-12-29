from typing import List, Dict, Optional
from pydantic import BaseModel

class UniInfo(BaseModel):
    """ Represents information about a university or course, including its opportunities. Can be represented as a string. """
    name: Optional[str]
    location: Optional[str]
    courses: Optional[List[str]]
    course_descriptions: Optional[List[str]]
    subjects: Optional[Dict[str, List[str]]]
    scholarships: Optional[Dict[str, str]]  # e.g., {course_name: scholarship_info}
    requisites: Optional[Dict[str, str]]    # e.g., {course_name: requisite_info}
    areas: Optional[List[str]]

    def __str__(self) -> str:
        if self.courses!=None:
            course_list = ", ".join(self.courses)
        else:
            course_list = "\nCourses not Available"
        
        if self.course_descriptions!=None:
            course_desc_list =", ".join(self.course_descriptions)
        else:
            course_desc_list = "\nCourses Description Not Available"

        if self.subjects!=None:   
            subjects_list = ", ".join([f"{course}: {subject}" for course, subject in self.subjects.items()])
        else:
            subjects_list = "\nCourses Subjects Information not Available"

        if self.scholarships!=None:
            scholarships_list = "\n".join([f"{course}: {scholarship}" for course, scholarship in self.scholarships.items()])
        else:
            scholarships_list = "\nScholarships Information Not Available"

        if self.requisites != None:
            requisites_list = "\n".join([f"{course}: {requisite}" for course, requisite in self.requisites.items()])
        else:
            requisites_list = "\nRequisites Information Not Available"

        if self.areas != None:
            areas_list = ", ".join(self.areas)
        else:
            areas_list = '\nAreas Information Not Available'
        return (
            f"University Name: {self.name}\n"
            f"Location: {self.location}\n"
            f"Courses Offered: {course_list}\n"
            f"Courses Descriptions: {course_desc_list}\n"
            f"Subjects Offered: {subjects_list}\n"
            f"Scholarships:{scholarships_list}\n"
            f"Requisites:{requisites_list}\n"
            f"Areas: {areas_list}\n"
        )


class Matches(BaseModel):
    """ Represents a list of university/course matches. Can be represented as a string. """
    matches: List[UniInfo]

    def __str__(self) -> str:
        i = 0
        s=""
        if not self.matches:
            return "No matches found."
        else:
            for match in self.matches:
                s += f"==============||MATCH NUMBER {i}||==============\n"
                s += str(match)
            return s



class UserInfo(BaseModel):
    """ Represents information about the user and their preferences. Can be represented as a string. """
    name: Optional[str]
    age: Optional[int]
    country: Optional[str]
    education_level: Optional[str]
    preferences: Optional[Dict[str, int]]
    main_area: Optional[str]

    def __str__(self) -> str:
        if self.preferences is not None:
            preferences_list = ", ".join(f"{interest}: {weight}" for interest, weight in self.preferences.items())
        else:
            preferences_list = 'No preferences Available'
        return (
            f"User Name: {self.name}\n"
            f"Country: {self.country}\n"
            f"Age: {self.age}\n"
            f"Education level: {self.education_level}\n"
            f"Preferences (and weight): {preferences_list}\n"
            f"Main Area: {self.main_area}\n"
        )

class Preferences(BaseModel):
    """ Represents preferences of a user. Can be represented as a dictionary """
    preferences: List[str]
    weights: List[int]

    def to_dict(self) -> Dict[str, int]:
        if len(self.preferences) != len(self.weights): 
            raise ValueError
        else:
            d = {}
            for i in range(len(self.preferences)):
                d[self.preferences[i]] = d[self.weights[i]]
            return d