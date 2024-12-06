from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Channels(db.Model):
    channel_id = db.Column(db.String(100), primary_key=True)
    studio = db.Column(db.String(100))
    channel_name = db.Column(db.String(100))
    channel_description = db.Column(db.String(100))
    channel_publishedAt = db.Column(db.String(100))
    channel_thumbnails = db.Column(db.String(100))

class Videos(db.Model):
    video_id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    channel_id = db.Column(db.String(100))
    published_at = db.Column(db.String(100))
    thumbnail_url = db.Column(db.String(100))
    view_count = db.Column(db.Integer)
    duration = db.Column(db.String(100))

class Original(db.Model):
    video_id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    channel_name = db.Column(db.String(100))
    published_at = db.Column(db.String(100))
    thumbnail_url = db.Column(db.String(100))
    view_count = db.Column(db.Integer)
    duration = db.Column(db.String(100))
    count = db.Column(db.Integer, default=0)