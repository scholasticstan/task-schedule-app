# Task Manager Application

alx final project

## Overview

A Task Manager App is a web-based platform designed to help people manage and schedule their tasks based on date and time. It will serve as the single reference point for a complete, calendar of all scheduled tasks for any user

Front End

- HTML
- CSS
- JavaScript

RESTful API

- GET, POST, PUT and DELETE requests handled
- CRUD manipulation through RESTful API

Relational Database

- MySql Handled with ORM (SQLAlchemy)
- Model system with base model handling identification
- Many to many relationships

## Features

The Task Manager APP includes the following key features:

1. **The ability to schedule tasks and activities:** Users can create tasks easily
2. **The ability to easily modify and delete tasks:** Users can view the details and information of the tasks created with the ability to modify and delete as needed.

# Installation

## Dependencies

- This application is written in Python and requires Python 3.11.4 or 3.11.6 to run correctly.
- Use Requirement.txt to install all dependancy library by add this command :( pip install -r requirements.txt)

## Getting Started

- Clone this git repository. If you are a GNU/Linux user, you could copy and paste the
  following command to clone and change the working directory into the root of this project:

```sh
[https://github.com/scholasticstan/task-schedule-app]
```

- Otherwise, clone the repository as you'd like and change the working directory into
  the root of the project.

## Run in your local

- use this command to enter mysql srver (mysql -u root -p ) and enter your password
- use command (source db_setup.sql) to create database name it (task_db)
- use command (python app.py) to run application and create table in to databes
- use command (python -m api.v1.app) to run API

* after all steps you ready to run ( use link http://127.0.0.1:5000) in you browser

## Usage

1. **Create Account in Task Manager Application:**

   - when you run this app you find login page
   - Click on “Sigin in now ” and you will be directed to the Sign in section form
   - Fill thi form by filling use:“Name , Email, Password and Confirm Password ”.
   - when you succefully create account that means you have valid info

2. **Login to your task page:**

   - You will be great when you create account automatically redirection to login page
   - Fill the Login form and Click on “Login” and you will be directed to the tasks page
   - update profile by Click on "edit profile" and you can update any fields you want

3. **Task Management :**
   - Fill form for task (task name , start_date, end_date, time, priority and status ) and click on “Add” button you will see the task as bellow.
   - show task as card dispaly all content and tow buttons (edit & delete) and dispaly remaning time need to cpmplete task
   - Use the “Edit” button to edit task info.
   - Use the “Delete” button to remove task info.

## Authors

<details>
    <summary>Stanley Alu</summary>
    <ul>
    <li><a href="https://www.linkedin.com/in/stanley-alu-62387491/">LinkedIn</a></li>
    <li><a href="https://www.github.com/scholasticstan">GitHub</a></li>
    <li><a href="mailto:alu.uzorka.stanley@gmail.com">Gmail</a></li>
    </ul>
</details>
