class CheckInRecordForStudent:

    def __init__(self, tup):
        self.course_id = tup[0]
        self.course_name = tup[1]
        self.time = tup[2]
    @property
    def serialize(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'time': self.time,
        }


class CourseInfoForStudent:

    def __init__(self, tup):
        self.course_id = tup[0]
        self.course_name = tup[1]
        self.teacher_name = tup[2]
        self.teacher_id = tup[3]

    @property
    def serialize(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'teacher_name': self.teacher_name,
            'teacher_id': self.teacher_id,
        }

