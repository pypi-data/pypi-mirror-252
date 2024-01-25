# OOD Implementation

This project demonstrates Object-Oriented Design principles in a Python implementation.


## Getting Started

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/asadjalbani/OOD-Implementation.git
cd OOD
```

## Using venv
```python
python -m venv venv
```


## Using virtualenv
```python
virtualenv venv
```
## Python Virtual Environment

### For Windows:
```python
venv\Scripts\activate
```

### For Windows
```python
venv\Scripts\activate
```

### For macOS/Linux:
```python
source venv/bin/activate
```
### Run the Project
```python
python main.py
```
---

## Documenation
---
### Inheritence 

Implemented a simple hierarchy of classes using Python. The Post class serves as a base with title, content, and author attributes. The Article class inherits from Post and introduces a category attribute, while the Review class also inherits from Post and adds a rating attribute. Each class has a method to display its specific details.

## Modules
LightsController Module:

class LightsController: Manages the lighting system for a specified room.
__init__(self, room): Initializes the controller with the specified room and sets the initial status to "off."
toggle_lights(self): Toggles the lights between on and off states in the assigned room.
SecuritySystem Module:

class SecuritySystem: Implements a security system.
__init__(self): Initializes the security system with armed set to False.
arm(self): Arms the security system.
disarm(self): Disarms the security system.
TemperatureController Module:

class TemperatureController: Controls the temperature for a specified room.
__init__(self, room, current_temp): Initializes the temperature controller with the specified room and current_temp.
adjust_temperature(self, target_temp): Adjusts the temperature in the assigned room from the current temperature to the specified target_temp.

# Garden Package Documentation

## Plants Module

### Class: Flower
Represents a flower in the garden.

- **Initialization:**
  - `__init__(self, name, color)`: Initializes a flower with the specified `name` and `color`.

- **Methods:**
  - `bloom(self)`: Prints a message indicating that the flower is blooming.

### Class: Tree
Represents a tree in the garden.

- **Initialization:**
  - `__init__(self, name, height)`: Initializes a tree with the specified `name` and `height`.

- **Methods:**
  - `grow(self)`: Prints a message indicating that the tree is growing to a certain height.

## Weather Module

### Class: Weather
Represents the weather in the garden.

- **Initialization:**
  - `__init__(self, condition)`: Initializes the weather with the specified `condition`.

- **Methods:**
  - `report(self)`: Prints a message reporting the current weather condition.

## Python Virtual Environment
A virtual environment is a crucial tool in Python development that allows you to manage dependencies, isolate project-specific packages, and maintain a clean and consistent environment for your projects. It helps to avoid conflicts between different projects and ensures that each project has its own set of dependencies, preventing version clashes and simplifying the deployment process.

- By using a virtual environment, you can:

- Isolate Dependencies: Keep the dependencies for - each project separate, preventing conflicts between different versions of packages.

- Version Control: Easily manage and replicate the exact environment used during development by freezing dependencies in a requirements.txt file.

- Clean Development: Start with a fresh, clean environment for each project, reducing the likelihood of issues related to global Python installations.

[Implemenation](#python-virtual-environment)

# JSON Persistence

## Overview

This Python script demonstrates data persistence with the `json` module. It writes match statistics to "data.json" and reads it back.

## Functions

### `load_json()`

- **Write:** Saves the provided `data` dictionary.
  ```python
  with open("data.json", "w") as json_data_file:
      json.dump(data, json_data_file)

- **Read:** Retrieves data.

```python
with open("data.json", "r") as json_data_file:
    loaded_data = json.load(json_data_file)

```
