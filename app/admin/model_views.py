from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class MyModelView(ModelView):
    can_view_details = True
    column_display_pk = True

    def is_accessible(self):
        return True
        # return current_user.is_authenticated
