class UniInfo:
    """
    Represents information about a university or course, including its opportunities.
    """
    def __init__(self, name, location, courses, subjects, scholarships, requisites, areas):
        self.name = name
        self.location = location 
        self.courses = courses
        self.subjects = subjects 
        self.scholarships = scholarships
        self.requisites = requisites 
        self.areas = areas 


    def __str__(self):
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
            f"Scholarships: {scholarships_list}\n"
            f"Requisites: {requisites_list}\n"
            f"Areas: {areas_list}\n"
        )

class Matches:
    """
    Represents a list of university/course matches.
    """
    def __init__(self, matches):
        self.matches = matches  # List of UniInfo objects

    def __str__(self):
        if not self.matches:
            return "No matches found."
        return "\n\n".join([str(match) for match in self.matches])

class UserInfo:
    """
    Represents information about the user and their preferences.
    """
    def __init__(self, name, age, interests, preferred_location, preferred_courses, preferred_subjects, preferred_areas):
        self.name = name  # User's name
        self.age = age  # User's age
        self.interests = interests  # User's interests
        self.preferred_location = preferred_location  
        self.preferred_courses = preferred_courses 
        self.preferred_subjects = preferred_subjects 
        self.preferred_areas = preferred_areas 

    def __str__(self):
        interest_list = ", ".join(self.interests)
        course_list = ", ".join(self.preferred_courses)
        subjects_list = ", ".join(self.preferred_subjects)
        areas_list = ", ".join(self.preferred_areas)
        return (
            f"User Name: {self.name}\n"
            f"Age: {self.age}\n"
            f"Interests: {interest_list}\n"
            f"Preferred Location: {self.preferred_location}\n"
            f"Preferred Courses: {course_list}"
            f"Preferred Subjects: {subjects_list}"
            f"Preferred Areas: {areas_list}"
        )