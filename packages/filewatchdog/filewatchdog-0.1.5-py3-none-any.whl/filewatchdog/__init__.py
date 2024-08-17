import schedule
import functools, datetime, logging
from pathlib import Path
from time import sleep
from typing import List, Optional, Callable
import os

logger = logging.getLogger("watcher")


class WatcherError(Exception):
    """Base watcher exception"""
    
    pass

class Watcher:
    def __init__(self) -> None:
        self.jobs: List[WatcherJob] = []

    def once(self) -> "WatcherJob":
        job = WatcherJob(self)
        return job

class WatcherJob:

    def __init__(self, watcher: Optional[Watcher] = None, check_period: int = 1, lag: int = 0, breadcrumb: str = 'C:/Temp/breadcrumb.txt'):
        """
        Check the files every `check_period` seconds to see if they exist or are modified and if so, do the job

        breadcrumb is only needed when self.event is 'exist'
        """
        self.breadcrumb: str = breadcrumb
        self.check_period: int = check_period
        self.lag: int = lag
        
        # the job job_func to run
        self.job_func: Optional[functools.partial] = None

        # list of files to watch
        self.files: List[str] = None
        self.mtime_last_check: dict[str, datetime.datetime] = {}

        # 'exist' or 'modified'
        self.event: str = None

        # 'one_of' or 'all_of'
        self.num_of: str = None

        self.watcher: Optional[Watcher] = watcher

    @property
    def modified(self):
        self.event = 'modified'
        return self
    
    @property
    def exist(self):
        self.event = 'exist'
        return self

    @property
    def exists(self):
        self.event = 'exist'
        return self

    def file(self,file_path:str):
        self.num_of = 'one_of'
        self.files = [file_path]
        if Path(file_path).exists():
            self.mtime_last_check.update({file_path:self._get_mtime(file_path)})
        return self
    
    def folder(self,folder_path:str):
        files = []
        if os.path.isdir(folder_path):
            for root,dir,filenames in os.walk(folder_path):
                for file in filenames:
                    files.append(os.path.join(root,file))
            self.one_of(files)
        else:
            raise ValueError(f"Folder path {folder_path} is not a directory")
        return self
            
    def one_of(self, files: List[str]): 
        self.num_of = 'one_of'
        self.files = files
        for file in self.files:
            if Path(file).exists():
                self.mtime_last_check.update({file: self._get_mtime(file)})
        return self
    
    def all_of(self, files: List[str]): 
        self.num_of = 'all_of'
        self.files = files
        for file in self.files:
            if Path(file).exists():
                self.mtime_last_check.update({file: self._get_mtime(file)})
        return self

    def with_breadcumb(breadcrumb: str = 'C:/Temp/breadcrumb.txt'):  # with_breadcumb must come before do or otherwise default breadcrumb will be used
        self.breadcrumb = breadcrumb
        return self
    
    def do(self, job_func: Callable, *args, **kwargs):
        self.job_func = functools.partial(job_func, *args, **kwargs)
        functools.update_wrapper(self.job_func, job_func)
        self._schedule_watcher_job()
        if self.watcher is None:
            raise WatcherError(
                "Unable to a add watcher job. "
                "Job is not associated with watcher"
            )
        self.watcher.jobs.append(self)
        return self

    def check_n_do(self):
        if self.event == 'exist':
            if ((self.num_of=='all_of' and all([Path(file).exists() and bool(Path(file).stat().st_size) for file in self.files])) \
                or (self.num_of=='one_of' and any([Path(file).exists() and bool(Path(file).stat().st_size) for file in self.files]))) \
                    and not Path(self.breadcrumb).exists():
                
                with open(self.breadcrumb, 'w') as f:
                    current_time = datetime.datetime.now().strftime('%H:%M')
                    f.write(f'Found everything in the watchlist at {current_time}. {self.job_func.__name__} will start in {self.lag} seconds.')

                sleep(self.lag)
                self.job_func()

        if self.event == 'modified':
            try:
                if ((self.num_of=='all_of' and all([self._was_modified(file) for file in self.files])) \
                    or (self.num_of=='one_of' and any([self._was_modified(file) for file in self.files]))):

                    sleep(self.lag)
                    self.job_func()
            except FileNotFoundError as e:
                print(f'Watching for modification but the following files are missing: {[file for file in self.files if not Path(file).exists()]}')

    def _get_mtime(self, file: str) -> datetime.datetime:
        """returns timestamp of a file"""
        return datetime.datetime.fromtimestamp(Path(file).stat().st_mtime)

    def _was_modified(self, file: str) -> bool: 
        """`file` was modified in the past `self.check_period` seconds"""
        current_mtime = self._get_mtime(file)
        if self.mtime_last_check[file] != current_mtime:
            self.mtime_last_check.update({file: current_mtime})
            return True
        else:
            return False

    def _schedule_watcher_job(self) -> None:
        schedule.every(self.check_period).second.until(datetime.timedelta(days=10000)).do(self.check_n_do)

default_watcher = Watcher()

def once() -> WatcherJob:
    return default_watcher.once()

def run_pending() -> None:
    schedule.run_pending()