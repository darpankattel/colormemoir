
# ColorMemoir - Colorize Your History
## Introduction
![Colormemoir Logo](https://cdn.discordapp.com/attachments/1141406483062464543/1200781243382497330/logo-no-background.png?ex=65c76dad&is=65b4f8ad&hm=ce95f2ea5ecc4ef463794b6ef0d7a28f270ca1455a0a63bcc52351df94235dae&)

Colormemoir is a project that leverages Convolutional Neural Networks (CNN) to colorize black and white photos. It aims to provide users with a simple and efficient tool to transform historical or grayscale images into vibrant, colored versions.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Django Server](#running-the-django-server)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Have you ever wondered how your black and white family photos would look in color? Colormemoir is here to bring those memories to life. Using advanced CNN techniques, this project allows you to colorize your images effortlessly.

## Features

- Black and white image colorization using CNN.
- User-friendly web interface for easy interaction.
- History tracking of colorization conversions.

## Getting Started

### Prerequisites

Before you start, make sure you have the following installed:

- Python 3.x
- Django

### Installation

#### 1. Clone the repository:

   ```bash
   git clone https://github.com/darpankattel/colormemoir.git
   ```
#### 2. Navigate to the project directory:

```bash
cd colormemoir
```

#### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Django Server
#### 1. Apply migrations:

```bash
python manage.py migrate
```

#### 2. Create a superuser:

```bash
python manage.py createsuperuser
```

#### 3. Run the development server:

```bash
python manage.py runserver
```

Visit http://localhost:8000 to access the Colormemoir web interface.

## Usage
1. Open the Colormemoir web interface in your browser.
2. Sign Up/ Log In to your account.
3. Upload a black and white image.
4. Initiate the colorization process.
5. Check the status and download the colored image once the process is complete.

## Contributing
If you'd like to contribute to ColorMemoir, please follow the Contributing Guidelines.

## License
This project is licensed under the MIT License.