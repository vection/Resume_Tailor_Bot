import openai
import os, time
from copy import deepcopy
import ast


def set_params(org, key):
    """
       Set the OpenAI organization and API key.

       Args:
           org (str): The OpenAI organization.
           key (str): The OpenAI API key.
    """
    openai.organization = org
    openai.api_key = key


def get_custom_resume(config, resume, job_description, enhance_end=True, enhance_start=False):
    """
        Generate a custom resume based on a given resume and job description.

        Args:
            config (dict): Configuration settings.
            resume (str): The candidate's original resume.
            job_description (str): The job description.
            enhance_end (bool): Flag to enable enhancing the end of the resume. Default is True.
            enhance_start (bool): Flag to enable enhancing the start of the resume. Default is False.

        Returns:
            dict: The generated custom resume in JSON format.
    """
    prompt = """You are expert recruiter and you need to rewrite candidate experience resume according to job qualities.
The final resume should be highly matched to job post profile. You are not allowed to lie about work experience or educational facts.
Your output should be in JSON format and follow the structure outlined below:
{
  "Name": "",
  "Contact_Info" : {"Email" : "", "Phone Number": ""}
  "Summary": "",
  "Education": [
    {
      "degree": "",
      "university": "",
      "dates": ""
    }
  ],
  "Experience": [
    {
      "title": "",
      "company name": "",
      "dates": "",
      "description": ""
    }
  ],
  "skills": [],
  "note": ""
}
"""
    print("DEBUG: Extract qualities from job description")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "this is job post, extract the relevant qualities needed to get the job"},
                {"role": "user", "content": job_description}
            ],
            temperature=float(config['description_temperature']),
            # max_tokens=1000,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        job_description = response["choices"][0]["message"]["content"]
    except:
        time.sleep(1)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Your job is to fix and correct misspelled words by given text. make it reacher and more understandable."},
                {"role": "user", "content": job_description}
            ],
            temperature=float(config['description_temperature']),
            # max_tokens=1000,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )

    job_description = response["choices"][0]["message"]["content"]

    if enhance_start:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Reflect on a meaningful work experience or personal experience and rewrite the paragraph to provide a vivid and detailed account. Include specific examples, challenges overcome, skills acquired, and the overall impact of the experience."},
                    {"role": "user", "content": resume}
                ],
                temperature=float(config['enhance_start_temperature']),
            )
        except:
            time.sleep(1)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Reflect on a meaningful work experience or personal experience and rewrite the paragraph to provide a vivid and detailed account. Include specific examples, challenges overcome, skills acquired, and the overall impact of the experience."},
                    {"role": "user", "content": resume}
                ],
                temperature=float(config['enhance_start_temperature']),
            )

        resume = response["choices"][0]["message"]["content"]

    prompt_to_ask = f"""

Candidate experience:

{resume}

Job Qualities:

{job_description}


"""
    print("DEBUG: Start Generating")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": prompt_to_ask}
            ],
            temperature=float(config['resume_generation_temperature']),
        )
    except:
        time.sleep(1)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": prompt_to_ask}
            ],
            temperature=float(config['resume_generation_temperature']),
        )

    new_resume = ast.literal_eval(response["choices"][0]["message"]["content"])

    temp = {}
    temp['summary'] = deepcopy(new_resume['Summary'])
    temp['experience'] = deepcopy(new_resume['Experience'])

    if enhance_end:
        print("Enhancing extra text")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Reflect on a meaningful work experience or personal experience and rewrite the paragraph to provide a vivid and detailed account. Include specific examples, challenges overcome, skills acquired, and the overall impact of the experience. the output should not be long remember its summary paragraph."},
                    {"role": "user", "content": new_resume['Summary']}
                ],
                temperature=float(config['enhance_end_summary_temperature']),
            )
        except:
            time.sleep(1)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Reflect on a meaningful work experience or personal experience and rewrite the paragraph to provide a vivid and detailed account. Include specific examples, challenges overcome, skills acquired, and the overall impact of the experience. the output should not be long remember its summary paragraph."},
                    {"role": "user", "content": new_resume['Summary']}
                ],
                temperature=float(config['enhance_end_summary_temperature']),
            )
        new_resume['Summary'] = response["choices"][0]["message"]["content"]

        for item in new_resume['Experience']:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system",
                         "content": "Take the description of your experience and transform it into a set of creative and accurate bullet points. Each bullet should succinctly highlight specific achievements, responsibilities, and skills developed during your tenure. Use imaginative language, action verbs, and quantifiable results where possible to make the bullet points more impactful and compelling."},
                        {"role": "user", "content": item['description']}
                    ],
                    temperature=float(config['enhance_end_experience_temperature']),
                )
            except:
                time.sleep(1)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system",
                         "content": "Take the description of your experience and transform it into a set of creative and accurate bullet points. Each bullet should succinctly highlight specific achievements, responsibilities, and skills developed during your tenure. Use imaginative language, action verbs, and quantifiable results where possible to make the bullet points more impactful and compelling."},
                        {"role": "user", "content": item['description']}
                    ],
                    temperature=float(config['enhance_end_experience_temperature']),
                )
            item['description'] = response["choices"][0]["message"]["content"]

    return new_resume


## Generate possible inteview questions based on company and job description
def get_possible_questions(company_name, job_description):
    """
        Generate possible interview questions based on a company name and job description.

        Args:
            company_name (str): The name of the company.
            job_description (str): The job description.

        Returns:
            str: The generated interview questions.
    """
    question_prompt = """
Job Description: {}
Company Name: {}

Interview Questions:
1. 
2. 
3. 
...
""".format(job_description, company_name)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Generate interview questions based on the job description and company name"},
            {"role": "user", "content": question_prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]
