# foodstock-backend

Foodstock is a web application that allows you to manage your food stock. It is composed of a frontend and a backend. This is the backend part.

## Architecture
The backend is build using [Django](https://www.djangoproject.com/). Django is used to manage the database and Django REST Framework is used to create the API. 

I chose to use Django because I have a lot of experience with it and it is very easy to use. 

The frontend and backend are separated in two different repositories. The front-end is available [here](https://github.com/food-stock/foodstock-backend).

 I wanted them to be separated because I wanted to be able to change the frontend without changing the backend and vice versa.


## Roadmap
- [x] Basic functions
- [x] Authentication
- [x] Secure the API : Endpoints compare the user id of the provided token with the user id of the object to ensure that no one can access other users data
- [ ] Generate Swagger documentation
- [ ] Host the landing page here and
- [ ] Make a paid plan
