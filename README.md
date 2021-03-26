# LearnGlish

## This is CS50 final project for Harvard University created by Oleksandr Volkov

### LearnGlish is a modern, dynamic and flexible tool for learning English.

With this website, you can easily and quickly customize the study of English words and phrases.

Almost everyone knows and has been scientifically proven that learning a foreign language does not begin with grammar but with expanding the vocabulary, and only then comes grammar and spelling.

Many modern technologies and frameworks were used to write this project, such as:

- **Python (Flask)** - as the main tool for creating a web application in the programming language Python. Used to write a backend, most of the logic of the website is written on it.
- **JavaScript (JQuery)** - was used as an additional tool for fast and dynamic access to program objects and retrieving data from the server without reloading the page.
- **Bootstrap** - powerful tool for using ready-made solutions for visual components. The project used such components as forms, buttons, navigation panel, etc. And also for responsive on different screens (desktop, tablet and mobile).
- **HTML** - used to indicate the structure of elements on the website.
- **CSS** - used to stylize custom objects in the project.
- **SQLite3 (SQLAlchemy)** - used to create a project database, to store user data. And ORM for convenient work with the database
- **etc ...** -

### Database structure

![alt text](https://github.com/VolkovOleksandr/LearnGlish/blob/main/static/img/db.png "DB")

The structure of the database consists of 6 tables such as:

- uerss: used to store personal data of users such as email, password, name.
- topics: this table is used to store topics.
- topic_identifier: used to unite users with their topics (many to many).
- vocabularys: used to store words and phrases.
- news: this table is used to store news and which are displayed on the index page of the project.
- progress: progress table of each user.

### Index page

Byde foto
The main page of the project. This web page has the following structure:

- Navigation Bar on the top of the website: the manu is used to navigate the site - "Home, Sdudy it, My progress,Sign In / Sign Out, Register and Admin panel wich is only available to the administrator" (Dublicated on each page).
- In the BODY of the site there are 2 blocks:
  - The first of which Carousel: a slideshow for cycling through of content representing website.
  - The second is a block of news (Cards), it displays all the news that is on the site. Clicking on read more opens the news page.
- Also from the bottom is a footer block. Where is the information about the project and who is its developer(Dublicated on each page).
