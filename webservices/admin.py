from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from emannotationschemas.models import AnalysisVersion, AnalysisTable


def setup_admin(app, db):
    admin = Admin(app, name="Mesh-Skeleton-Web-Services")
    admin.add_view(ModelView(AnalysisVersion, db.session))
    admin.add_view(ModelView(AnalysisTable, db.session))
    return admin