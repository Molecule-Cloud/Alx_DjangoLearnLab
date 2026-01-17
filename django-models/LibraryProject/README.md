# Introduction to Django

Welcome to the **Introduction to Django** project. This project is designed to help you gain hands-on experience with Django, one of the most popular web frameworks for building robust web applications. Throughout this project, you will set up a Django development environment, learn about Django models and ORM, and explore the Django admin interface.

## Objectives

- **Set Up Django Development Environment:** Install Django and create a new Django project. Familiarize yourself with the project's default structure and run the development server.

- **Implementing and Interacting with Django Models:** Create a Django app, define Django models with specified attributes, and perform CRUD operations using Django's ORM via the Django shell.

- **Utilizing the Django Admin Interface:** Register your models with the Django admin and customize the admin interface to enhance the management and visibility of your data.

This structured approach will provide you with a solid foundation in Django, preparing you to develop more complex web applications in the future.

---

## Task 0: Django Development Environment Setup

**Objective:** Gain familiarity with Django by setting up a Django development environment and creating a basic Django project.

### Steps:

1. **Install Django**
   - Ensure Python is installed on your system
   - Install Django using pip:
     ```bash
     pip install django
     ```

2. **Create Your Django Project**
   - Create a new Django project:
     ```bash
     django-admin startproject LibraryProject
     ```

3. **Run the Development Server**
   - Navigate into your project directory:
     ```bash
     cd LibraryProject
     ```
   - Create a README.md file inside the LibraryProject
   - Start the development server:
     ```bash
     python manage.py runserver
     ```
   - Open a web browser and go to `http://127.0.0.1:8000/` to view the default Django welcome page

4. **Explore the Project Structure**
   - Familiarize yourself with the created project structure:
     - `settings.py`: Configuration for the Django project
     - `urls.py`: URL declarations for the project
     - `manage.py`: Command-line utility for interacting with the Django project

---

## Task 1: Implementing and Interacting with Django Models

**Objective:** Demonstrate proficiency in Django by creating a Book model within a Django app and using Django's ORM to perform database operations.

### Steps:

1. **Create the bookshelf App**
   ```bash
   python manage.py startapp bookshelf
   ```

2. **Define the Book Model**
   - Navigate to `bookshelf/models.py`
   - Create a Book class with the following fields:
     - `title`: CharField with a maximum length of 200 characters
     - `author`: CharField with a maximum length of 100 characters
     - `publication_year`: IntegerField

3. **Model Migration**
   - Create migration files:
     ```bash
     python manage.py makemigrations bookshelf
     ```
   - Apply migrations:
     ```bash
     python manage.py migrate
     ```

4. **Interact with the Model via Django Shell**
   - Open the Django shell:
     ```bash
     python manage.py shell
     ```

### CRUD Operations Documentation

Document each operation in separate Markdown files with both the Python command used and its output:

#### Create (`create.md`)
- Create a Book instance with title "1984", author "George Orwell", and publication year 1949
- Document the Python command and expected output

#### Retrieve (`retrieve.md`)
- Retrieve and display all attributes of the book created
- Document the Python command and expected output

#### Update (`update.md`)
- Update the title from "1984" to "Nineteen Eighty-Four"
- Document the Python command and expected output showing the updated title

#### Delete (`delete.md`)
- Delete the book created and confirm deletion
- Document the Python command and expected output confirming deletion

---

## Task 2: Utilizing the Django Admin Interface

**Objective:** Gain practical experience with the Django admin interface by configuring the admin to manage the Book model.

### Steps:

1. **Register the Book Model with Django Admin**
   - Modify `bookshelf/admin.py` to include the Book model

2. **Customize the Admin Interface**
   - Display `title`, `author`, and `publication_year` in the admin list view
   - Configure list filters and search capabilities for Book entries

---

## Project Structure

```
LibraryProject/
├── manage.py
├── LibraryProject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── bookshelf/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    └── views.py
```

---

## Additional Resources

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django Models Documentation](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Admin Site Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)

---

## License

This project is part of a Django learning curriculum.