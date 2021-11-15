"""
##########################
@author: Avi Zaguri
Application Name: .csv to .vcf convertor
version: 1.0
##########################
"""

import sys
import logging
import pandas as pd

from Infrastructure.Logger_Infrastructure.Projects_Logger import ProjectsLogging


class CSVToVCFConvertorClass:
    def __init__(self):
        self.logger = \
            logging.getLogger('Infrastructure.Logger_Infrastructure.Projects_Logger.' + self.__class__.__name__)

    def csv_to_vcf_convertor(self, path_to_save):
        try:
            # assuming file format : ['last_name', 'first_name', 'phone_number', 'mail']
            dataframe = pd.read_csv(path_to_save)
            dataframe = dataframe.fillna('')

            all_vcf = open("Contacts.vcf", "w")

            for index, row in dataframe.iterrows():
                # self.logger.info(row)
                all_vcf.write(f"BEGIN:VCARD\n")
                all_vcf.write(f"VERSION:2.1\n")

                all_vcf.write(f"N:'{row['last_name']};{row['first_name']}\n")
                all_vcf.write(f"FN:{row['organization']} {row['first_name']} {row['last_name']}\n")
                all_vcf.write(f"ORG:{row['organization']}\n")
                all_vcf.write(f"TEL;CELL:0{row['phone_number']}\n")
                all_vcf.write(f"EMAIL:{row['mail']}\n")

                all_vcf.write(f"END:VCARD\n")
                all_vcf.write(f"\n")
            all_vcf.close()
            self.logger.debug(f'Finish csv_to_vcf_convertor function')
        except Exception:
            logger.exception('')


def main(args):
    try:
        if len(args) == 2:
            CSVToVCFConvertorClass().csv_to_vcf_convertor(args[1])
        else:
            logger.info('There is more than one parameter.\n'
                        'Please, send only the path to save the .vcf file')
        logger.debug('Finish main function')
        return
    except Exception:
        logger.exception('')


if __name__ == '__main__':
    print('Start .csv to .vcf convertor script')

    logger = ProjectsLogging('.csvTo.vcfConvertor').project_logging()
    logger.info('Start .csv to .vcf convertor script')

    try:
        argv_list = sys.argv  # ['', path_to_save]
        argv_list = ['', 'Contacts.csv']

        logger.info(argv_list)
        main(argv_list)
        logger.debug('Finish __main__ - csv_to_vcf_convertor')
    except Exception:
        logger.exception('')
