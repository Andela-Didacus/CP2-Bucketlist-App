# **BUCKETLIST API APPLICATION**
A Bucket List is a list of things that one has not done before but wants to do before dying. THe Bucketlist API application is an application that helps keep track of those bucketlist ideas. 

# **Getting Started**
The program has been fully developed using **Flask** and some of its libraries, while the database implementation uses **SqlAlchemy** and **SQLITE3**

* Python 3.6
* sqlAlchemy
* Flask
* SQLITE3
* Visual Studio

# **Prerequisites**
Below are some of the basic requirements to run the program:
* Python should be installed in your computer, if not do so here _[Python Download](https://tutorial.djangogirls.org/en/python_installation/)_
* Git should be installed in your computer, if not do so here, _[Git Download](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwjxsYyak8zRAhWsI8AKHR9YDL4QFggfMAA&url=https%3A%2F%2Fgit-scm.com%2Fdownloads&usg=AFQjCNHZLDrEFiZHXrz1JGq57NFHFrcfkA&sig2=4ht1GzU2s-G7fLM3fuDxYA)_
* A stable internet connection is recommended

* SQLITE3 should be installed, if not, do so on _[SQLITE3](github.com/sqlitebrowser/sqlitebrowser/releases)_

# **Installation**
Follow the following steps to succesfully _**install**_ the program:
1. Run your _Git Bash_ program and `cd`into the directory of installation.
2. Type **`$ git clone https://github.com/Andela-Didacus/CP2-Bucketlist-App.git`** to clone the repository to your desktop folder.
3. cd into the `CP2-Bucketlist-App` folder.
3. open command prompt and enter **`$ pip install -r requirements.txt`** to install the required packages to run the program.
4. Finally enter **`$ python run.py`** to run the program.

# **Bucketlist API Features**
* `POST /auth/login`          -------              Logs a user in
* `POST /auth/register`       -------              Register a user
* `GET /users`  ----------- Returns A list of all Users
* `DELETE/users/<id>/`    -------Deletes a user from the system
* `PUT/users/<id>/` --------updates user Information
* `POST /bucketlists/`        -------              Create a new bucket list
* `GET /bucketlists/`         -------              List all the created bucket lists
* `GET /bucketlists/<id>/`    -------              Get single bucket list
* `PUT /bucketlists/<id>/`    -------              Update this bucket list
* `DELETE /bucketlists/<id>/`  ------             Delete this single bucket list
* `POST /bucketlists/<id>/items/`  --         Create a new item in bucket list
* `PUT /bucketlists/<id>/items/<item_id>/`  Update a bucket list item
* `DELETE /bucketlists/<id>/items/<item_id>/` Delete an item in a bucket list

## Running the tests

Tests on this project are done using python nose package. To run the tests enter the following command in your terminal in the `CP2-Bucketlist-App` directory.
`nosetests --with-coverage --cover-package=app`
## Authors

* **Didacus Odhiambo** -- [Didacus Odhiambo](https://github.com/Andela-Didacus)
