# hashr

Simply a custom hashing package with optional salting, able to be both run from the command line and imported as a package.

## Installation

To install, just run either of the below commands.
```bash
pip install hashr
```
```bash
pip3 install hashr
```

## Usage

#### Command Line

To use hashr from the command line, run:
```bash
hashr [input]
```
Make sure to surround an input with double quotes if it contains spaces.  
There is also the option to add a salt, which causes duplicate string to have unique hashes. To use this, add the ```-s``` flag to the command.

#### Import Package

To import hashr as a package, add ```from hashr import [function]``` to the top of your Python file.
The available functions are as follows:
 - hashr: main hashing algorithm, turns any string into a string hash
 - saltr: generates a seven digit salt, either numerical or alphabetical
 - number_to_letters: converts a number to letters based on each digit
