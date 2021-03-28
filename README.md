# LearnGlish

## This is CS50 final project for Harvard University created by Oleksandr Volkov

### LearnGlish is a modern, dynamic and flexible tool for learning English.

#### Check it out! On the YouTube

<a href="http://www.youtube.com/watch?feature=player_embedded&v=hoKPcnjr0Zs
" target="_blank"><img src="http://img.youtube.com/vi/hoKPcnjr0Zs/0.jpg" 
alt="LearnGlish" width="500" height="180" border="10" /></a>

With this website, you can easily and quickly customize the study of English words and phrases.

Almost everyone knows and has been scientifically proven that learning a foreign language does not begin with grammar but with expanding the vocabulary, and only then comes grammar and spelling.

Many modern technologies and frameworks were used to write this project, such as:

- _Python (Flask)_ - as the main tool for creating a web application in the programming language Python. Used to write a backend, most of the logic of the website is written on it.
- _JavaScript (JQuery)_ - was used as an additional tool for fast and dynamic access to program objects and retrieving data from the server without reloading the page.
- _Bootstrap_ - powerful tool for using ready-made solutions for visual components. The project used such components as forms, buttons, navigation panel, etc. And also for responsive on different screens (desktop, tablet and mobile).
- _HTML_ - used to indicate the structure of elements on the website.
- _CSS_ - used to stylize custom objects in the project.
- _SQLite3 (SQLAlchemy)_ - used to create a project database, to store user data. And ORM for convenient work with the database
- _etc ..._ -

### Database structure

![alt text](https://github.com/VolkovOleksandr/LearnGlish/blob/main/static/img/db.png "DB")

The structure of the database consists of 6 tables such as:

- **uerss:** used to store personal data of users such as email, password, name.
- **topics:** this table is used to store topics.
- **topic_identifier:** used to unite users with their topics (many to many).
- **vocabularys:** used to store words and phrases.
- **news:** this table is used to store news and which are displayed on the index page of the project.
- **progress:** progress table of each user.

### Index page

The main page of the project. This web page has the following structure:

- Navigation Bar on the top of the website: the manu is used to navigate the site - "Home, Sdudy it, My progress,Sign In / Sign Out, Register and Admin panel wich is only available to the administrator" (Dublicated on each page).
- In the BODY of the site there are 2 blocks:
  - The first of which Carousel: a slideshow for cycling through of content representing website.
  - The second is a block of news (Cards), it displays all the news that is on the site. Clicking on read more opens the news page.
- Also from the bottom is a footer block. Where is the information about the project and who is its developer(Dublicated on each page).

### Study it page

Displays a list of all topics available to the user and allows you to create new ones. If you click on a specific topic, you are redirected to the topic you witch selected.
The main functionality of the site is located on a specific page of the topic.
This webpage consists of 4 blocks, such as:

- At the top is the topic control block, which has the following capabillities:
  - Shows the name of the topic
  - Edit and delete topic (Bootstrap Modal Window)
- Button control block:
  - Buttons for adding new words and phrases: Modal windows.
  - Quiz button: by clicking on this button the quiz page opens which displays the word or phrase being quizzed and 4 answer options of which only 1 is correct (all answers are recorded in the progress table)
- Topic statistics block (this bllock consists of 2 diagrams):

  - The first of which shows the number of words and phrases in this topic.
  - And the second number of attempts and successful answers to the quiz in this topic.

- Next block is the navigation tab block that has 2 tables: Words and phrases tables. Each row in the table has information about a word or phrase, and buttons for editing and deleting a word or phrase from the user's database.

### My progress page

This web page consists of two blocks:

- The first block has two diagrams. The first diagram shows the total number of words and phrases in the user. And the second reflects the total number of attempts and correctly provided answers to the quiz.
- The second block consists of navigation Tab, which has 2 elements:
  - The first element is a table with a list of all topics with the ability to reset the statistics of a particular topic.
  - And the second element is the settings: Shows the user's personal data and the ability to change name, email, and password

### Admin page

This page is the admin panel for website management. Only the site administrator has access to this page.
This page consists of navigation Tab which contains 2 elements:

- News management tab - allows the administrator to add new news, edit and delete news.
- All users view tab - displays a list of all users who are registered on the website.

[The project also deployed on Heroku](https://learnglish.herokuapp.com/)
