[![server-ci](https://github.com/reubinoff/Baking/actions/workflows/python-app.yml/badge.svg?branch=develop)](https://github.com/reubinoff/Baking/actions/workflows/python-app.yml)  [![React App](https://github.com/reubinoff/Baking/actions/workflows/frontend-react.yml/badge.svg?branch=develop)](https://github.com/reubinoff/Baking/actions/workflows/frontend-react.yml)

# Baking
This is a web application for managing baking recipes. It allows users to create, edit, and delete recipes, as well as view a list of all recipes.

# Getting Started
To get started with the application, follow these steps:

Clone the repository to your local machine.
Install the dependencies by running npm install.
Start the development server by running npm start.
The application should now be running at http://localhost:3000.

# Usage
To use the application, follow these steps:

Click on the "New Recipe" button to create a new recipe.
Fill in the recipe details, including the name, ingredients, and instructions.
Click on the "Save" button to save the recipe.
To edit a recipe, click on the recipe in the list and then click on the "Edit" button.
To delete a recipe, click on the recipe in the list and then click on the "Delete" button.
Contributing
If you would like to contribute to the project, please follow these steps:

# Makefile
This is the Makefile for the baking recipes project. It provides a set of commands for building, testing, and running the project.

## Commands
build
Builds the server and client components of the project.

`test-server`
Runs the server tests using pytest and generates a coverage report.

`run-db`
Starts a MongoDB container with the specified root password and username.

`stop-db`
Stops the MongoDB container.

`check-updates`
Checks for outdated packages in the server and client components and updates them.

## Variables
`DOCKER_REG`
The Docker registry to use for building and pushing Docker images.

`DB_ROOT_PWD`
The root password to use for the MongoDB container.

`DB_ROOT_USER`
The root username to use for the MongoDB container.

`DB_CONTAINER_NAME`
The name to use for the MongoDB container.

## Usage
To use the Makefile, run the make command followed by the name of the command you want to run. For example, to build the server and client components, run:



# Fork the repository.
Create a new branch for your changes.
Make your changes and commit them.
Push your changes to your fork.
Create a pull request.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgments
This project was inspired by my love of baking and my desire to create a simple recipe management tool.
