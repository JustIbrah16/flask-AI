from extensions import db
from Modulos.others.areas.models import Area 

class AreaRepository:
    @staticmethod
    def get_all():
        return Area.query.all()
    
    @staticmethod
    def get_by_id(area_id):
        return Area.query.get(area_id)

    @staticmethod
    def create(name):
        new_area = Area(name=name)
        db.session.add(new_area)
        db.session.commit()
        return new_area

    @staticmethod
    def update(area, new_name):
        area.name = new_name
        db.session.commit()
        return area

    @staticmethod
    def delete(area):
        db.session.delete(area)
        db.session.commit()
