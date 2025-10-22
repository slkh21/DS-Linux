from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Video, Task, Progress

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('index'))
        return "Неверный логин или пароль"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def is_teacher():
    return session.get('role') == 'teacher'

@app.route('/videos')
def videos():
    video_list = Video.query.all()
    return render_template('videos.html', videos=video_list)

@app.route('/tasks')
def tasks():
    task_list = Task.query.all()
    return render_template('tasks.html', tasks=task_list)

@app.route('/add_video', methods=['GET', 'POST'])
def add_video():
    if not is_teacher():
        return "Доступ только для учителей", 403
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        new_video = Video(title=title, url=url)
        db.session.add(new_video)
        db.session.commit()
        return redirect(url_for('videos'))
    return render_template('add_video.html')

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if not is_teacher():
        return "Доступ только для учителей", 403
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        new_task = Task(question=question, answer=answer)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('tasks'))
    return render_template('add_task.html')

if __name__ == '__main__':
    app.run(debug=True)
