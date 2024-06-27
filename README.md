# Flask Task Manager

Flask Task Manager is a web application for managing tasks efficiently. Users can register, log in, create tasks with descriptions and due dates, update tasks, and delete tasks.

## Features

- **User Authentication**: Register and login securely.
- **Task Management**: Create, update, and delete tasks.
- **PDF Export**: Generate and download tasks as a PDF document.

## Technologies Used

- **Flask**: Python web framework for building the application.
- **SQLAlchemy**: ORM (Object-Relational Mapping) for working with the SQLite database.
- **Flask-WTF**: Integration with WTForms for form handling and validation.
- **Bootstrap**: Front-end framework for styling the application.
- **ReportLab**: Python library for PDF generation.

## Setup

### Prerequisites

- Python 3.x installed on your system.
- SQLite database engine.
- Virtual environment (recommended).

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/flask-task-manager.git
   cd flask-task-manager
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Configure the application by setting the environment variables or editing `config.py` file:

   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development  # or 'production' for production environments
   ```

2. Initialize the SQLite database:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

### Running the Application

Run the Flask development server:

```bash
flask run
```

Open a web browser and go to `http://localhost:5000` to view the application.

## Usage

1. **Register**: Create a new account to log in.
2. **Login**: Enter your credentials to access the dashboard.
3. **Dashboard**: Manage tasks, create new tasks, update existing tasks, and delete tasks.
4. **PDF Export**: Download your task list as a PDF document.
