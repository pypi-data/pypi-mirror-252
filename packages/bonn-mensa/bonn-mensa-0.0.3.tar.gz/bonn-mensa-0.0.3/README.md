# Meal plans for university canteens in Bonn

A python script for displaying the meal plans of the canteens of the [Studierendenwerk Bonn](https://www.studierendenwerk-bonn.de/).
The script parses the HTML response of a call to an API.
Depending on your request the API might take a few seconds to respond.

![an example output](images/bonn-mensa_example_output.png)

## Installation

To install this script, run

```sh
 pip install bonn-mensa
```

### MacOS (using homebrew)

To install the application using homebrew, run:

```bash
# Add the tap to homebrew
brew tap --force-auto-update alexanderwallau/bonn-mensa https://github.com/alexanderwallau/bonn-mensa

# Install the application
brew install bonn-mensa

# Install the application from main branch
brew install --HEAD bonn-mensa 
```

In case you want to remove the application, run:

```bash
brew uninstall bonn-mensa
brew untap alexanderwallau/bonn-mensa
brew autoremove
```

## Usage

To run the script, simply run `mensa`. For a list of all arguments, see `mensa --help`
```
$ mensa --help
usage: mensa [-h] [--vegan | --vegetarian]
             [--mensa {SanktAugustin,CAMPO,Hofgarten,FoodtruckRheinbach,VenusbergBistro,CasinoZEF/ZEI,Foodtruck}]
             [--filter-categories [CATEGORY ...]] [--date DATE] [--lang {de,en}] [--show-all-allergens]
             [--show-additives] [--no-colors] [--markdown]

optional arguments:
  -h, --help            show this help message and exit
  --vegan               Only show vegan options
  --vegetarian          Only show vegetarian options
  --mensa {SanktAugustin,CAMPO,Hofgarten,FoodtruckRheinbach,VenusbergBistro,CasinoZEF/ZEI,Foodtruck, Rabinstraße}
                        The canteen to query. Defaults to CAMPO.
  --filter-categories [CATEGORY ...]
                        Meal categories to hide. Defaults to ['Buffet', 'Dessert'].
  --date DATE           The date to query for in YYYY-MM-DD format. Defaults to today.
  --lang {de,en}        The language of the meal plan to query. Defaults to German.
  --show-all-allergens  Show all allergens. By default, only allergens relevant to vegans (e.g. milk or fish) are shown.
  --show-additives      Show additives.
  --no-colors           Do not use any ANSI colors in the output.
  --markdown            Output in markdown table format.
  --verbose             Output Debug Log
```
