import time

from PrivateInfrastructure.Logger_Infrastructure.Projects_Logger import ProjectsLogging
from PythonApplications.FileListener.FileListener_infrastructure import FileListener

# Global configuration
PATTERNS = ["csv"]
RECURSIVE = False

SITE = 'IL_SVG'

# HOST_NAME = 'asil-svg-cores'
# SERVER_PATH = f'\\\\{HOST_NAME}\\SUMMARY'
# LAST_ROW_INDEX_PATH = f'{SERVER_PATH}\\last_index_of_summery_cores.csv'

HOST_NAME = 'asil-azaguri'
SERVER_PATH = f'\\\\{HOST_NAME}\\C$\\Users\\azaguri\\Desktop\\SUMMARY'
LAST_ROW_INDEX_PATH = f'C:\\Users\\azaguri\\PycharmProjects\\Personal_Projects\\Infrastructure\\Projects\\FiveG\\' \
                      f'CoreCare\\data\\{SITE}_Last_Index_Of_Summery_Cores.csv'

if __name__ == '__main__':
    print("\n################################")
    print("### Start CoreCare Process ###")
    print("################################\n")
    time.sleep(1)

    log_file_name = f'CoreCare_Logs_{SITE}'
    log_path = f'C:\\Python Logs\\CoreCare\\{SITE}'
    logger = ProjectsLogging(project_name='CoreCare', path=log_path, file_name=log_file_name).project_logging()
    logger.info(f'Start {log_file_name.replace("_", " ")} Main')

    FileListener(PATTERNS=PATTERNS, HOST_NAME=HOST_NAME, SERVER_PATH=SERVER_PATH,
                 LAST_ROW_INDEX_PATH=LAST_ROW_INDEX_PATH, RECURSIVE=RECURSIVE,
                 days_before=3, old_size=0).start_process()
