import os
import time
import yaml

from PrivateInfrastructure.Logger_Infrastructure.Projects_Logger import ProjectsLogging
from PythonApplications.TriggerProcessByYaml.actual_process import ProcessClass

PROJECT_NAME = "Deleter"


def get_yaml_dict_test(yaml_path):
    yaml_ = None
    try:
        with open(yaml_path) as yaml_file:
            yaml_ = yaml.load(yaml_file, Loader=yaml.FullLoader)
    except Exception as err:
        logger.error(err)
    return yaml_


def get_yaml_dict(yaml_path):
    with open(yaml_path) as yaml_file:
        yaml_ = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return yaml_


if __name__ == '__main__':
    print('')
    print('################################')
    print(f'### Start {PROJECT_NAME} Process ###')
    print('################################')
    print('')
    time.sleep(1)

    try:
        log_path = f'C:\\Python Logs\\{PROJECT_NAME}'
        log_file_name = f'{PROJECT_NAME}_logs'
        logger = ProjectsLogging(project_name=PROJECT_NAME, path=log_path, file_name=log_file_name).project_logging()
        logger.info(f'Start {PROJECT_NAME} Process')
        time.sleep(1)

        yaml_full_path = f'sut.yaml'
        # yaml_full_path = input(f'Please, set a full yaml path: ')
        yaml_dict = get_yaml_dict(yaml_full_path)
        logger.debug(yaml_dict)

        parameters_dict = {
            'server_path': yaml_dict["GlobalConfiguration"]["server_path"],
            'recursive': yaml_dict["GlobalConfiguration"]["recursive"],

            'patterns': yaml_dict["GlobalConfiguration"]["patterns"],

            'only_include_part_name': yaml_dict["GlobalConfiguration"]["only_include_part_name"],
            'exclude_part_name': yaml_dict["GlobalConfiguration"]["exclude_part_name"],

            'time_delta_days': yaml_dict["HowLongBackCheck"]["time_delta_days"],
            'time_delta_hours': yaml_dict["HowLongBackCheck"]["time_delta_hours"],
            'time_delta_minutes': yaml_dict["HowLongBackCheck"]["time_delta_minutes"]
        }

        while yaml_dict['StartOrStopProcess']['start_or_stop_process']:
            if (parameters_dict['server_path'] and parameters_dict['recursive'] and parameters_dict['patterns']) and \
                    (parameters_dict['only_include_part_name'] and parameters_dict['exclude_part_name']):
                ProcessClass_ = ProcessClass(**parameters_dict)

                if parameters_dict['recursive']:
                    for path_to_file, d, files in os.walk(parameters_dict['server_path']):
                        ProcessClass_.process(path_to_file, files)
                else:
                    path_to_file = list(os.walk(parameters_dict['server_path']))[0][0]
                    files = list(os.walk(parameters_dict['server_path']))[0][2]
                    ProcessClass_.process(path_to_file, files)
                logger.info(f'cycle interval is: {yaml_dict["GlobalConfiguration"]["cycle_interval"]}')
                time.sleep(yaml_dict["GlobalConfiguration"]["cycle_interval"])

                patterns = yaml_dict["GlobalConfiguration"]["patterns"]
            else:
                logger.error(f'Part of the parameters '
                             f'("server_path", "recursive", "patterns", "only_include_part_name", "exclude_part_name") '
                             f'were not defined')
                logger.debug(f'cycle interval is: {yaml_dict["GlobalConfiguration"]["cycle_interval"]}')
                time.sleep(yaml_dict["GlobalConfiguration"]["cycle_interval"])
                continue
    except Exception as error:
        print(error)
