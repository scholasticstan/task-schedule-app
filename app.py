from flask import Flask, abort, flash, redirect, render_template, request, jsonify, session, url_for
from models import storage
import bcrypt
import json
import requests
from models.user import User
from models.task import Task


app = Flask(__name__)
app.config['SECRET_KEY'] = 'os.urandom(32)'  # Replace with your secret key


def order_task_by_priority(list_of_task):
    low = []
    medium = []
    high = []
    for task in list_of_task:
        if task.priority == 'low':
            low.append(task)
        elif task.priority == 'medium':
            medium.append(task)
        else :
            high.append(task)
    return low + medium + high
@app.teardown_appcontext
def teardown_db(exception):
    """Close the database at the end of the request."""
    storage.close()

@app.route('/', strict_slashes=False)
@app.route('/index', strict_slashes=False)
def index():
    """The homepage of the application."""    
    return render_template('index.html')
  
@app.route('/login', strict_slashes=False)
def login():
    """The homepage of the application."""    
    return render_template('login.html')

@app.route('/register', strict_slashes=False)
def reg():
    """The homepage of the application."""    
    return render_template('register.html')
 
@app.route('/login/user', methods=['POST'], strict_slashes=False)
def login_user():
    """Render the Login page."""
    url = "http://127.0.0.1:5100/api/v1/users/verify"
    print("Debug is here")  
    if "email" not in request.form or "password" not in request.form:
      abort(400)    
    email = request.form['email']
    password = request.form['password']    
    obj = {
        'email': email,
        'password': password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    print(obj)
    response = requests.post(url, json=obj, headers=headers)
    print("Hi", response.status_code)
    if response.status_code == 201:
        # just remember, we need to render this page base on his credentials
        flash("Successfully logged in", "success")
        user_id = response.json().get('id')
        user_obj = storage.get(User, user_id)     
        return redirect(url_for('get_task', user_id=user_id))
    else:
        flash("Wrong email or password", "danger")
        return render_template('login.html')
    
@app.route('/register', strict_slashes=False)
def register():
    """Render the Register page."""
    return render_template('register.html')

@app.route('/register/new', methods=['POST'], strict_slashes=False)
def register_new():
    """Render the Register page."""
    # data = request.form.json()
    # name = data.get('name')
    # email = data.get('email')
    # password = data.get('password')
    # confirm_password = data.get('confirm_password')
    # or
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        flash("Password mismatch", "danger")
        return "Password mismatch", (400)
    obj = {
        'name': name,
        'email': email,
        'password': password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    print("laaaapllaaaaaaaapaaaaaaaaaaapaaaaaaaaap")
    url = "http://127.0.0.1:5100/api/v1/users"
    response = requests.post(url, json=obj, headers=headers)
    print("HI: ", response.status_code)
    if response.status_code == 200:
        flash("Successfully registered", "success")
        return render_template('login.html')
    else:
        flash("Email already exists", "danger")
        return render_template('login.html')
    

@app.route('/edit_user/<user_id>', strict_slashes=False)
def edit_user(user_id):
  """Render the edit page with necessary information to Edit a model."""
  get_users = storage.get(User, user_id)
  """Render the edit page with necessary information to Edit a tasks."""
  return render_template('profile.html', user=get_users)
 


@app.route('/update_user/<user_id>', methods=['POST'], strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    # print(password,'*************************************')
    url = f"http://127.0.0.1:5100/api/v1/users/{user_id}"
    if password :
        obj = {
            'name': name ,
            'email': email,
            'password': password

            }
    else :
        obj = {
            'name': name ,
            'email': email,

            }

    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.put(url, json=obj, headers=headers)
    if response.status_code == 200:
        flash(f"User Information Successfully updated", 'success')

        return redirect(url_for('login'))
    else:
        
        flash("Faile to update credentials check your info ", "danger")
        return render_template('profile.html', user=user)
    pass
 
@app.route('/user/<user_id>/tasks/search/',methods=['POST'], strict_slashes=False)
def search_task(user_id):
    """search for tasks by name."""
    name = request.form.get('name')

    user_task = storage.get(User, user_id).tasks
    user = storage.get(User, user_id)
    
    filtried_task = [task  for task in user_task if name.lower() in task.name.lower()] if name != '' else user_task
    filtried_task = order_task_by_priority(filtried_task)
    return render_template('tasks.html', tasks=filtried_task, user=user,user_id=user_id)


@app.route('/user/<user_id>/tasks', strict_slashes=False)
def get_task(user_id):
    """Render the tasks page."""
    user_task = order_task_by_priority(storage.get(User, user_id).tasks)
    user = storage.get(User, user_id)
    # print(user_task[0])
    return render_template('tasks.html', tasks=user_task, user=user,user_id=user_id)

  
@app.route('/create_task/<user_id>', methods=['POST'], strict_slashes=False)
def create_task(user_id):
    user_task = storage.get(User, user_id).tasks

    """Get the properties of this new obj instance of tasks create this obj via API"""
    name = request.form['name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    stop_time = request.form['stop_time']
    status = request.form['status']
    priority = request.form['priority']
    
    url = f"http://127.0.0.1:5100/api/v1/users/{user_id}/tasks"
    obj = {
        'name': name,
        'start_date': start_date,
        'end_date': end_date,
        'stop_time': stop_time,
        'status': status,
        'priority': priority
        }
    headers = {
        'Content-Type': 'application/json'
    }
    print("Hi from front end :", obj)
    data = requests.post(url, json=obj, headers=headers)
    # validate status code
    if data.status_code == 201:
        flash("tasks created successfully", "success")
        return redirect(url_for ('get_task', user_id=user_id) )
    else:
        flash("Failed to create tasks, It's already Exist you can try to update or us different Name", "danger")
        return render_template('add_task.html', user_id=user_id)


@app.route('/add_tasks/<user_id>', strict_slashes=False)
def add_task(user_id):
  """ Render the tasks page for Adding a new obj insance"""
  return render_template('add_task.html',user_id=user_id)



@app.route('/edit_task/<task_id>', strict_slashes=False)
def edit_task(task_id):
  get_tasks = storage.get(Task, task_id)
  """Render the edit page with necessary information to Edit a tasks."""
  return render_template('edit_task.html', task=get_tasks)

@app.route('/update_task/<task_id>', methods=['POST'], strict_slashes=False)
def update_task(task_id):
    user_id = storage.get(Task, task_id).user_id
    
    name = request.form['name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    stop_time = request.form['stop_time']
    status = request.form['status']
    priority = request.form['priority']
    
    url = f"http://127.0.0.1:5100/api/v1/tasks/{task_id}"
    obj = {
        'name': name,
        'start_date': start_date,
        'end_date': end_date,
        'stop_time': stop_time,
        'status': status,
        'priority': priority
        }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.put(url, json=obj, headers=headers)
    if response.status_code == 200:
        flash(f"Task Successfully updated1", 'success')

        return redirect(url_for('get_task', user_id=user_id))
    else:
        flash("Faile to update credentials", "danger")
        return redirect(url_for('get_task', user_id=user_id))
    pass
 

  
@app.route('/delete_task/<task_id>', methods=['GET'], strict_slashes=False)
def delete_task(task_id):
  """Delete a tasks."""
  user_id = storage.get(Task, task_id).user_id

  url = f"http://127.0.0.1:5100/api/v1/tasks/{task_id}"
  obj = storage.get(Task, task_id)
  response = requests.delete(url)
  storage.save()
  if response.status_code == 200:
    flash(f"Task '{obj.name }' successfully deleted!", 'success')
    return redirect(url_for('get_task', user_id=user_id))
  else:
    abort(500)
@app.route("/logout")
def logout():
    # Clear session data
    session.clear()

    # Redirect to the login page
    return redirect(url_for("login"))

@app.route('/search', strict_slashes=False)
def search():
    """The homepage of the application."""    
    return render_template('search.html')



if __name__ == '__main__':
    app.run(debug=True)
