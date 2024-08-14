import logging
import logging.config
import yaml
from typing import Literal

Handlers = Literal["console", "file", "rotating_file"]
Choices = Literal["asctime", "filename", "funcname", "levelname", "lineno", "message", "name", "pathname"]


class LoggoBlocks:
    '''
    Abstracts the configuration of logging, logger can be retrieved
    from self.logger after instantiation of LoggoBlocks.
    '''
    def __init__(self) -> None:
        self.logger_name = ""
        self.config = {}


    @staticmethod
    def logger_from_yaml(fp:str, logger_name:str="default"):
        with open(fp, "r") as file:
            config = yaml.safe_load(file)
        
        logging.config.dictConfig(config)

        return logging.getLogger(logger_name)


    @staticmethod
    def basic_logger(fp:str, 
                     logger_name:str="default",
                     level:str="DEBUG",
                     date_format:str='%Y-%m-%d %H:%M:%S',
                     message_format:str='%(asctime)s :: %(levelname)s :: %(message)s'):
        '''
        Constructs basic_config, will not send logs to console, only
        to files. If both are needed, use default config and choose options
        
        params:
            fp: str, filepath to save
            level: str, defaults to DEBUG (shows all logs)
            date_format: str, format for date
            message_format: str, format of the logs.
        returns:
            LoggoBlocks object
        ''' 
        logging.basicConfig(filename=fp, 
                            filemode="a",
                            level=level,
                            format=message_format,
                            datefmt=date_format)
        return logging.getLogger(logger_name)

    
    @staticmethod
    def default_logger(handler_list:Handlers=[],
                       logger_name:str="default",
                       fp:str=None, 
                       date_format='%Y-%m-%d %H:%M:%S',
                       to_yaml_fp:str=None):
        '''
        Classmethod that builds a hardcoded dict_config as a starting point to change
        in the future. Choose options from the handler list to determine
        how logs will be handled, options in params.
            params:
                handler_list: str, options are:\n
                                - "console", will push every log to stdout\n
                                - "file", stores all logs produced by logger to single file.
                                    Cannot be used with rotating_file. MUST PASS fp ARGUMENT\n
                                - "rotating_file", stores logs into multiple files after they
                                    reach a certain number of bytes (1024 atm)\n
                                - "smtp", not yet implemented. MUST PASS fp ARGUMENT\n
                              example: ['console', 'file']
                logger_name: str, defaults as "default". This is the name that
                             logging will invoke when building a logger.
                fp: str, filepath to store logs if using "file" OR "rotating_file" handlers.
                date_format: str, date format in logs
                to_yaml_fp:str, will save configuration as a yaml. Do what you want with it from there.
        returns:
            LoggoBlocks object
        '''
   
        brief_format = '%(asctime)s :: %(levelname)s :: %(message)s'
        precise_format = '%(asctime)s :: %(levelname)s :: %(funcName)s :: %(message)s'
        
        dict_config = {"version":1, "disable_existing_loggers":False, 
                       "formatters":{}, "loggers":{}}
        
        dict_config['formatters']['brief'] = {"format":brief_format,"datefmt":date_format}
        dict_config['formatters']['precise'] = {"format":precise_format,"datefmt":date_format}

        dict_config['handlers'] = LoggoBlocks.__choose_handlers(handler_list, fp)

        dict_config['loggers'][logger_name] = {"level":"DEBUG", "handlers":handler_list}

        logging.config.dictConfig(dict_config)

        if to_yaml_fp:
            with open(to_yaml_fp, "w") as file:
                yaml.dump(dict_config, file)

        return logging.getLogger(logger_name)


    @staticmethod
    def __choose_handlers(handler_list:list, fp:str=None)->dict:
        '''
        console, file, rotating file, SMTP
        '''
        choices = {}
        for handler in handler_list:
            if handler == "console":
                choices['console'] = {"class":"logging.StreamHandler","formatter": "brief",
                                      "level": "DEBUG", "stream": "ext://sys.stdout"}
            elif handler == "file":
                if fp:
                    choices['file'] = {"class":"logging.FileHandler", "filename":fp, 
                                       "formatter":"precise", "level": "DEBUG"}
                else:
                    print("NEED FILE PATH TO MAKE FILE")
            elif handler == "rotating_file":
                if fp:
                    choices['rotating_file'] = {"class":"logging.handlers.RotatingFileHandler",
                                                "formatter":"precise", "filename":fp, "level":"DEBUG",
                                                "max_bytes": 1024, "max_count":7}
                else:
                    print("NEED FILE PATH TO MAKE FILEs")
            elif handler == "smtp":
                continue
            else:
                print(f"{handler} not in list of default options")
        return choices
      
    @staticmethod
    def config_to_yaml(fp:str, dict_config:dict)->None:
        '''
        Save self.config as a yaml file
        '''
        with open(fp, "w") as yaml_file:
            yaml.dump(dict_config, yaml_file)


    @staticmethod
    def construct_message_format(choice_list:Choices, joiner:str="  "):
        '''
        Gathers format specifiers for each name. Options are:
        asctime, filename, funcname (if applicable), levelname (debug, info etc), lineno (line number of logging call),
        message (logging message), name (logger name), pathname (filepath of logging call).
        params:
            choice_list: list, in desired order, choose formatter options. Example: ['asctime', 'filename', 'message']
            joiner: optional str, what divides each specifier, defaults as "  "
        returns:
            Str of format specifiers. 
        '''
        format_map = {"asctime":"%(asctime)s", "filename":"%(filename)s", "funcname":"%(funcName)s", 
                      "levelname":"%(levelname)s", "lineno": "%(lineno)d", "message":"%(message)s",
                      "name":"%(name)s", "pathname":"%(pathname)s"}
        return f"{joiner}".join([format_map[choice] for choice in choice_list])
    