# SM Backend

# SM Backend test task

*To start the project you need to execute:**

* clone project repo
* Create an .env file and populate it following the default.env file example



* execute the command `make build` for build container
* execute the command `make cmd` for using console
* execute the command `make run` for run container

* execute the command `python manage.py migrate` for run migrations (if you don`t use dump)

You can fill db or run `make load` for load dump (**when container is running**)

* execute the command `python manage.py resource_allocation` for run resource allocation (**when container is running**)
* 
you can use user from dump:

*users creds for testing route and admin panel:*
 username:"admin", password:"admin"


full dock in [SM_Backend.postman_collection.json](SM_Backend.postman_collection.json) file





