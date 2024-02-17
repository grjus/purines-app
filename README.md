# Purine Content Tracker

## Overview
The Purine Content Tracker is a simple application designed to list the amount of purine acid in various food products. It serves as a practical tool for individuals looking to manage their purine intake, often crucial for those with conditions like gout or kidney stones. This project was created as a means to explore the integration of HTMX, FastAPI, Jinja templating system, and deployment on Fly.io.

## Features
- **Purine Content Listing:** Access a comprehensive list of food products along with their purine acid content.
- **Fast and Efficient Backend:** Built with FastAPI


## Technologies
- [HTMX](https://htmx.org/): Offers high power and flexibility for building modern web applications with fewer complexities.
- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- [Jinja](https://jinja.palletsprojects.com/): A full-featured template engine for Python.
- [Docker](https://www.docker.com/): Used for containerizing the application, ensuring it runs consistently across different environments.
- [Fly.io](https://fly.io/): For deploying and hosting the application, offering easy scalability and global distribution.

## Getting Started

### Prerequisites
- Docker installed on your machine
- Basic understanding of Python, Docker, and web development

### Setup and Installation

1. **Clone the Repository**
 

2. **Build the Docker Container**
    ```bash
    docker build -t purine-content-tracker .
    ```

3. **Run the Application**
    ```bash
    docker run -d -p 80:80 purine-content-tracker
    ```

The application should now be running and accessible via `http://localhost` or the configured port.