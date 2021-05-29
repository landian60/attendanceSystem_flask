class CheckInRecordForTeacher:

    def __init__(self, tup):
        self.stu_id = tup[0]
        self.stu_name = tup[1]
        self.time = tup[2]

    @property
    def serialize(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'time': self.time,
        }
