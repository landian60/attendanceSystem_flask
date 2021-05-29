class StudentDao:

    @staticmethod
    def query_student_by_uuid(uuid):
        pass

    @staticmethod
    def query_course_by_stu_id(stu_id):
        pass

    @staticmethod
    def add_student(uuid, stu_id, stu_name, phone_number, email):
        pass

    @staticmethod
    def update_student_by_uuid(uuid, stu_name, phone_number, email):
        pass

    @staticmethod
    def add_sc_by_course_id_and_stu_id(course_id, stu_id):
        pass

    @staticmethod
    def query_course_not_taken_by_stu_id(stu_id):
        pass

    @staticmethod
    def delete_sc_by_course_id_and_stu_id(course_id, stu_id):
        pass

    @staticmethod
    def query_task_by_task_id(task_id):
        pass

    @staticmethod
    def add_check_in_record(stu_id, task_id):
        pass

    @staticmethod
    def query_sc_by_course_id_and_stu_id(course_id, stu_id):
        pass

    @staticmethod
    def query_task_by_course_id(course_id):
        pass

    @staticmethod
    def query_check_in_record_by_task_id_and_uuid(task_id, uuid):
        pass


    @staticmethod
    def query_course_by_course_id(course_id):
        pass

    @staticmethod
    def query_check_in_record_by_stu_id(stu_id):
        pass
