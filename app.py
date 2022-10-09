from flask import Flask, render_template, send_file, redirect, url_for, abort
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, url
import yt_dlp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GVVHjncacnj_-8y784jfkdkmm9'

class LinkForm(FlaskForm):
    link = URLField('To convert video to mp3 just enter a link here:', validators = [
    url(),
    DataRequired()],
    render_kw={"placeholder": "https://www.youtube.com/watch?v=somthing_here"})
    submit = SubmitField('Get MP3 file')

@app.route('/', methods=['GET', 'POST'])
def index():
    link = None
    form = LinkForm()
    info = None
    file = None

    if form.validate_on_submit():
        try:
         link = form.link.data
         ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'mp3/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',}]
         }
         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
             try:
                 info = ydl.extract_info(link, download=False)
                 file = info['title'] + '.mp3'
                 error_code = ydl.download(link)
             except:
                 return render_template('304.html')
         return redirect(url_for('download', file=file))
        except IndexError:
         abort(404)
         abort(500)
         return render_template('index.html')

    return render_template('index.html', link=link, form=form, info=info, file=file)

@app.route('/download<file>')
def download(file):
    got_file = file
    return send_file(got_file, as_attachment=True)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

@app.errorhandler(404)
def page_not_foud(e):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True)
