from util.config import db


class VersionModel(db.Model):

    __tablename__ = 'version'

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(100))

    def __init__(self, version):
        self.version = version

    def __repr__(self):
        return f"{self.version}"
