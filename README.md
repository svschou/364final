# SI 364 - Winter 2018 - Final Project
## Stephanie Schouman

## My Project

In this Harry Potter-themed project, a user will be able to explore Hogwarts by searching for different Hogwarts students and save them in their very own Marauder's Map. Or a user can search for different spells and save them to their own Spellbook. At any time the user can also update or delete any students or spells they don't want. By clicking on the Sorting Hat feature, a user will be sorted into one of the four Hogwarts houses.

## Installation Requirements
* `flask` library and all `flask`-related modules used in SI364 (flask,flask_script,flask_sqlalchemy,flask_login,flask_wtf)
* `bs4` - used in scraping HTML data using BeautifulSoup

## How to run application:
* `cd` to directory where SI364final.py lives
* Run using `python SI364final.py runserver`
* You should see a home page asking you to either log in or register
* Log in (or register and then log in)
* From here, you should be able to do one of 3 tasks:
	
	* Enter a Hogwarts students name into the name field and an affiliation with this student into the second field. The name field requires a first and last name, as well as formal names ('Ronald Weasley' vs 'Ron Weasley' or 'Ginerva Weasley' vs 'Ginny Weasley'). The affiliation can be any string, though I've been using 'friend', 'study buddy', 'potions partner', etc.
		* This should redirect you to the Marauder's Map page. To continue adding students, go back to the Home page.
		* Example student names: Harry Potter, Hermione Granger, Neville Longbottom, Draco Malfoy, Luna Lovegood, Cho Chang

	* Enter a spell name into the spell field to search for that spell. This should redirect you to the Spellbook page. To continue adding spells, go back to the Home page
		* Example spell names: Accio, Lumos, Nox, Alohomora, Expecto Patronum, Wingardium Leviosa

	* Click the Sorting Hat link to be sorted into a Hogwarts house. This should redirect you to the Sorting Hat page, where you will click the "Click here to be sorted into a Hogwart house" button
		* Each user can only be sorted once. If you have already been sorted, you can still use the same path to see your house, but it will read "You have already been sorted" and display your house.

## Routes 
* `/` --> `index.html`
* `/login` --> `login.html`
* `/logout` --> `logout.html`
* `/register` --> `register.html`
* `/sorting_hat` --> `sorting_hat.html`
* `/sorting_results` --> `sorting_results.html`
* `/show_students` --> `show_students.html`
* `/show_spells` --> `show_spells.html`
* `/update_student/<student>` --> `update_student.html`, or `show_students.html`
* `/delete_student` --> deletes student, redirects to `show_students`
* `/delete_spell` --> --> deletes spell, redirects to `show_students`


## Differences from Midterm
My midterm project only allowed for a user to search and save Hogwarts students. This projects adds elements like spells and a sorting_hat feature, as well as an affilication attribute for the Hogwarts students. 

## **Documentation README Requirements**

- [x] **Create a `README.md` file for your app that includes the full list of requirements from this page. The ones you have completed should be bolded or checked off.**

- [x] **The `README.md` file should use markdown formatting and be clear / easy to read.**

- [x] **The `README.md` file should include a 1-paragraph (brief OK) description of what your application does**

- [x] **The `README.md` file should include a detailed explanation of how a user can user the running application (e.g. log in and see what, be able to save what, enter what, search for what... Give us examples of data to enter if it's not obviously stated in the app UI!)**

- [x] **The `README.md` file should include a list of every module that must be installed with `pip` if it's something you installed that we didn't use in a class session. If there are none, you should note that there are no additional modules to install.**

- [x] **The `README.md` file should include a list of all of the routes that exist in the app and the names of the templates each one should render OR, if a route does not render a template, what it returns (e.g. `/form` -> `form.html`, like [the list we provided in the instructions for HW2](https://www.dropbox.com/s/3a83ykoz79tqn8r/Screenshot%202018-02-15%2013.27.52.png?dl=0) and like you had to on the midterm, or `/delete -> deletes a song and redirects to index page`, etc).**

### Code Requirements

- [x] **Ensure that your `SI364final.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up).**

- [x] **A user should be able to load `http://localhost:5000` and see the first page they ought to see on the application.**

- [x] **Include navigation in `base.html` with links (using `a href` tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )**

- [x] **Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.**

- [x] **Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).**

- [x] **Must have data associated with a user and at least 2 routes besides `logout` that can only be seen by logged-in users.**

- [x] **At least 3 model classes *besides* the `User` class.**

- [x] **At least one one:many relationship that works properly built between 2 models.**

- [x] **At least one many:many relationship that works properly built between 2 models.**

- [x] **Successfully save data to each table.**

- [x] **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).**

- [x] **At least one query of data using an `.all()` method and send the results of that query to a template.**

- [x] **At least one query of data using a `.filter_by(...` and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).**

- [x] **At least one helper function that is *not* a `get_or_create` function should be defined and invoked in the application.**

- [x] **At least two `get_or_create` functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).**

- [x] **At least one error handler for a 404 error and a corresponding template.**

- [x] **At least one error handler for any other error (pick one -- 500? 403?) and a corresponding template.**

- [x] **Include at least 4 template `.html` files in addition to the error handling template files.**

- [x] **At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.**

- [x] **At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that *does* accord with other involved sites' Terms of Service, etc).**

 - [x] **Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source *to the database* (in some way).**

- [x] **At least one WTForm that sends data with a `GET` request to a *new* page.**

- [] At least one WTForm that sends data with a `POST` request to the *same* page. (NOT counting the login or registration forms provided for you in class.)

- [x] **At least one WTForm that sends data with a `POST` request to a *new* page. (NOT counting the login or registration forms provided for you in class.)**

- [x] **At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.**

- [x] **Include at least one way to *update* items saved in the database in the application (like in HW5).**

- [x] **Include at least one way to *delete* items saved in the database in the application (also like in HW5).**

- [x] **Include at least one use of `redirect`.**

- [x] **Include at least two uses of `url_for`. (HINT: Likely you'll need to use this several times, really.)**

- [x] **Have at least 5 view functions that are not included with the code we have provided. (But you may have more! *Make sure you include ALL view functions in the app in the documentation and navigation as instructed above.*)**

## Additional Requirements for additional points -- an app with extra functionality!

**Note:** Maximum possible % is 102%.

- [] (100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.
- [ ]  (100 points) Create, run, and commit at least one migration.
- [ ] (100 points) Include file upload in your application and save/use the results of the file. (We did not explicitly learn this in class, but there is information available about it both online and in the Grinberg book.)
- [ ]  (100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README. (Heroku deployment as we taught you is 100% free so this will not cost anything.)
- []  (100 points) Implement user sign-in with OAuth (from any other service), and include that you need a *specific-service* account in the README, in the same section as the list of modules that must be installed.

