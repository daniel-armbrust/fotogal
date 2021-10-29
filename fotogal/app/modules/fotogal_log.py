#
# fotogal/app/modules/fotogal_log.py
#

import datetime
import logging

import oci


class OciLoggingHandler(logging.Handler):
    """Custom class for OCI Logging Service.

    """        
    _oci_config = None
    _loggroup_name = None
    _customlog_name = None
    _log_id = None

    def __init__(self, oci_config, loggroup_name, customlog_name):             
        super(OciLoggingHandler, self).__init__()

        self._oci_config = oci_config
        self._loggroup_name = loggroup_name
        self._customlog_name = customlog_name

        self._log_id = self.__get_customlog_id()
        
    def __get_customlog_id(self):
        """Return the custom log OCID from "OCI Log Group" and "OCI Custom Log".

        """
        log_mgmt = oci.logging.LoggingManagementClient(self._oci_config)
        log_group = log_mgmt.list_log_groups(self._oci_config['compartment'], display_name=self._loggroup_name)

        if len(log_group.data) > 0:
            log_group_id = log_group.data[0].id    
            customlog_list = log_mgmt.list_logs(log_group_id=log_group_id, log_type='CUSTOM')

            for log_data in customlog_list.data:
                if log_data.display_name == self._customlog_name:
                    return log_data.id

        return None

    def __get_datetime_now(self):
        datetime_now = datetime.datetime.now()
        
        return '%04d-%02d-%02dT%02d:%02d:%02d.%03dZ' % (datetime_now.year,
            datetime_now.month, datetime_now.day, datetime_now.hour,
            datetime_now.minute, datetime_now.second, datetime_now.microsecond / 1000,)

    def emit(self, record):
        log_entry = self.format(record)

        datatime_now = self.__get_datetime_now()

        oci_log_client = oci.loggingingestion.LoggingClient(self._oci_config)      

        # TODO: if fail to send the logs, send it to the console stream.
        put_logs_response = oci_log_client.put_logs(log_id=self._log_id, 
            put_logs_details=oci.loggingingestion.models.PutLogsDetails(specversion='1.0',
                log_entry_batches=[oci.loggingingestion.models.LogEntryBatch(
                entries=[
                    oci.loggingingestion.models.LogEntry(
                        data=log_entry,
                        id='fotogal_app_log',
                        time=datatime_now
                    )],
                source='fotogal_app_log',
                type='br.com.ocibook.fotogal',
                defaultlogentrytime=datatime_now,
                subject="")]))


class FotogalLog():
    """Create log handler to send records to OCI.

    """   
    @staticmethod
    def create_handler(oci_config, oci_loggroup_name, oci_customlog_name):                        
        log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')        

        log_handler = OciLoggingHandler(oci_config, oci_loggroup_name, oci_customlog_name)        
        log_handler.setFormatter(log_formatter)
        
        return log_handler

    def log(self):
        pass