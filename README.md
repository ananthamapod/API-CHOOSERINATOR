# API-Chooserinator

This application is built using [Flask microframework](http://flask.pocoo.org/) and is intented to be a resource for hackers to find ideas for projects and APIs for data classes. It is hosted on [IBM's Bluemix](https://bluemix.net/) environment which is based on Cloud Foundry.

You can view the project at [http://api-chooserinator.mybluemix.net/](http://api-chooserinator.mybluemix.net/)

This project was built at [HackUMass](http://hackumass.com).
## Run Locally

Very simple. First, clone it and go into the directory. Once you're in the directory containing the files, it's advisable to set up virtualenv (Go to the [Flask installation instructions](http://flask.pocoo.org/docs/0.10/installation/#installation) for more information)and use ```pip install -r requirements.txt``` to install dependencies.

Command to run the program from the command line is ```python app.py```

## Usage

#### Searching

Searching is pretty basic. Just search for a data class or api in the search box either on the main page or in the header bar. Auto-completion is currently not implemented but is planned as a later feature.

#### Adding an API, Data Class, or API-to-Data-Class Mapping

This is a collaborative database. The point is to be able to add, so to that end, there is a dedicated [add page](http://api-chooserinator.mybluemix.net/add/).

## Contributing changes

Completely open source. Add an issue, submit a pull request, and together we can make the API-Chooserinator an awesome tool for hackathon hackers everywhere. Keeping the name not mandatory.

## Licensing

See [LICENSE](LICENSE.md)
