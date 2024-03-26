# car-wiki

Ongoing project with end-goal of being a web app for searching and comparing vehicles on a detailed list of specifications.

I will be building out the database by web-scraping from several sources, and my dream goal is to develop the most comprehensive database on car specs possible.

While not new to coding, I am very much new to web development, so this was started mostly an exercise in learning, but I'm also hopeful that the end result will be something interesting and useful.

## Stack

- [Frontend](https://github.com/sebbooth/car-wiki/tree/main/react_frontend)
  - Frontend is a React Vite project written in JavaScript
  - Using Material UI for various components
  - Will be using axios to interface with Flask backend
- [Backend](https://github.com/sebbooth/car-wiki/tree/main/flask_backend)
  - Backend is a Python Flask API built on top of Firebase
  - Building out Pytest integration tests as I flesh out the API
- [Data Acquisition](https://github.com/sebbooth/car-wiki/tree/main/data_mine)
  - Backend
  - Data is acquired through web-scraping with Python and Selenium.

## Updates

### 2024-03-26

Original plan was to build the app entirely in React with Firebase directly integrated, but for the sake of security, scalability, and my own education, I recently decided to create my own API with Flask, abstracting all of Firebase away from my frontend.

So far, I've built out a basic CRUD system, which incorporates a rudimentary form of version control for documents in the database. I've also built some basic integration tests and plan to continue building out a testing framework as the API improves. Next steps include handling authorization, cloud storage, and the integration of these with the database functions.

I haven't been working on the webscrapers as of late, since I need to develop a way to merge data from different sources before I allow the scrapers to fully run. This will involve cleaning up data on all datasources, normalizing the names of fields and units of values, and finally settling on a final structure for how documents will look in my database.

The frontend will be on standby until my API is at least mostly functional and I have a decent-sized database to run tests on.
