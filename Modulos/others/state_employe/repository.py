from extensions import db
from Modulos.others.state_employe.models import StateEmploye


class StateEmployeRepository:
    @staticmethod
    def get_all():
        return StateEmploye.query.all()

    @staticmethod
    def get_by_id(item_id):
        return StateEmploye.query.get(item_id)

    @staticmethod
    def create(name):
        new_item = StateEmploye(name=name)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    @staticmethod
    def update(item, new_name):
        item.name = new_name
        db.session.commit()
        return item

    @staticmethod
    def delete(item):
        db.session.delete(item)
        db.session.commit()
