import os
import time
import logging
from datetime import datetime
from datetime import timedelta
import csv
import pandas as pd

from PrivateInfrastructure.Files_Infrastructure.Folders.Path_folders_Infrastructure import GeneralFolderActionClass
from PrivateInfrastructure.Network_Infrastructure.IP_Address_Network_Infrastructure import IPAddressNetworkClass


class FileListener:
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(f'PrivateInfrastructure.Logger_Infrastructure.Projects_Logger.{self.__class__.__name__}')

        self.PATTERNS = kwargs.get('PATTERNS')
        self.HOST_NAME = kwargs.get('HOST_NAME')
        self.SERVER_PATH = kwargs.get('SERVER_PATH')
        self.LAST_ROW_INDEX_PATH = kwargs.get('LAST_ROW_INDEX_PATH')
        self.RECURSIVE = kwargs.get('RECURSIVE')
        self.days_before = kwargs.get('days_before')
        self.old_size = kwargs.get('old_size')

    def find_files_changes(self):
        # Find files changes (create/update files)
        new_size = GeneralFolderActionClass().get_folder_size(self.SERVER_PATH)
        if new_size == 0 or new_size < self.old_size:
            self.old_size = 0

        if new_size > self.old_size:
            self.old_size = new_size
            file_name_list = []
            for r, d, f in os.walk(self.SERVER_PATH):
                for file in f:
                    file_name_list.append(os.path.join(r, file).replace(self.SERVER_PATH + "\\", ""))
                if not self.RECURSIVE:
                    break
        else:
            return False, []
        return True, file_name_list

    def check_file_till_days(self, file_name):
        # check file till "days_before" days
        if file_name.split(".")[-1] not in self.PATTERNS or 'CORE_SUMMARY_' not in file_name:
            return False
        elif 'CORE_SUMMARY_' in file_name:
            file_date = datetime.strptime(file_name.split('CORE_SUMMARY_')[1][:-4], '%Y_%m_%d')
            if 'CORE_SUMMARY_' in file_name and file_date < datetime.today() - timedelta(days=self.days_before):
                # self.logger.debug(f'"{file_name}" date < current date in {self.days_before} days')
                return False
        return True

    def add_or_update_last_index(self, file_name):
        # Load summary file and create new row (file name, last index)
        path_summary_file = self.SERVER_PATH + "\\" + file_name
        dataframe_summary_file = pd.read_csv(path_summary_file)
        summary_last_index = [file_name, dataframe_summary_file.index.__len__() + 1]

        old_summary_last_index = 0
        if GeneralFolderActionClass().check_path_exist(self.LAST_ROW_INDEX_PATH):
            # Load and get the old last index from "last_index_of_summery_cores.csv" file
            dataframe_last_index_summery_file = pd.read_csv(self.LAST_ROW_INDEX_PATH)
            dataframe_old_summary_last_index = \
                dataframe_last_index_summery_file.loc[dataframe_last_index_summery_file['file name'] == file_name]

            # Check for changes in the file
            if dataframe_old_summary_last_index.shape[0] > 0:
                dataframe_last_index_summery_file = \
                    dataframe_last_index_summery_file.sort_values('last index').drop_duplicates('file name',
                                                                                                keep='last')
                old_summary_last_index = int(dataframe_old_summary_last_index['last index'].values[0]) - 1

            if old_summary_last_index == summary_last_index[1]:
                return False, 0

            # Add row to "last_index_of_summery_cores.csv" file
            columns = ['file name', 'last index']
            if len(summary_last_index) == len(columns):
                new_row = pd.DataFrame([summary_last_index], columns=columns)
                dataframe_last_index_summery_file = pd.concat([dataframe_last_index_summery_file, new_row],
                                                              ignore_index=False)
            else:
                self.logger.error(f'len_row != len_columns \n{len(summary_last_index) != len(columns)}')

            dataframe_last_index_summery_file = \
                dataframe_last_index_summery_file.sort_values('last index').drop_duplicates('file name', keep='last')
            dataframe_last_index_summery_file = dataframe_last_index_summery_file.sort_values('file name', ascending=True)
            dataframe_last_index_summery_file.to_csv(self.LAST_ROW_INDEX_PATH, mode='w', header=True, index=False)
        else:  # if the file not exist -> create the file
            new_df = pd.DataFrame([summary_last_index], columns=['file name', 'last index'])
            new_df = new_df.sort_values('file name', ascending=True)
            new_df.to_csv(self.LAST_ROW_INDEX_PATH, mode='w', header=True, index=False)

        self.logger.info(f'Save New Row {summary_last_index}')
        return True, old_summary_last_index

    def start_process(self):
        while True:
            self.logger.info('Waiting 3 sec')
            time.sleep(3)
            try:
                # Find files changes (create/update files)
                find_changes, file_name_list = self.find_files_changes()
                if not find_changes:
                    continue
            except FileExistsError:
                self.logger.exception("except_1 FileExistsError")
                continue
            except Exception:
                self.logger.exception('except_1 Exception')
                while True:
                    if IPAddressNetworkClass(ip_address=f'{self.HOST_NAME}').check_ping_status():
                        break
                    else:
                        time.sleep(30)
                continue

            try:
                # check file till "days_before" days
                for index, file_name in enumerate(file_name_list, start=1):
                    if not self.check_file_till_days(file_name=file_name):
                        continue

                    # Load summary file and create new row (file name, last index)
                    find_changes, old_summary_last_index = self.add_or_update_last_index(file_name=file_name)
                    if not find_changes:
                        continue

                    # Start the process
                    try:
                        self.real_process(file_name, old_summary_last_index)
                    except csv.Error:
                        self.logger.exception('except_2 csv.Error')
                        continue
                time.sleep(1)
            except Exception:
                self.logger.exception('except_2 Exception')
                while True:
                    if IPAddressNetworkClass(ip_address=f'{self.HOST_NAME}').check_ping_status():
                        break
                    else:
                        time.sleep(30)
                time.sleep(180)
                continue

    def real_process(self, file_name, old_summary_last_index):
        self.logger.debug(f'{self.SERVER_PATH}\\{file_name}')
        dataframe = pd.read_csv(f'{self.SERVER_PATH}\\{file_name}')[old_summary_last_index:]
        dataframe.index += 2
        if len(dataframe):
            self.logger.debug(f'\n{dataframe.head()}')
        else:
            self.logger.debug(f'The len of dataframe is: {len(dataframe)}')
            return
        print()
