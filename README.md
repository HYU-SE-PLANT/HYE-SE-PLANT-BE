# BloomMate - Backend

> This software is part of a project for a Software Engineering Project.

> The class is in collaboration with **LG Electronics.**

## 🌱Intro
This repository is the server-side equivalent of the BloomMate application. We used **Django** for the server implementation
and deployed it using **Amazon EC2**. The role of the backend is to store the information that the user enters when using the 
application in a database and return the requested information in form of API by using **Rest API**.

|**Backend Architecture**|
|------------------------|
|<image src="https://github.com/BloomMate/BloomMate-BE/assets/110537841/67fc7d25-8cc8-4e95-a448-d4e79941c004">|

## ☘️About the Backend
### ① Why Django?
We chose Django for our backend database management for the following reasons. Django is written in Python, so a lot of 
functionality is built in. This allows developers to focus more on the core functionality of the application and not waste 
time on the basics. Django also simplifies working with databases through its object-relational mapping (ORM), which allows 
developers to easily manipulate databases without having to write SQL themselves. In fact, its support for sqlite as a 
database allows code written in Django to store data in the correct format for sqlite. Django has an administrator interface 
that makes it easy for developers to see what's actually being stored and manage the site when they deploy the backend part.

### ② Why EC2?
Our original goal was to distribute the application after we finished it, so that people could actually download it and use 
it easily. When we were looking for a way to deploy it, we chose Amazon EC2 for the following reasons EC2 gives us the 
flexibility to scale our computing resources up or down, so we can reliably deliver our service even during traffic spikes. 
EC2 also provides strong security for the instances you create. We also wanted to be able to connect to other Amazon services 
so that we could use additional AWS services as we expand our service in the future.

## 🌿Special files you need to add to use this repository
Apart from the regular files created by Django, this repository should contains:

```
BloomMate/               - The top folder where you added the repository.
├── .env                 - The API Key of OPENAI and OpenWeather should be in this file.
└── requirements.txt     - List of dependencies
```

## 🪴Local development
> If you're using **Postman** instead of a direct connection to the Internet, you should be able to use each **request** normally.

To run this project in your development machine, follow these steps:

1. Move to your file location where you want to install the project and install virtualenv.

   ```
   cd C:\your\location\to\install\the\project
   
   pip install virtualenv
   ```

1. Make a folder to start Django project and move to that folder.

   ```
   mkdir Project

   cd Project
   ```

2. Configure the virtualenv environment.

   ```
   virtualenv venv
   ```

3. Enter the virtual environment.

   - windows: `venv\Scripts\activate`
   - macOS(Linux): `source venv/bin/activate`

4. Fork this repository and clone your fork.

   ```
   git clone https://github.com/BloomMate/BloomMate-BE.git
   ```

5. Install dependencies.

   ```
   pip install -r requirements.txt
   ```

6. Create a development database.

   ```
   python manage.py migrate
   ```

7. If everything is alright, you should be able to start the Django development server.

   ```
   python manage.py runserver
   ```

8. Open your browser and go to http://127.0.0.1:8000, You should see a Rest API page that specifies the exact page address.

|**The first page when you enter**|
|---------------------------------|
|![image](https://github.com/BloomMate/BloomMate-BE/assets/110537841/e3d6b420-7858-4966-b827-578af2faf741)|
