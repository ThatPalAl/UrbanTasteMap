from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app
from app.tasks import process_places

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city')
        place_type = request.form.get('place_type')

        if not city or not place_type:
            flash('All fields are required!')
            return redirect(url_for('index'))

        city_center = (52.2297, 21.0122) 
        radius_km = 5 
        grid_size = 2 

        task = process_places.delay(app.config['GOOGLE_API_KEY'], city_center, radius_km, grid_size, place_type, city)
        return jsonify({'task_id': task.id, 'state': 'PENDING'})

    return render_template('index.html')

@app.route('/status/<task_id>')
def task_status(task_id):
    task = process_places.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('status', ''),
            'result': task.info
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    return jsonify(response)
