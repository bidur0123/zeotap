# Assignment 1 : Rule Engine


This project is a simple UI-based Rule Engine that enables users to create, modify, and evaluate rules from input data. It comprises a React frontend for the user interface and an Express.js backend, utilizing MongoDB for the storage and evaluation of rules.

## Demo
[Rule Engine Demo Video](https://youtu.be/agFyy1W6DX0)

## Features
- Create new rules by entering rule strings (e.g. : **(age > 30 AND department = "Sales") OR (salary > 50000 AND experience > 5)** ).
- Modify existing rules using an intuitive UI.
- Evaluate rules based on JSON input data and determine eligibility.
- Use JSON-Rules-Engine to evaluate complex conditions.

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)

## Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/bidur0123/zeotap.git
    cd rule-engine
    ```
2. Build and run the app using Docker Compose:
    ```bash
    docker-compose up --build
    ```
# Assignment 2 : Weather Monitoring System

This project monitor real-time weather data for various cities by leveraging the OpenWeatherMap API. It aggregates the weather information in MongoDB and produces visual summaries, which are saved as PNG images.

## Demo
[Weather monitor Demo Video](https://youtu.be/4Rj1GH3bZyc)

## Features

- Real-time weather data fetching.
- Data aggregation (temperature, humidity, wind speed).
- Automatic alerts for high temperatures.
- PNG image visualization of weather summaries.
- Data stored in MongoDB for further analysis.

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- OpenWeatherMap API key ([Sign up here](https://openweathermap.org/api)).

## Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/bidur0123/zeotap.git
    cd weather-monitor
    ```

2. Add your OpenWeatherMap API key in the Python script:
    ```python
    API_KEY = "your_api_key_here"
    ```

3. Build and run the app using Docker Compose:
    ```bash
    docker-compose up --build
    ```

## Output
- Weather summaries are stored in MongoDB.
- Visual summaries are saved as PNG images in the working directory.

