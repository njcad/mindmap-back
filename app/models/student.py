class Student:
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.submissions = {}
        self.email = email