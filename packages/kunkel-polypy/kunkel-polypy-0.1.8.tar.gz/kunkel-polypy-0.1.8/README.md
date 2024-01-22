# **PolyPy**
## Intro:
Polypy is meant to a be a small, straightfoward library that interfaces with the official **`Polygon.io`** Api. The library is currently in pre-alpha, as it lacks a complete configuration file of api endpoints to interface with. It currently only has core functionality surrounding _stock-options_ related endpoints configured. That being said, the core module **`data_access.py`** depends on _.yaml_ configuration files for all api endpoints (and other configs), and is coded in a way that makes adding functionality a matter of copy and paste (which will be done after unit testing this release's framework). The most important limitation is that the polygon.io api itself is _extremely_ limited unless you pay a subscription for premium data rates. The free data rate is 5 api calls/minute along with only previous day data available. This is far too slow for any high performance project, but would be fine albiet slow for backtesting. There is more information on these subjects below. Thanks for checking out the project!

## **Table Of Contents:**
1. Functions
2. Configuration
3. End

## 1. Functions:
This pre-alpha release has the functionality broken down into three classes within the **`data_access.py`** module. 
1. **DataAccessToolkit** - Functions for parameter validation and loading data from configuration files into python objects.
2. **GetApiData** - Functions make up a sort of modular engine for generating reliable request urls, and then making those api calls.
3. **ExportApiData** - Functions to stamp and export the data to .yaml files and/or .json files.

The module is written in a way that makes up front setup slow, but is reliable and clean to code with. Only three functions in entire module the **DataAccessToolkit** class, meant to streamline loading all of the configuration data held in .yaml files, contain any kind of hard coded value. That value is only that of `file_paths.yaml` which contains file paths for all program files. the `file_paths.yaml` file is the only program file that needs to remain in the the working directory of the module.


The full class structure for the `data_access.py` module is as follows:
1. ### DataAccessToolkit
    + `def validate_parameters_exist(*params) -> bool:` 
        '''Returns a boolean denoting status of conditional check. True if params exist'''
    + `def validate_parameters_type(exp_type: type, *params ) -> bool:`
        '''Returns a boolean denoting status of conditional check. True if params match expected type (abb. as 'exp_type')'''
    + `def settings() -> dict:`
        '''loads the program's settings file into a python dict'''
    + `def req_params() -> dict:`
        '''loads the program's request parameters file into a python dict'''
    + `def file_paths() -> dict:`
        '''loads the local file_paths.yaml configuration file into a python dict'''

    The **DataAccessToolkit** class streamlines the task of accessing configuration file values via the `settings()`, `req_params()` and `file_paths()` functions. The three afromentioned functions do the work of locating, then opening configuration files and returns a python dictionary representing the values.
    + **settings()** - returns a dictionary of program settings. Takes no arguments.
    + **req_params()** - returns a dictionary of request parameters, which are used to configure api calls. Takes no arguments.
    + **file_paths()** - returns a dictionary of file paths for all other program files. Takes no arguments.

    These functions help clean up code from this for each configuration file:
    ```
    try:

            settings = {}

            with open("file_paths.yaml") as paths_file:
                paths = yaml.safe_load(paths_file)
                settings_file_path = paths["program_files"]["settings"]

            with open(settings_file_path, mode='r') as settings_file:
                settings = yaml.safe_load(settings_file)

            some_config_value = settings[value][value2]
            
        except FileNotFoundError as err:
            print("FileNotFoundError: Could not open <File: {}>. 1. Check to make sure that the file exists.\n2. That the file is in the program's working directory.\n".format(err.filename))
            return None
        except FileExistsError as err:
            print("FileNotFoundError: Could not open <File: {}>. 1. Check to make sure that the file exists.\n2. That the file is in the program's working directory.\n".format(err.filename))
            return None
    ```
    Into this:
    ```
    import data_access
    tools = data_access.DataAccessToolkit()
    settings = tools.settings()
    some_config_value = settings[value][value2]
    ```

    The class also provides existence and type checking functions with the `validate_parameters_exist()` and `validate_parameters_type()` functions. This allows you to implement parameter validation and handle errors with fewer lines of code. All class methods in `data_access.py` are type checked using these functions.  
    + **def validate_parameters_exist(\*params)** - Validates that parameter(s) exists. Takes 1-_any_ number of arguments to check via _*params_. This gives the programmer an option to load the function with any number of parameters to check or to use the function in a loop. Returns True if _*params_ exists. 

    + **def validate_parameters_type(exp_type: type, \*params )** - Validates that parameter(s) is of an expected type. Takes an expected type argument via _exp\_type_ and 1-_any_ number of arguments to check via _*params_. This gives the programmer an option to load the function with any number of parameters to check or to use the function in a loop. Returns True if _*params_ is of expected type.    


2. ### GetApiData
    + `def generate_request_url2(base_url: str, options_ticker: str, ticker: str, date: str, request_parameters: dict) -> str:`
        '''Generates and properly formats a request url for 'polygon.io' given parameters in configuration file'''
    + `def request_data(url: str, api_key: str) -> dict:`
        '''Makes a 'GET' API request to polygon.io'''

    The **GetApiData** class is written as an engine to make api calls to `polygon.io`. The `request_parameters.yaml` file contains all configured polygon.io api endpoints and their respective parameters. Each endpoint has a section of configuration values. Take a look at the snippet of the `request_parameters.yaml` file below for a line by line breakdown:
    ```
    simple_moving_average: -> This is the dictionary key you would refer to when wanting to call the 'simple moving average' api endpoint. 
        url: "https://api.polygon.io/v1/indicators/sma/{optionsTicker}?" -> Base url for this specific endpoint. *see note for the curly {} brackets at the bottom
        parameters: -> This collection of items are the parameters for the request itself. These should be the only values to change within each endpoint's values.
            timestamp: null
            timespan: "day"
            adjusted: "true"
            window: "200"
            series_type: null
            expand_underlying: "true"
            order: "desc"
            limit: "10"

    NOTE: The curly {} brackets and text within are placeholders for a regular expression engine in the `generate_request_url2()` function and need to be notated that in this way.
    ```  
    + **generate_request_url2(base_url: str, options_ticker: str, ticker: str, date: str, request_parameters: dict)** - Takes 5 arguments and returns a string to use as our request url for an api call. Arguments are as follows:
        + _base\_url_ - The url pointing to the api endpoint we want to make a request to. This would be the 'url' key in the YAML example above.  
        + _options\_ticker_ - The target options ticker. There is a field for this value in `request_parameters.yaml`, but you can use any source for the string. ex. file containing multiple options tickers. *See note at bottom of list
        + _ticker_ - The target stock ticker symbol. Also has a field in `request_parameters.yaml`, but can use another source. *See note at bottom of list
        + _date_ - A date as a string, formatted as 'YYYY/MM/DD'. *See note at bottom of list
        + _request\_parameters_ - A dictionary of request parameters for the endpoint. This would be the 'parameters' key in the YAML example above.
        + NOTE: _options\_ticker_, _ticker_ and _date_ are currently all required parameters even if the endpoint does not call for that value. For now, in order to avoid an error, just use a default value from `request_parameters.yaml` for the values that you don't require (or default values for all). Values needed for a given endpoint can be found in the curly {} brackets in the 'url' field of that endpoint.

    + **request_data(url: str, api_key: str) -> dict:** - Takes 2 arguments and makes a request to the polygon.io api. Returns a response as python dictionary upon a successful api call. Arguments:
        + _url_ - A string formatted as a valid api request url. You would use the return value of `generate_request_url2()` here.
        + _api\_key_ - A string containing the caller's api key. You must obtain this key from polygon.io via making an account. This value is stored in `settings.yaml` 

    An example of implementing these functions can be found in `example.py` of this module's working directory! You can try out the example implementation by running the `api_cmd.py` file.

3. ### ExportApiData
    + `def sort_api_data(data_object: dict, request_url: str) -> dict:`
        '''Sorts and adds program stamp(s) to an API response from polygon.io'''
    + `def write_yaml(write_file_dir: str, data_object: dict, filename: str) -> None:`
        '''Writes a dictionary data object (ex. api response) to a .yaml file'''
    + `def write_json(write_file_dir: str, data_object: dict, filename: str) -> None:`
        '''Writes a dictionary data object (api response)to a .json file'''
    
    The **ExportApiData** class contains methods for organizing and exporting an api response to a file.
    + **sort_api_data(data_object: dict, request_url: str) -> dict:** - Will sort and stamp added parameters such as the date of the request onto the data object and then return it. Takes 2 arguments:
        + _data\_object_ - The dictionary object to sort/stamp and return. This will be the return value of the `request_data()` function from the `GetApiData` class.
        + _request\_url_ - The string containing the request url for the api call in question. This should be the return value of the `generate_request_url2()` function from the `GetDataApi` class.

    + **write_yaml(write_file_dir: str, data_object: dict, filename: str) -> None:** - Exports a given data dictionary object to a .yaml file. Takes 3 arguments:
        + _write\_file\_dir_ - The directory in which to write the file into. Can be found in the `file_paths.yaml` file.
        + _data\_object_ - The dictionary object to write into the file. Should be a return value from either the `request_data()` or `sort_api_data()` functions, depending on whether you just want to write the raw response or not (you could do both?).
        + _filename_ - The name of the file to be written.
        + NOTE: The `write_json()` function operates on the same arguments so we will skip it. 


## Configuration:

Configuration in polypy revolves around 3 included program files - _file\_paths.yaml_, _settings.yaml_ and _request\_parameters.yaml_. `file_paths.yaml` is the only one of these files that _can not_ move from the program's working directory. This file contains the file paths for _settings.yaml_, _request\_parameters.yaml_, the path to the directory in which you wish to export files and potentially any other file you may want to work into a program. Both of the other program files are by default stored in the program's working directory (polypy/src/), but can be stored anywhere that is convenient for you. Note that you _can_ rename them (besides file_paths.yaml) but are encouraged to keep them names as is and just cut+paste them to avoid confusion. The following configuration tutorial will assume that the user may not want/know how to code. If you do, then you can skip this section with the information you already know about the program. 

The default _file\_paths.yaml_ file looks like this:
```
---
api_files: 
  request_parameters: "path/to/request_parameters.yaml"
  api_export: "path/to/you/data/export/directory"

program_files:
  settings: "path/to/settings.yaml"

```
You probably want your files in a location that makes sense to _you_. Simply move the files where you want them and copy the path to the appropriate entry in the file! Ensure that the file path is written/copied properly and is contained within the double `""` quotes.

The _settings.yaml_ file contains static program configuration values such as your api key. The default file is as follows:
```
---
static: 
  api_key: "Bearer 123apikey321" -> Api key from polygon.io goes in this field formatted with 'Bearer', a space and then the key.
  request_rate: 15 #seconds -> The rate at which the program will make requests, in seconds. Free api key rate is 5 calls/minute. This is set @ 4 calls/minute

preferences: 
  verbose?: true - > not implemented yet, but will be upon alpha release
```
As with the fields in _file\_paths.yaml_, all values must be enclosed in double `""` quotes. This is true for all values in any configuration file for this module!

Finally we have the _request\_parameters.yaml_ file. Below is a snippet:
```
simple_moving_average: -> endpoint key used to id the endpoint by the module - **Don't Touch!** 
  url: "https://api.polygon.io/v1/indicators/sma/{optionsTicker}?" - > The base url with placeholder for regular expressions - **Don't Touch!**
  parameters: -> Key for program to get params - **Don't Touch!**
    timestamp: null - > Everything from here down is a parameter that can be adjusted to return different information from the api. All of these can be changed.
    timespan: "day"
    adjusted: "true"
    window: "200"
    series_type: null
    expand_underlying: "true"
    order: "desc"
    limit: "10"

exponential_moving_average: 
  url: "https://api.polygon.io/v1/indicators/ema/{optionsTicker}?"
  parameters: 
    timestamp: null
    timespan: "day"
    adjusted: "true"
    window: "50"
    series_type: "close"
    expand_underlying: "true"
    order: "desc"
    limit: "10"
```
Above we have two api endpoints. One for simple moving average (SMA), and one for exponential moving average (EMA). The SMA is marked up to show you what values can be changed. As you can see, all values under the `parameters` key can be changed to suit your needs. Just remember to keep values in quotes as always. To refer to what these values should/can be, look at  https://polygon.io/docs/options/getting-started.
   
## End:
As always, thanks for checking out the project! As we are in pre-alpha, documentation will be only this page. As the module enters >= pre-alpha, more comprehensive docs will be supplied along with the added functionality. 