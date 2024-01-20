from app.models import Asset, Unit, Application
from fab_react_toolkit import ModelRestApi, SQLAInterface
from flask import request, Response
from flask_appbuilder.api import expose, protect, safe, permission_name
from app import appbuilder, db
from typing import Any

class AssetApi(ModelRestApi):
    resource_name = "assets"
    datamodel = SQLAInterface(Asset)
    page_size = 200
    description_columns = {
        'name': 'Name of the asset',
        'owner_id': 'ID of the asset owner',
        'owner': 'Owner of the asset',
        'date_time': 'Date time of the asset',
        'date': 'Date of the asset',
    }
    quick_filters = [
        {
            "name": "asset_name",
            "label": "Asset Name",
            "column": "name",
            "type": "multiselect",
            "options": [{"value": f"asset&{i}", "label": f"asset&{i}"} for i in range(10)]
        }
    ]

    @expose("/bulk/<string:handler>", methods=["PUT"])
    @protect()
    @safe
    @permission_name("bulk")
    def put_bulk(self, handler, **kwargs: Any) -> Response:
        """
            
        """
        id_list = request.get_json()
        print (id_list)
        func = getattr(self, f"bulk_{handler}")
        return func(id_list)

    def bulk_update_time(self, id_list):
        try:
            updated = db.session.query(Asset).filter(Asset.id.in_(id_list)).update({Asset.date_time: db.func.now()}, synchronize_session=False)
            db.session.commit()
            return self.response(200, message=f"Updated {updated} records")
        except Exception as e:
            db.session.rollback()
            print(e)
            return self.response(500, message=str(e))

class ApplicationApi(ModelRestApi):
    resource_name = "applications"
    datamodel = SQLAInterface(Application)
    description_columns = {
        'name': 'Name of the Application',
        'description': 'Description'
    }
    quick_filters = [
        {
            "name": "application_name",
            "label": "Application Name",
            "column": "name",
            "type": "multiselect",
            "options": [{"value": f"application_{i}", "label": f"application_{i}"} for i in range(10)]
        }
    ]


class UnitApi(ModelRestApi):
    resource_name = "units"
    datamodel = SQLAInterface(Unit)
    description_columns = {
        'name': 'Name of the unit'
    }
    quick_filters = [
        {
            "name": "unit_name",
            "label": "Unit Name",
            "column": "name",
            "type": "multiselect",
            "options": [{"value": f"unit_{i}", "label": f"unit_{i}"} for i in range(10)]
        }
    ]

appbuilder.add_api(AssetApi)
appbuilder.add_api(ApplicationApi)
appbuilder.add_api(UnitApi)
