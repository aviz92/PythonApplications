import os
import logging
from termcolor import colored
from datetime import datetime, timedelta


class ProcessClass:
    def __init__(self, **kwargs):
        self.logger = \
            logging.getLogger('Infrastructure.Logger_Infrastructure.Projects_Logger.' + self.__class__.__name__)

        self.server_path = kwargs.get('server_path')
        self.recursive = kwargs.get('recursive')
        self.patterns = kwargs.get('patterns')

        self.only_include_part_name = kwargs.get('only_include_part_name')
        self.exclude_part_name = kwargs.get('exclude_part_name')

        self.time_delta_days = kwargs.get('time_delta_days')
        self.time_delta_hours = kwargs.get('time_delta_hours')
        self.time_delta_minutes = kwargs.get('time_delta_minutes')

        if not self.time_delta_days or not self.time_delta_hours or not self.time_delta_minutes:
            self.logger.info(
                f'The parameters ("time_delta_days", "time_delta_hours" and "time_delta_minutes") were not defined '
                f'and are therefore equal to zero'
            )
            self.time_delta_days = 0
            self.time_delta_hours = 0
            self.time_delta_minutes = 0

    def process(self, path_to_file, files):
        self.logger.info('\n\n')
        try:
            for file in files:
                try:
                    mtime = os.path.getmtime(f'{path_to_file}\\{file}')
                except OSError:
                    mtime = datetime.now()
                last_modified_date = datetime.fromtimestamp(mtime)

                if last_modified_date < datetime.now() - timedelta(days=self.time_delta_days,
                                                                   hours=self.time_delta_hours,
                                                                   minutes=self.time_delta_minutes):
                    flag = False
                    if file.split(".")[-1] in self.patterns:
                        if self.only_include_part_name:
                            flag = [True for include_name in self.only_include_part_name if include_name in file]
                        else:
                            pass
                        if self.exclude_part_name:
                            flag = [True for exclude_name in self.exclude_part_name if exclude_name not in file]
                        else:
                            pass

                        if flag:
                            os.system(f'del /f "{path_to_file}\\{file}')
                            self.logger.info(
                                f'\nDelete the file: '
                                f'\n{path_to_file}\\{file}'
                            )
                            self.logger.info(
                                f'\nBecause the last modified date < current date '
                                f'\n{last_modified_date} < {datetime.now()-timedelta(days=10, hours=0, minutes=0)}'
                            )
                    else:
                        pass
                else:
                    pass
        except Exception:
            self.logger.exception(colored('Get "last_line" doesnt work', 'red'))
