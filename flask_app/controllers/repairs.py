from flask import render_template,redirect,session,request, url_for, flash
from flask_app import app
from flask_app.models import repair
# test comit
@app.route('/new_repair')
def request_repair():
    return render_template('techrepair_create.html')

@app.route('/repair_submission', methods=['POST'])
def request_submit(): 
    if not repair.Repair.validate(request.form):
        return redirect('/new_repair')
    data = {
        'name' : request.form['name'],
        'location' : request.form['location'],
        'description' : request.form['description'],
        'user_id_posted' : request.form['user_id_posted'],
        # 'user_id_worker' : request.form['user_id_worker']
    }
    repair.Repair.save(data)
    # flash("Success! Your reapir has been created.", "success")
    return redirect('/user_dashboard')

@app.route('/delete_repair/<int:id>')
def destroy(id):
    data = {
        'id' : id
    }
    repair.Repair.delete(data)
    flash("Success! Your reapir has been deleted.", "success")
    return redirect('/user_dashboard')

@app.route('/become_worker', methods =['POST'])
def update_driver():
    data = {
        'repair_id' : request.form['repair_id'],
        'user_id_worker' : session['user_id']
    }
    repair.Repair.become_worker(data)
    return redirect('/user_dashboard')

@app.route('/detail_page/<int:id>')
def show_details(id):
    data = {
        'id' : id
    }
    return render_template('view_job.html',repair=repair.Repair.get_one_with_users(data))

@app.route('/edit_job/<int:id>')
def display_edit_page(id):
    data = {
        'id' : id
    }
    return render_template('edit_job.html', repair = repair.Repair.get_one_by_id(data))

@app.route('/submit_update', methods = ['POST'])
def update_the_details():
    data = {
        'repair_id' : request.form['repair_id'],
        'location' : request.form['location'],
        'destination' : request.form['destination']
    }
    repair.Repair.update(data)
    flash("Success! Your repair has been changed.", "success")
    return redirect(f'/user_dashboard/{data["repair_id"]}')

@app.route('/cancel_repair/<int:id>')
def worker_canceled(id):
    data = {
        'repair_id' : id
    }
    repair.Repair.worker_cancel(data)
    return redirect('/user_dashboard')