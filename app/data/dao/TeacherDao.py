class TeacherDao:

    @staticmethod
    def query_teacher_by_uuid(uuid):
        pass

    @staticmethod
    def query_teacher_by_teacher_id(teacher_id):
        pass

    @staticmethod
    def query_student_by_course_id(course_id):
        pass

    @staticmethod
    def query_student_by_task_id_and_course_id(task_id, course_id):
        pass

    @staticmethod
    def query_course_by_teacher_id(teacher_id):
        pass

    @staticmethod
    def query_task_by_course_id_and_now_time(course_id):
        pass

    @staticmethod
    def query_check_in_record_for_teacher_by_task_id_and_course_id(task_id, course_id):
        pass

    @staticmethod
    def add_teacher(uuid, teacher_id, teacher_name, phone_number, email):
        pass

    @staticmethod
    def update_teacher_by_uuid(uuid, teacher_name, phone_number, email):
        pass

    @staticmethod
    def add_course(course_id, course_name, course_intro, teacher_id):
        pass

    @staticmethod
    def add_check_in_task(course_id, start_time, end_time):
        pass
