from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from forms import FreelancerForm, ClientForm, JobForm
from extensions import db
from sqlalchemy import text

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///freelance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from models import Freelancer, Client, Job

@app.route('/')
def home():
    return redirect('/freelancers')

# Freelancers CRUD
@app.route('/freelancers')
def freelancers():
    all_freelancers = Freelancer.query.all()
    return render_template('freelancers.html', freelancers=all_freelancers)

@app.route('/freelancer/add', methods=['GET', 'POST'])
def add_freelancer():
    form = FreelancerForm()
    if request.method == 'POST' and form.validate():
        try:
            new_freelancer = Freelancer(
                name=form.name.data,
                email=form.email.data,
                skills=form.skills.data,
                availability=form.availability.data
            )
            db.session.add(new_freelancer)
            db.session.commit()
            return redirect('/freelancers')
        except Exception as e:
            db.session.rollback()
            print(f"Error adding freelancer: {e}")
    return render_template('add_freelancer.html', form=form)


@app.route('/freelancer/edit/<int:id>', methods=['GET', 'POST'])
def edit_freelancer(id):
    freelancer = Freelancer.query.get_or_404(id)
    form = FreelancerForm(obj=freelancer)
    if request.method == 'POST' and form.validate():
        form.populate_obj(freelancer)
        db.session.commit()
        return redirect('/freelancers')
    return render_template('edit_freelancer.html', form=form, freelancer=freelancer)

@app.route('/freelancer/delete/<int:id>')
def delete_freelancer(id):
    freelancer = Freelancer.query.get_or_404(id)
    db.session.delete(freelancer)
    db.session.commit()
    return redirect('/freelancers')

# Clients CRUD
@app.route('/clients')
def clients():
    all_clients = Client.query.all()
    return render_template('clients.html', clients=all_clients)

@app.route('/client/add', methods=['GET', 'POST'])
def add_client():
    form = ClientForm()
    if request.method == 'POST' and form.validate():
        client = Client(name=form.name.data, email=form.email.data)
        db.session.add(client)
        db.session.commit()
        return redirect('/clients')
    return render_template('add_client.html', form=form)

@app.route('/client/edit/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    client = Client.query.get_or_404(id)
    form = ClientForm(obj=client)
    if request.method == 'POST' and form.validate():
        form.populate_obj(client)
        db.session.commit()
        return redirect('/clients')
    return render_template('edit_client.html', form=form, client=client)

@app.route('/client/delete/<int:id>')
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    return redirect('/clients')

# Jobs CRUD
@app.route('/jobs')
def jobs():
    all_jobs = Job.query.all()
    return render_template('jobs.html', jobs=all_jobs)

@app.route('/job/add', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    form.client_id.choices = [(c.id, c.name) for c in Client.query.all()]
    if request.method == 'POST' and form.validate():
        job = Job(
            title=form.title.data,
            description=form.description.data,
            pay_rate=form.pay_rate.data,
            date_posted=datetime.now().date(),
            client_id=form.client_id.data  
        )
        db.session.add(job)
        db.session.commit()
        return redirect('/jobs')
    return render_template('add_job.html', form=form)

@app.route('/job/edit/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    job = Job.query.get_or_404(id)
    form = JobForm(obj=job)
    form.client_id.choices = [(c.id, c.name) for c in Client.query.all()]
    if request.method == 'POST' and form.validate():
        form.populate_obj(job)
        job.client_id = form.client_id.data
        db.session.commit()
        return redirect('/jobs')
    return render_template('edit_job.html', form=form, job=job)

@app.route('/job/delete/<int:id>')
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect('/jobs')

# Reports

@app.route('/report', methods=['GET'])
def report():
    skill = request.args.get('skill', '')
    availability = request.args.get('availability', '')

    sql = "SELECT * FROM freelancer WHERE 1=1" #1
    params = {}
    if skill:
        sql += " AND skills LIKE :skill" #2
        params["skill"] = f"%{skill}%"
    if availability:
        sql += " AND availability = :availability" #3
        params["availability"] = availability
    freelancers = db.session.execute(text(sql), params).fetchall() #4

    count_sql = "SELECT COUNT(*) FROM freelancer WHERE 1=1"
    count_params = {}
    if skill:
        count_sql += " AND skills LIKE :skill"
        count_params["skill"] = f"%{skill}%"
    if availability:
        count_sql += " AND availability = :availability"
        count_params["availability"] = availability
    total = db.session.execute(text(count_sql), count_params).scalar()


    avail_sql = "SELECT availability, COUNT(*) AS count FROM freelancer WHERE 1=1"
    if skill:
        avail_sql += " AND skills LIKE :skill"
    if availability:
        avail_sql += " AND availability = :availability"
    avail_sql += " GROUP BY availability"
    avail_counts = db.session.execute(text(avail_sql), params).fetchall()

    most_common_avail = None
    if avail_counts:
        most_common_avail = max(avail_counts, key=lambda x: x.count).availability

    return render_template('report.html',
        freelancers=freelancers,
        total=total,
        most_common_avail=most_common_avail
    )



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
