import sqlite3
from jenkins import DEFAULT_TIMEOUT, JOBS_QUERY_TREE, JOBS_QUERY, Jenkins
from gitlab_ps_utils.processes import MultiProcessing
from gitlab_evaluate.migration_readiness.jenkins.data_classes.job import Job
class MultiProcessJenkins(Jenkins):
    """
        Extended class to multiprocess retrieving job data
    """
    def __init__(self, url, username=None, password=None, timeout=DEFAULT_TIMEOUT):
        super().__init__(url, username, password, timeout)
        self.multi = MultiProcessing()
        self.num_jobs = 0

    def jobs_count(self):
        '''Get the number of jobs on the Jenkins server

        :returns: Total number of jobs, ``int``
        '''
        if self.num_jobs:
            return self.num_jobs
        else:
            return len(self.get_all_jobs())

    def get_jobs(self, folder_depth=0, folder_depth_per_request=10, view_name=None):
        """Get list of jobs.

        Each job is a dictionary with 'name', 'url', 'color' and 'fullname'
        keys.

        If the ``view_name`` parameter is present, the list of
        jobs will be limited to only those configured in the
        specified view. In this case, the job dictionary 'fullname' key
        would be equal to the job name.

        :param folder_depth: Number of levels to search, ``int``. By default
            0, which will limit search to toplevel. None disables the limit.
        :param folder_depth_per_request: Number of levels to fetch at once,
            ``int``. See :func:`get_all_jobs`.
        :param view_name: Name of a Jenkins view for which to
            retrieve jobs, ``str``. By default, the job list is
            not limited to a specific view.
        :returns: list of jobs, ``[{str: str, str: str, str: str, str: str}]``

        Example::

            >>> jobs = server.get_jobs()
            >>> print(jobs)
            [{
                u'name': u'all_tests',
                u'url': u'http://your_url.here/job/all_tests/',
                u'color': u'blue',
                u'fullname': u'all_tests'
            }]

        """

        if view_name:
            return self._get_view_jobs(name=view_name)
        else:
            return self.get_all_jobs(folder_depth=folder_depth,
                                     folder_depth_per_request=folder_depth_per_request)

    def get_all_jobs(self, folder_depth=None, folder_depth_per_request=10):
        """Get list of all jobs recursively to the given folder depth.

        Each job is a dictionary with 'name', 'url', 'color' and 'fullname'
        keys.

        :param folder_depth: Number of levels to search, ``int``. By default
            None, which will search all levels. 0 limits to toplevel.
        :param folder_depth_per_request: Number of levels to fetch at once,
            ``int``. By default 10, which is usually enough to fetch all jobs
            using a single request and still easily fits into an HTTP request.
        :returns: list of jobs, ``[ { str: str} ]``

        .. note::

            On instances with many folders it would not be efficient to fetch
            each folder separately, hence `folder_depth_per_request` levels
            are fetched at once using the ``tree`` query parameter::

                ?tree=jobs[url,color,name,jobs[...,jobs[...,jobs[...,jobs]]]]

            If there are more folder levels than the query asks for, Jenkins
            returns empty [#]_ objects at the deepest level::

                {"name": "folder", "url": "...", "jobs": [{}, {}, ...]}

            This makes it possible to detect when additional requests are
            needed.

            .. [#] Actually recent Jenkins includes a ``_class`` field
                everywhere, but it's missing the requested fields.
        """
        jobs_query = 'jobs'
        for _ in range(folder_depth_per_request):
            jobs_query = JOBS_QUERY_TREE % jobs_query
        jobs_query = JOBS_QUERY % jobs_query

        jobs_list = []
        job_types = []
        jobs_to_process = []
        jobs_to_process.append((0, [], self.get_info(query=jobs_query)['jobs']))
        self.multi.start_multi_process_stream_with_args(self.handle_retrieving_job_level, jobs_to_process, folder_depth, jobs_query, jobs_to_process, nestable=True)
        con = sqlite3.connect('jenkins.db')
        cur = con.cursor()
        job_results = cur.execute("SELECT * FROM jobs")
        for result in job_results.fetchall():
            jobs_list.append(Job(*result).to_dict())
        job_type_results = cur.execute("SELECT * FROM job_types")
        for result in job_type_results.fetchall():
            job_types.append(result[0])
        con.close()
        self.num_jobs = len(jobs_list)
        return jobs_list, job_types

    def handle_retrieving_job_level(self, folder_depth, jobs_query, jobs_to_process, job_level: tuple):
        
        lvl, root, lvl_jobs = job_level
        if not isinstance(lvl_jobs, list):
            lvl_jobs = [lvl_jobs]
        self.multi.start_multi_process_stream_with_args(self.handle_retrieving_job, lvl_jobs, lvl, root, folder_depth, jobs_query, jobs_to_process)
        
    
    def handle_retrieving_job(self, lvl, root, folder_depth, jobs_query, jobs_to_process, job):
        con = sqlite3.connect('jenkins.db')
        cur = con.cursor()
        path = root + [job[u'name']]
        # insert fullname info if it doesn't exist to
        # allow callers to easily reference unambiguously
        if u'fullname' not in job:
            job[u'fullname'] = '/'.join(path)
        try:
            cur.execute(f"INSERT INTO jobs VALUES {tuple(job.values())}")
            con.commit()
            job_type_check = cur.execute(f"SELECT type FROM job_types WHERE type='{job['_class']}'")
            if not job_type_check.fetchone():
                job_class = job['_class']
                cur.execute(f"INSERT INTO job_types VALUES ('{job_class}')")
                con.commit()
        except Exception as e:
            print(e)
        if 'jobs' in job and isinstance(job['jobs'], list):  # folder
            if folder_depth is None or lvl < folder_depth:
                children = job['jobs']
                # once folder_depth_per_request is reached, Jenkins
                # returns empty objects
                if any('url' not in child for child in job['jobs']):
                    url_path = ''.join(['/job/' + p for p in path])
                    children = self.get_info(url_path,
                                                query=jobs_query)['jobs']
                jobs_to_process.append((lvl + 1, path, children))
        con.close()
