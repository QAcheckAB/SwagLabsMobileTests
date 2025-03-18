# README #

### What is this repository for? ###

This project is created and developed to automate tests for mobile applications SWAG LABS MOBILE app.
Currently only selectors for android are implemented.

### How to set up a project locally ###

1. Install IDE - e.g: PyCharm
2. Clone project from repository
3. Install python 3.11
4. Create a python virtual environment:

    ###### From pycharm:
    `PyCharm -> Settings -> Project:swag_labs_mobile -> Project Interpreter -> Add interpreter`

    ###### From command line:
    ```
    python3 -m venv ./venv
    source venv/bin/activate
    ```
5. install dependencies: `pip install -r requirements.txt`
6. Get the app from the following link: https://github.com/saucelabs/sample-app-mobile/releases/
7. Install Appium app - read more: https://appium.io/
8. Verify appium configuration with the appium-doctor tool: https://www.npmjs.com/package/appium-doctor
9. Run the appium server
10. Connect real mobile devices or use simulators
11. Set app environment variables
12. run command: `pytest -s -v ./tests`

### Environment variables used in the project:

    PLATFORM # android or ios
    APP_DIRECTORY # Path to the directory with the application, you can create a directory test_apps in the project and put the application there
    CONFIG_FILE # The name of the configuration file, you can use 'android_config.json' or 'ios_config.json' to run test locally


### pre-commit

This project uses flake8, mypy and Black tools to lint and format code automatically. To run tools on commit:

- Install libraries pre-commit, black, and flake8 (included in requirements.txt)
- run command: `pre-commit install` in the project main directory

### HTML Report - Allure report

TO DO right now only steps to generate the report are provided.
