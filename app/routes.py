from app import app
from app.forms import UsernameForm
from flask import render_template, flash, redirect
from app.librarian import Librarian
import time

@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')


@app.route('/comments', methods=['GET', 'POST'])
def comments():

    form = UsernameForm()
    if form.validate_on_submit():

        lib_obj = Librarian()
        lib_obj.praw_auth()

        bodies, links, archive = lib_obj.comment_scrape(form.username.data, write_to_file=form.with_download.data, with_archive=form.with_archive.data)

        if len(archive) != 0:
            return render_template('iteratorTriple.html', data=zip(bodies, links, archive))

        return render_template('iteratorDouble.html', data=zip(bodies, links))

    return render_template('commentInput.html', form=form)


@app.route('/submissions', methods=['GET', 'POST'])
def submissions():

    form = UsernameForm()
    if form.validate_on_submit():

        lib_obj = Librarian()
        lib_obj.praw_auth()

        bodies, links, archive = lib_obj.submission_scrape(form.username.data, write_to_file=form.with_download.data, with_archive=form.with_archive.data)

        if len(archive) != 0:
            return render_template('iteratorTriple.html', data=zip(bodies, links, archive))

        return render_template('iteratorDouble.html', data=zip(bodies, links))

    return render_template('submissionInput.html', form=form)
