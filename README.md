# <center>Fyyur</center>

### Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

![image](https://user-images.githubusercontent.com/104495751/194054532-441f6af3-b2a7-4fd8-83bd-60bbb22c9f33.png)

### Code Style

The code use PEP8 style.

## Getting Started

### Tech Stack (Dependencies)

#### <center>Backend Dependencies</center>

The following are the backend dependencies

 - virtualenv: To create an isolated Python environment
 - SQLAlchemy ORM to be my ORM library of choice
 - PostgreSQL as my database of choice
 - Python3 and Flask as my server language and server framework
 - Flask-Migrate for creating and running schema migrations (Creating versions of schemas)

You can download and install all the dependencies mentioned above using `pip` as:

```
pip install visrtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

#### <center>Frontend Dependencies</center>
You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for the website's frontend.

You can install Bootstrap using Node Package Manager (NPM) and if you dont have NPM installed already, you can download and install the [Node.js](https://nodejs.org/en/download/).

You can confirm if Node.js and NPM is installed successfully using the codes below

```
node -v
npm -v
```

Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:

```
npm init -y
npm install bootstrap@3
```

## Main Files: Project Structure

```
├── README.md
├── app.py *** The main driver of the app. Includes your SQLAlchemy models.
                  "python app.py" to run after installing dependencies
├── config.py *** Database URLs, CSRF generation, etc
├── models.py *** Models
├── error.log
├── forms.py *** Your forms
├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
├── static
│   ├── css
│   ├── font
│   ├── ico
│   ├── img
│   └── js
└── templates
    ├── errors
    ├── forms
    ├── layouts
    └── pages
```

**Overall**:

- Models are located in `models.py` file
- Controllers are located in `app.py` file
- The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
- Web forms for creating data are located in `form.py` file

## Local or Development Setup.

You can either download the repository code or fork and clone the project.

### Method 1 : Downloading the repository code.
* Click on `Code` and`Download as zip`

![image](https://user-images.githubusercontent.com/104495751/186272594-325116ad-e426-4509-9af3-a807e9cc2ccb.png)
____________

### Method 2 : Forking and cloning the project.

1. **Fork the project**

![image](https://user-images.githubusercontent.com/104495751/186272278-5feb2d1d-948b-437d-9188-a81de0413ac5.png)
__________

2. **Clone the project**

   ```
   git clone https://github.com/Ojerinde/Udacity-Fyyur-1.git
   cd Udacity-Fyyur-1
   ```

3. **Initialize a virtual enviroment using**

```
python -m virtualenv env
```

4. **Activate the environment using**:

`source env/bin/activate`

**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:

`source env/Scripts/activate`

5. **Install the dependencies**:

pip install -r requirements.txt

6. **Run the development server**:

If you have the code in the screnshot below in your app.py, all you have to do is to run `python app.py`

![image](https://user-images.githubusercontent.com/104495751/186289098-0803edbd-88a6-4632-b46d-78ab34a9ca20.png)

Else, you run the codes below

```
export FLASK_APP=myapp
export FLASK_DEBUG=True # enables debug mode
flask run

```
**Note**: For window, change export to set i.e. set FLASK_APP=myapp

7. **Verify on the Browser** by navigating to the default port http://127.0.0.1:5000/

