from Web import db
from datetime import date
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    requests = db.relationship('UserRequest', backref='user')

class UserRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.Date, default=date.today)
    end_date =db.Column(db.Date)
    task_name = db.Column(db.String(5000))
    task_desc = db.Column(db.String(5000))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'start_date': self.date.isoformat(),
            'end_date': self.date.isoformat(),
            'task_name': self.task_name,
            'task_desc': self.task_desc
        }
