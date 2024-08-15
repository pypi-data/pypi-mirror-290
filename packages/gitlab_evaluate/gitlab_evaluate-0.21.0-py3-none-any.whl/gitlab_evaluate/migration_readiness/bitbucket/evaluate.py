import requests

class BitbucketEvaluateClient():
    def __init__(self, host, token):
        self.host = host.rstrip('/') + "/rest/api/1.0"
        self.headers = {'Authorization': f'Bearer {token}'}

    def get_application_properties(self):
        url = f"{self.host}/application-properties"
        return requests.get(url, headers=self.headers)
    
    def get_projects(self):
        url = f"{self.host}/projects"
        return requests.get(url, headers=self.headers)
        
    def get_repos(self, project_key, params=None):
        url = f"{self.host}/projects/{project_key}/repos"
        return requests.get(url, headers=self.headers, params=params)
   
    def get_admin_users(self):
        url = f"{self.host}/admin/users"
        return requests.get(url, headers=self.headers)
    
    def get_users(self):
        url = f"{self.host}/users"
        return requests.get(url, headers=self.headers)
    
    def get_branches(self, project_key, repo_slug):
        url = f"{self.host}/projects/{project_key}/repos/{repo_slug}/branches"
        return requests.get(url, headers=self.headers)
    
    def get_prs(self, project_key, repo_slug):
        url = f"{self.host}/projects/{project_key}/repos/{repo_slug}/pull-requests"
        return requests.get(url, headers=self.headers)
    
    def get_commits(self, project_key, repo_slug):
        url = f"{self.host}/projects/{project_key}/repos/{repo_slug}/commits"
        return requests.get(url, headers=self.headers)
    
    def get_repo_size(self, repo):
        #grab the repo url and build the url to get repo size
        repoURL = repo['links']['self'][0]['href'].replace('/browse', '/sizes')
        #get repo size
        response = requests.request("GET", repoURL, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch repository size for repo {repoURL}: {response.status_code} - {response.text}")
        response_json = response.json()
        #convert size to MB
        repoSize = (response_json['repository'] + response_json['attachments']) / 1024 / 1024
        return round(repoSize,2)
    
    def get_tags(self, project_key, repo_slug):
        url = f"{self.host}/projects/{project_key}/repos/{repo_slug}/tags"
        return requests.get(url, headers=self.headers)
    
    def is_repo_archived(self, project_key, repo_slug):
        url = f"{self.host}/projects/{project_key}/repos/{repo_slug}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            repo_info = response.json()
            return repo_info.get('archived', False)
        response.raise_for_status()
        return False
    