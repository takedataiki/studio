from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from flask_migrate import Migrate
from models import db, Channels, Videos, Original
import module
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cover.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

@app.route('/')
def studios():
    channels = Channels.query.all()

    studio_list = list(set(channel.studio for channel in channels))

    return render_template('studios.html', channels=channels, studio_list=studio_list)

@app.route('/search_channel', methods=['GET', 'POST'])
def search_channel():
    results = []
    channels = Channels.query.all()
    studio_list = list(set(channel.studio for channel in channels))

    if request.method == 'POST':
        query = request.form['query-input']
        results = module.channel_search(query)

    return render_template('channel.html', results=results, studio_list=studio_list)

@app.route('/add_channel/<channel_id>', methods=['POST'])
def add_channel(channel_id):
    studio = request.form['studio']
    if studio == 'other':
        studio = request.form['new_studio']
    new_channel = Channels(
        channel_id = channel_id,
        studio = studio,
        channel_name = request.form['title'],
        channel_description = request.form['description'],
        channel_publishedAt = request.form['publishedAt'],
        channel_thumbnails = request.form['thumbnails']
    )
    db.session.add(new_channel)
    db.session.commit()

    video_ids = []

    next_page_token = None

    while True:
        response = module.channel_videos(channel_id, next_page_token)

        items = response.get('items', [])
        print(len(items))
        video_ids.extend([
            item['id']['videoId']
            for item in items
            if '歌ってみた' in item['snippet']['title'] or 'cover' in item['snippet']['title'].lower()
        ])

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    for video_id in video_ids:
        detail = module.video_detail(video_id)['items'][0]

        existing_video = Videos.query.filter_by(video_id=video_id).first()

        if not existing_video:
            if 'M' in detail['contentDetails']['duration'] and detail['contentDetails']['duration'] != 'PT1M':
                new_video = Videos(
                    video_id = video_id,
                    title = detail['snippet']['title'],
                    description = detail['snippet']['description'],
                    channel_id = detail['snippet']['channelId'],
                    published_at = detail['snippet']['publishedAt'],
                    thumbnail_url = detail['snippet']['thumbnails']['high']['url'],
                    view_count = int(detail['statistics']['viewCount']),
                    duration = detail['contentDetails']['duration']
                )
                db.session.add(new_video)
                db.session.commit()            

    return redirect(url_for('studios'))

@app.route('/search_videos/<channel_id>')
def channel_videos(channel_id):
    channel_videos = Videos.query.filter_by(channel_id=channel_id).all()
    channel = Channels.query.filter_by(channel_id=channel_id).first()

    return render_template('videos.html', channel_videos=channel_videos, channel=channel)

@app.route('/original_update')
def original_update():
    with app.app_context():
        Original.__table__.drop(db.engine)
        db.create_all()

    original_videodata = []
    youtube_url_pattern = r'(?:https://www\.youtube\.com/watch\?v=|https://youtu\.be/)([a-zA-Z0-9_-]{11})'

    cover_videos = Videos.query.all()

    for cover_video in cover_videos:
        description = cover_video.description

        found_video_ids = re.findall(youtube_url_pattern, description)

        for video_id in found_video_ids:
            original_videodata.append((cover_video.channel_id, video_id))

    for cover_channelid, original_videoid in original_videodata:
        original = Original.query.filter_by(video_id=original_videoid).first()
        if not original:
            response = module.video_detail(original_videoid)['items']

            if response:
                video_data = response[0]

                if cover_channelid != video_data['snippet']['channelId']:
                    new_original = Original(
                        video_id = original_videoid,
                        title = video_data['snippet']['title'],
                        description = video_data['snippet']['description'],
                        channel_name = video_data['snippet']['channelTitle'],
                        published_at = video_data['snippet']['publishedAt'],
                        thumbnail_url = video_data['snippet']['thumbnails']['high']['url'],
                        view_count = int(video_data['statistics']['viewCount']),
                        duration = video_data['contentDetails']['duration']
                    )
                    db.session.add(new_original)
                    db.session.commit()
        else:
            original.count += 1
            db.session.commit()
    
    original_videos = Original.query.all()
    return render_template('original.html', original_videos=original_videos)

@app.route('/original_videos')
def original_videos():
    originals = Original.query.order_by(Original.count.desc()).all()
    return render_template('original.html', original_videos=originals)

@app.route('/covers/<original_id>')
def covers(original_id):
    covers = Videos.query.filter(Videos.description.contains(original_id)).all()
    original = Original.query.filter_by(video_id=original_id).first()
    
    return render_template('covers.html', covers=covers, original=original)

@app.route('/delete_channel/<channel_id>')
def delete_channel(channel_id):
    channel = Channels.query.filter_by(channel_id=channel_id).first()
    if channel:
        db.session.delete(channel)
        db.session.commit()
    return redirect(url_for('studios'))

@app.route('/delete_original/<video_id>')
def delete_original(video_id):
    original = Original.query.filter_by(video_id=video_id).first()
    if original:
        db.session.delete(original)
        db.session.commit()
    return redirect(url_for('original_videos'))

if __name__ == '__main__':
    app.run(debug=True)