from linkedin_api import Linkedin
from multiprocessing.pool import ThreadPool
import pandas as pd
import os


class LinkApi:
    def __init__(self, user, password):
        """
            Initialize the LinkApi class.

            Args:
                user (str): The LinkedIn username.
                password (str): The LinkedIn password.
        """
        self.api = Linkedin(user, password)

    def get_job_posts(self, jobs):
        """
           Get the job posts and their details.

           Args:
               jobs (list): A list of job items retrieved from a job search.

           Returns:
               tuple: A tuple containing the job posts and their IDs.
        """
        post_ids = [job_item['dashEntityUrn'].split(":")[-1] for job_item in jobs if
                    int(job_item['dashEntityUrn'].split(":")[-1]) > 0]

        def get_json_job(p_id):
            try:
                return self.api.get_job(p_id)
            except:
                return None

        with ThreadPool(os.cpu_count()) as p:
            result = p.map(get_json_job, post_ids)

        return result, post_ids

    def get_jobs(self, config,text, limit=10, add_filter=None):
        """
            Get jobs based on search criteria.

            Args:
                config (dict): Configuration settings.
                text (str): The search text.
                limit (int): The maximum number of jobs to retrieve. Default is 10.
                add_filter (str): An additional filter to apply. Default is None.

            Returns:
                list: A list of job records in dictionary format.
        """
        all_jobs = pd.DataFrame()
        company_names = []
        posts_text = []
        posts_timestamp = []
        posts_ids = []
        posts_urls = []
        posts_title = []
        if isinstance(add_filter,str):
            limit = 200
        jobs = self.api.search_jobs(text, location_name=config['location'], listed_at=int(config['listed_time']), limit=limit)
        job_posts, job_posts_ids = self.get_job_posts(jobs)
        for job_post, job_posting_id in zip(job_posts, job_posts_ids):
            if job_post is None:
                company_names.append(None)
                posts_text.append(None)
                posts_timestamp.append(None)
                posts_ids.append(None)
                posts_urls.append(None)
                posts_title.append(None)
                continue

            job_post_text = job_post['description']['text']

            try:
                job_post_company_name = \
                    job_post['companyDetails'][list(job_post['companyDetails'].keys())[0]]['companyResolutionResult'][
                        'name']
                job_post_company_url = \
                    job_post['companyDetails'][list(job_post['companyDetails'].keys())[0]]['companyResolutionResult'][
                        'url']
            except:
                job_post_company_name = None
                job_post_company_url = None
            job_post_timestamp = job_post['listedAt']
            job_post_title = job_post['title']

            if isinstance(add_filter, str) and isinstance(job_post_company_name,str):
                if add_filter.lower() not in job_post_company_name.lower():
                    continue

            job_apply_method = job_post['applyMethod']
            if 'com.linkedin.voyager.jobs.OffsiteApply' in job_apply_method:
                apply_url = job_apply_method['com.linkedin.voyager.jobs.OffsiteApply']['companyApplyUrl']
            elif 'com.linkedin.voyager.jobs.ComplexOnsiteApply' in job_apply_method:
                apply_url = job_apply_method['com.linkedin.voyager.jobs.ComplexOnsiteApply']['easyApplyUrl']
            else:
                apply_url = f'https://www.linkedin.com/jobs/{job_posting_id}/?currentJobId={job_posting_id}'

            company_names.append(job_post_company_name)
            posts_text.append(job_post_text)
            posts_timestamp.append(job_post_timestamp)
            posts_ids.append(job_posting_id)
            posts_urls.append(apply_url)
            posts_title.append(job_post_title)

        all_jobs['company_name'] = company_names
        all_jobs['post_title'] = posts_title
        all_jobs['post_id'] = posts_ids
        all_jobs['job_post_text'] = posts_text
        all_jobs['time_created'] = posts_timestamp
        all_jobs['post_url'] = posts_urls

        return all_jobs.to_dict(orient='records')
