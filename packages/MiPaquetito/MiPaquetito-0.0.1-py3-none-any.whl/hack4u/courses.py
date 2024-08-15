class Course:

    def __init__(self,name,duration,link):
        self.name = name 
        self.duration = duration 
        self.link = link
    
    def __repr__(self):
        return f"{self.name} [{self.duration} horas] ({self.link})"


courses = [
    Course("Introduccion a Linux",15,"www.google.cl"),
    Course("Personalizacion de Linux",3,"www.google.cl"),
    Course("Introduccion al Hacking", 53,"www.google.cl")
]


def list_courses():

    for course in courses:
        print(course)


def search_course_by_name(name):

    for course in courses:
        if course.name == name:
            return course

    return None
