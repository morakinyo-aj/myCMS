from flask import render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import login_required, current_user
from forms.content import ContentForm
from werkzeug.utils import secure_filename
from models.models import Content, User
import datetime
from config import Config
from utils import db, generate_hashtags
from classifier import predict_video_tag
import os
import videodb

conn = videodb.connect(Config.VIDEODB_API_KEY)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def init_main_routes(app):
    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/dashboard", methods=['GET','POST'])
    @login_required
    def dashboard():
        form = ContentForm()
        search_query = request.args.get('search', '').strip()
        if search_query:
            user_content = Content.query.filter(
                Content.user_id == current_user.id,
                Content.title.ilike(f"%{search_query}%")
            ).all()
        else:
            user_content = Content.query.filter_by(user_id=current_user.id).all()
        if form.validate_on_submit():
            try:
                file = form.file.data
                filename = secure_filename(file.filename)
                unique_filename = f"{datetime.datetime.now().timestamp()}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                file.save(filepath)
                
                ext = filename.rsplit('.', 1)[1].lower()
                content_type = 'video' if ext in {'mp4', 'mov'} else 'image'
                
                tags_data = form.tags.data
                if content_type == 'video':
                    predicted = predict_video_tag(filepath)
                    if predicted:
                        tags_data = ", ".join(generate_hashtags(predicted))

                # Save to db
                new_content = Content(
                    title=form.title.data,
                    description=form.description.data,
                    filename=unique_filename,
                    filepath=filepath,
                    user_id=current_user.id,
                    content_type=content_type,
                    tags=tags_data
                )
                
                db.session.add(new_content)
                db.session.commit()
                flash('Content uploaded successfully!', 'success')
                return redirect(url_for('dashboard'))
            
            except Exception as e:
                db.session.rollback()
                flash(f'Error uploading file: {str(e)}', 'error')
                app.logger.error(f"Upload error: {str(e)}")
        return render_template('dashboard.html', form=form, content=user_content, username = current_user.username)
    

    @app.route('/upload/<filename>')
    @login_required
    def upload(filename):
        # conn.upload(filename)
        return(send_from_directory(app.config['UPLOAD_FOLDER'], filename))

    @app.errorhandler(404)
    def pageNotFound(error):
        return render_template('NotFound.html'), 404

    @app.errorhandler(500)
    def serverError(error):
        return "Could not process your request", 500