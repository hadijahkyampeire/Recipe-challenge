


![Test Coverage](https://api.codeclimate.com/v1/badges/ca71e324cb7d2d470b11/test_coverage)](https://codeclimate.com/github/sir3n-sn/Recipe-challenge/test_coverage)
![Maintainability](https://api.codeclimate.com/v1/badges/ca71e324cb7d2d470b11/maintainability)](https://codeclimate.com/github/sir3n-sn/Recipe-challenge/maintainability)
![Coverage Status](https://coveralls.io/repos/github/sir3n-sn/Recipe-challenge/badge.svg?branch=master)
![Build status](https://travis-ci.org/sir3n-sn/Recipe-challenge.svg?branch=master)

# Yummy recipes

A simple app based on flask 


##currently under development

## useful links
https://www.pivotaltracker.com/n/projects/2119357
https://sir3n-sn.github.io/Recipe-challenge/designs/UI/index.html
## Heroku app coming up once pull request is accepted
##Application snippets
![Alt text](/images/login.png?raw=true "Login page")
![Alt text](/images/Sign-up.png?raw=true "Registration page")
![Alt text](/images/inside_1.png?raw=true "My Recipe page")
![Alt text](/images/Categories.png?raw=true "Category page")
![Alt text](/images/myrecipes.png?raw=true "My Recipe page")


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

A working web browser and or a pc.
If you wish to clone the repo please satisfy the requirements in the requirements.txt

### Installing

A step by step series of examples that tell you have to get a development env running

```
Clone the repo to your desktop

git clone https://github.com/sir3n-sn/Recipe-challenge.git

##install and run a development environment

apt-get install virtualenv
apt-get install -f 

##Navigate to cloned repo
virtualenv venv
source venv/bin/activate
##You should now see an environment inside you terminal with (venv)
pip install -r requirements.txt
python3 app.py

#you should now see a local host 127.0.0.1:5000
Navigate to the local host with your favorite browser 
enjoy

```


## Running the tests

```
#run

pip3 install pytest

pytest /path/to/repo

### Breaking down the tests
These tests ensure login credentials are secure, recipes 
are created, Users are registered
example below



```
    def test_user_password_is_encrypted(self):
        """Returns true if password is encrypted"""
        self.assertNotEqual(userdata[self.Sir3n.user_id]['password'], 'Kali2017', msg='Password is not encrypted')
```

### Need for test

To ensure maintainability of code in future developments
This ensures no new code breaks our already existing code

Note: Travis-ci ensures continous integration and runs test automatically for this build

```
Give an example
```

## Deployment

Heroku app coming up in afew

## Built With

* [Html5 and css3 python and flask] - The markup and styling sheet
* [Dependencies in requirements.txt] - Dependency Management
* 
## Contributing

Contributions would be highly appreciated, Help out and make a pull request, and the process for submitting pull requests to me.

## Versioning

Version 0.6

## Authors

* **Dhulkifli Husseiin** - *Initial work* - [Recipe-challenge](https://github.com/Recipe-challenge)

See also the list of [contributors](https://github.com/Sir3n-sn/Recipe-challenge/contributors) who participated in this project.

## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Andela


