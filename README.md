# 🤖 Job Genius Bot

## Table of Contents

- [Overview](#overview)
- [Initial Requirements](#initial-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [AI Configuration Settings](#ai-configuration-settings)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Job Genius Bot is a Discord bot designed to assist users in their job search process using advanced generative AI tools. It provides job alerts and offers custom resume generation based on user input and job descriptions. With this bot, users can streamline their job search, receive notifications for new job posts, and generate tailored resumes to match specific job requirements.

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

## AI Configuration Settings
- enhance_start: This setting determines whether the AI should enhance the original description of the resume. When set to True, the AI will attempt to improve the description of the candidate. The default value is False.

- enhance_start_temperature: The temperature parameter controls the randomness of the AI's responses during the process of enhancing the user description. Higher values (e.g., 0.9) make the output more random, while lower values (e.g., 0.1) make it more deterministic. The default temperature for enhancing the start is set to 0.9.

- enhance_end: This setting determines whether the AI should enhance the experience and summary of the resume. When set to True, the AI will attempt to improve the concluding section of the generated better results. The default value is True.

- enhance_end_summary_temperature: The temperature parameter controls the randomness of the AI's responses during the process of enhancing the end of the summary section in the custom resume. The default temperature for enhancing the end of the summary is set to 0.9.

- enhance_end_experience_temperature: The temperature parameter controls the randomness of the AI's responses during the process of enhancing the end of the experience section in the custom resume. The default temperature for enhancing the end of the experience is set to 0.9.

- resume_generation_temperature: The temperature parameter controls the randomness of the AI's responses during the process of generating the custom resume tailored to job description. Higher values (e.g., 1.0) make the output more random, while lower values (e.g., 0.1) make it more deterministic. The default temperature for resume generation is set to 1.0.

- description_temperature: The temperature parameter controls the randomness of the AI's responses when extracting relevant qualities from the job description. Higher values (e.g., 0.9) make the output more random, while lower values (e.g., 0.1) make it more deterministic. The default temperature for description extraction is set to 0.9.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## Images
<img src="https://github.com/vection/JobGenius/assets/28596354/c2a4324b-59d5-4546-9108-096c9c63c5e4" width=50% height=50%>
<img src="https://github.com/vection/JobGenius/assets/28596354/83ff8f90-5b64-4b15-8cf6-bedc8d7cfa18" width=50% height=50%>
<img src="https://github.com/vection/JobGenius/assets/28596354/579f7b19-b1db-4d5a-806c-7b91cb320eb4" width=50% height=50%>
<img src="https://github.com/vection/JobGenius/assets/28596354/a3e5c71c-2022-4451-9b01-222a0fa69aad" width=50% height=50%>
<img src="https://github.com/vection/JobGenius/assets/28596354/24304b65-ff3a-4c79-a8ff-9409d5380cfa" width=50% height=50%>
<img src="https://github.com/vection/JobGenius/assets/28596354/a762d5c7-0eed-4da1-a7b4-2c46c40a3910" width=50% height=50%>


## License

This project is licensed under the [MIT License](LICENSE).
