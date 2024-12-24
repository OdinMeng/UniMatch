from typing import List, Dict, Optional
from pydantic import BaseModel

class UniInfo(BaseModel):
    """
    Represents information about a university or course, including its opportunities.
    """
    name: str
    location: str
    courses: Optional[List[str]]
    subjects: Optional[Dict[str, list[str]]]
    scholarships: Optional[Dict[str, str]]  # e.g., {course_name: scholarship_info}
    requisites: Optional[Dict[str, str]]    # e.g., {course_name: requisite_info}
    areas: Optional[List[str]]

    def __str__(self) -> str:
        course_list = ", ".join(self.courses)
        subjects_list = ", ".join(self.subjects)
        scholarships_list = "\n".join([f"{course}: {scholarship}" for course, scholarship in self.scholarships.items()])
        requisites_list = "\n".join([f"{course}: {requisite}" for course, requisite in self.requisites.items()])
        areas_list = ", ".join(self.areas)
        return (
            f"University Name: {self.name}\n"
            f"Location: {self.location}\n"
            f"Courses Offered: {course_list}\n"
            f"Subjects Offered: {subjects_list}\n"
            f"Scholarships:\n{scholarships_list}\n"
            f"Requisites:\n{requisites_list}\n"
            f"Areas: {areas_list}\n"
        )


class Matches(BaseModel):
    """
    Represents a list of university/course matches.
    """
    matches: List[UniInfo]

    def __str__(self) -> str:
        if not self.matches:
            return "No matches found."
        return "\n\n".join(str(match) for match in self.matches)


class UserInfo(BaseModel):
    """
    Represents information about the user and their preferences.
    """
    name: str
    age: int
    country: str
    education_level: str
    preferences: Optional[Dict[str, int]]
    main_area: Optional[str]

    def __str__(self) -> str:
        preferences_list = ", ".join(f"{interest}: {weight}" for interest, weight in self.preferences.items())
        return (
            f"User Name: {self.name}\n"
            f"Country: {self.country}\n"
            f"Age: {self.age}\n"
            f"Education level: {self.education_level}\n"
            f"Preferences (and weight): {preferences_list}\n"
            f"Main Area: {self.main_area}\n"
        )

class Preferences(BaseModel):
    """
    Represents preferences of a user
    """
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