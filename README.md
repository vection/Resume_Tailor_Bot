# 🤖 Job Genius Bot

## Table of Contents

- [Overview](#overview)
- [Initial Requirements](#initial-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Job Genius Bot is a Discord bot designed to assist users in their job search process. It provides job alerts and offers custom resume generation based on user input and job descriptions. With this bot, users can streamline their job search, receive notifications for new job posts, and generate tailored resumes to match specific job requirements.

## Initial Requirements
Before running the Job Genius Bot, make sure you have the following requirements in place:

- **OpenAI API Key**: You need an OpenAI API key to utilize the AI-powered features of the bot, such as generating custom resumes and interview questions. You can obtain an API key by signing up for OpenAI services.

- **LinkedIn Account**: The bot requires a LinkedIn account to fetch job listings. Make sure you have a valid LinkedIn account with appropriate credentials.

- **Discord Token**: To use the bot on Discord, you'll need a Discord token. Create a Discord bot and obtain its token by following the Discord Developer Portal guidelines.

## Installation

1. Clone the repository:
git clone https://github.com/vection/JobGenius.git


2. Install the required dependencies:
pip install -r requirements.txt

**Note**: Make sure you have installed [wkhtmltopdf](https://wkhtmltopdf.org/).

3. Configure the bot:
- Open the `config.ini` file and adjust the necessary settings.
- Set up your Discord bot token, LinkedIn credentials, and OpenAI API keys in the `config.ini` file.

4. Run the bot:
python bot.py

**Note**: There is a Dockerfile provided if you prefer running the bot in a Docker container. Please be aware that Docker creates a separate environment, and files may be saved locally.


## Usage

1. Registration:
- Use the `!register` command to register with the bot and provide your name.
- Specify your job keywords for job alerts and provide your work experience and personal projects.
In the registration process, it is important to provide as much detail as possible about your work and personal experience. Include relevant information such as job titles, company names, dates of employment, and a description of your responsibilities and achievements. Additionally, include details about your education, such as degree names, institution names, and graduation dates. The more descriptive and accurate the information you provide, the better the bot will be able to generate tailored resumes for you.

3. Job Search:
- Use the `!jobs <num_jobs> [COMPANY_OPTIONAL]` command to fetch the newest jobs based on your registered keywords.
- Specify the number of jobs to fetch and optionally add a company filter to narrow down the job search.

3. Custom Resume Generation:
- Use the `!generate <job_id>` command to generate a custom resume based on your information and a specific job description.
- Provide the job ID of the desired job for resume generation.

4. Other Commands:
- `!stats`: View your registration information and statistics.
- `!delete`: Delete your registration from the bot.
- `!alert <num_seconds>`: Set up job alerts to receive notifications at the specified interval.
- `!questions <job_id>`: Generate possible interview questions based on a job post.

## Features

- User registration and customization of job keywords and personal information.
- Fetching and displaying the newest jobs based on registered keywords.
- Custom resume generation based on job descriptions using AI-powered methods.
- Job alerts to receive notifications about new job posts.
- Interview question generation based on job descriptions.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## License

This project is licensed under the [MIT License](LICENSE).
