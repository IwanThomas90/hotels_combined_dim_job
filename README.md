Data Job Template
=================

A simple template that should be used for all python data jobs.

To create a virtual environment, run flake8 style check and run tests:

```shell
./gradlew
```

In order to run the job locally as a docker image run (includes a config override as an example):

```shell
./gradlew dockerImage
docker run -it travel/data-job-template:1.0.10 --mart_db_name database_name
```

## Acceptance Tests


To run the **acceptance tests** you will require the job under test to be available as a local docker image.

The image can be built with the following command:


```shell
./gradlew :job:dockerImage
```

This will then allow for the **acceptance tests** to be runnable either through an IDE or the command line:
 
 ```shell
 ./gradlew :acceptance-tests:cucumber
 ```


## Configuration

The template contains a framework for dealing with config for the job.

Default values are set in the config.ini file and can be overridden using commandline arguments of the same name.

Out of the box there are some commonly used config options specified.
These can be removed or added to by adding or removing lines from the *_setup_configuration_keys* method within the *configuration.py* module.

**e.g.** If you want to add a new config option you would add the last line below:

```python
def _setup_configuration_keys(parser: configargparse.ArgumentParser):
    # The keys supplied in the template are for example only. Remove any that are not required in your job and add
    # Any extras
    parser.add_argument('--warehouse_host', required=True, help='host address of the data warehouse')
...
    parser.add_argument('--new_config_option', required=True, help='This is a new config option required for the job')
```

Config is printed out at the start of the job to help with debugging.
Sensitive values are replaced with asterisk characters.
Sensitive config is by default anything that contains 'password'.
This can easily be added to by adding regex expressions to the *patterns_to_hide* variable within *_should_mask_key*

**e.g.** To include anything containing secret

```python
def _should_mask_key(key):
    patterns_to_hide = ['.*password.*', '.*secret.*']
```

## PyCharm Setup

Once a build has been run, you will have a virtual miniconda environment available in your build dir.

You will want to set this to be used as the interpreter within Pycharm in order to run tests and get code completion.

To do this:

1. Navigate to File -> Setting -> Project -> Project Interpreter
2. Click the settings button in the top right and select add local
3. Select <PROJECT_DIR>/build/venv/bin/python
4. Click the settings button again and select More
5. Select the environment you just created and click the edit icon
6. Set the name to <PROJECT_NAME> e.g. data-job-template and select ok

After doing this the environment should automatically be used as the name matches what is specified in the checked in iml file.

## OS Support

**The gradle build will not currently run successfully on Windows machine.**

This is down to the Miniconda plugin no being fully compatible with non unix systems.
There is a pull request submitted to resolve this but may be a while before a new version is released containing the fix.
