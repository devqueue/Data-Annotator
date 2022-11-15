# Gene lookup
A web application for gene search built with django using the [django black template](https://github.com/creativetimofficial/black-dashboard-django) by creative tim

<br />

## Data requirements
1. The uploaded CSV files must contain the following columns Chromosome, start, end, referance, observed, refGene gene, zygosity, filename. The application will not process the file unless these columns are found.
2. Rest of the columns are optional and can be included if required. You need to update the `required` list in `apps/utils.py`. these names must match the ones in the CSV
3. Also note that the app will only read these columns from the csv regardless of how many columns are available 
## ✨ Deploy in production using `Docker`

> Get the code

```bash
$ git clone <repo>
$ cd genelookup
```
> Configure environment variables
```
1. Create a .env file and paste the contents. 

DEBUG=1
DB_NAME=dbname
DB_USER=rootuser
DB_PASS=changeme
SECRET_KEY=changeme
ALLOWED_HOSTS=127.0.0.1

2. Change the variables to store real values
3. Allowed hosts can be a comma seperated list of multiple hosts (IP's or domain names)
```
> Start the app in Docker

```bash
$ docker-compose up --build
$ docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

Visit `http://localhost:80` in your browser. The app should be up & running.


<br />

## ✨ How to use it for development
The development deployment provies hot reloading for the code to update in real time

```bash
$ # Get the code
$ git clone <repo>
$ cd genelookup
$
$ 
$ # Docker compose
$ docker-compose -f docker-compose-dev.yml up --build
$
$ # open a new terminal and run 
$ docker-compose -f docker-compose-dev.yml run --rm app sh -c "python manage.py createsuperuser"
$
$ # Access the web app in browser: http://127.0.0.1/
```

<br />

## ✨ Code-base structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- core/                               # Implements app configuration
   |    |-- settings.py                    # Defines Global Settings
   |    |-- wsgi.py                        # Start the app in production
   |    |-- urls.py                        # Define URLs served by all apps/nodes
   |
   |-- apps/
   |    |
   |    |-- home/                          # A simple app that serve HTML files
   |    |    |-- views.py                  # Serve HTML pages for authenticated users
   |    |    |-- urls.py                   # Define some super simple routes  
   |    |
   |    |-- authentication/                # Handles auth routes (login and register)
   |    |    |-- urls.py                   # Define authentication routes  
   |    |    |-- views.py                  # Handles login and registration  
   |    |    |-- forms.py                  # Define auth forms (login and register) 
   |    | 
   |    |-- search/
   |    |    |-- views.py                  # Handles search and export
   |    |    |-- urls.py                   # Define urls for search and export
   |    |    |-- models.py                 # model for the gene storage
   |    | 
   |    |-- upload/
   |    |    |-- urls.py                   # Define upload and compute routes  
   |    |    |-- views.py                  # Handles populating database 
   |    |    |-- forms.py                  # Define upload form
   |    |    |-- models.py                 # model for csv file upload
   |    | 
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>         # CSS files, Javascripts files
   |    |
   |    |-- templates/                     # Templates used to render pages
   |         |-- includes/                 # HTML chunks and components
   |         |    |-- navigation.html      # Top menu component
   |         |    |-- sidebar.html         # Sidebar component
   |         |    |-- footer.html          # App Footer
   |         |    |-- scripts.html         # Scripts common to all pages
   |         |
   |         |-- layouts/                   # Master pages
   |         |    |-- base-fullscreen.html  # Used by Authentication pages
   |         |    |-- base.html             # Used by common pages
   |         |
   |         |-- accounts/                  # Authentication pages
   |         |    |-- login.html            # Login page
   |         |    |-- register.html         # Register page
   |         |
   |         |-- home/                      # UI Kit Pages
   |              |-- index.html            # Index page
   |              |-- 404-page.html         # 404 page
   |              |-- *.html                # All other pages
   |
   |-- requirements.txt                     # Development modules - SQLite storage
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- manage.py                            # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />

## ✨ Recompile CSS

To recompile SCSS files, follow this setup:

<br />

**Step #1** - Install tools

- [NodeJS](https://nodejs.org/en/) 12.x or higher
- [Gulp](https://gulpjs.com/) - globally 
    - `npm install -g gulp-cli`
- [Yarn](https://yarnpkg.com/) (optional) 

<br />

**Step #2** - Change the working directory to `assets` folder

```bash
$ cd apps/static/assets
```

<br />

**Step #3** - Install modules (this will create a classic `node_modules` directory)

```bash
$ npm install
// OR
$ yarn
```

<br />

**Step #4** - Edit & Recompile SCSS files 

```bash
$ gulp scss
```

The generated file is saved in `static/assets/css` directory.

<br /> 

## Future improvement proposals
1. Live table update using ajax
2. Testing time complexity with large number of files. 

## ✨ Credits & Links

### [Django Admin Dashboards](https://appseed.us/admin-dashboards/django)

Index with UI-ready **admin dashboards** generated by the AppSeed platform in [Django Framework](https://www.djangoproject.com/).
Start fast your next Django project by using functional admin dashboards enhanced with Database, ORM, authentication flow, helpers and deployment scripts.

### What is Django

**Django** is a Python-based free and open-source web framework, which follows the model-template-view architectural pattern. It is maintained by the Django Software Foundation, an independent organization established as a 501 non-profit. Django's primary goal is to ease the creation of complex, database-driven websites.

### What is a dashboard

A dashboard is a set of pages that are easy to read and offer information to the user in real-time regarding his business. A dashboard usually consists of graphical representations of the current status and trends within an organization. Having a well-designed dashboard will give you the possibility to act and make informed decisions based on the data that your business provides - *definition provided by [Creative-Tim - Free Dashboard Templates](https://www.creative-tim.com/blog/web-design/free-dashboard-templates/?AFFILIATE=128200)*.

### Black Dashboard

**Black Dashboard** is a beautiful Bootstrap 4 Admin Dashboard with a huge number of components built to fit together and look amazing. If you are looking for a tool to manage and visualize data about your business, this dashboard is the thing for you. It combines colors that are easy on the eye, spacious cards, beautiful typography, and graphics.

<br />