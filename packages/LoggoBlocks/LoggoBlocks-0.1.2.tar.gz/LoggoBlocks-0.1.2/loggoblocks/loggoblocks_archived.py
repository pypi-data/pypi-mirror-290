import logging
import logging.config
import yaml

class LoggoBlocks:
    '''
    Abstracts the configuration of logging, logger can be retrieved
    from self.logger after instantiation of LoggoBlocks.
    '''
    def __init__(self) -> None:
        self.logger_name = ""
        self.config = {}
    
    @classmethod
    def from_basic_config(cls, basic_config:dict, logger_name=None)->None:
        '''
        Creates basic logger from a basic_config, will not send logs to console, only
        to files. If both are needed, use either LoggoBlocks.from_dict_config() or 
        LoggoBlocks.construct_default_dict_config()\n
        params:
            basic_config: dict, precreated config to instantiate LoggoBlocks object.
                                keys used are name, level (DEBUG, normally), date_format and
                                message_format\n
            logger_name: optional str, overwrites basis_config name, otherwise
                         uses all other attributes from self.basic_config
        returns:
            LoggoBlocks object
        '''
        loggo = cls()
        if not logger_name:
            loggo.logger_name = basic_config['name']
        else:
            loggo.logger_name = logger_name
        loggo.config = basic_config
        logging.basicConfig(filename=loggo.basic_config["fp"], 
                            filemode="a",
                            level=loggo.config['level'],
                            format=loggo.config['message_format'],
                            datefmt=loggo.basic_config['datefmt'])
        return loggo
    
    
    @classmethod
    def from_dict_config(cls, dict_config:dict, logger_name:str=None):
        '''
        Creates a logger with much more fine-tuned configuration, allows for 
        additional features like SMTP handlers right out the gate, vs having 
        to logging.addHandlers with basic_configs
        
        params:
            dict_config: dict, a precreated config to instantiate LoggoBlocks object
            logger_name: optional str, overwrites dict_config name value
        returns:
            LoggoBlocks object
        '''
        loggo = cls()
        if not logger_name:
            loggo.logger_name = dict_config['name']
        else:
            loggo.logger_name = logger_name
        
        loggo.config = dict_config
        logging.config.dictConfig(loggo.config)
        return loggo

    
    @classmethod
    def construct_basic_config(cls, 
                               logger_name:str,
                               fp:str, 
                               level:str="DEBUG",
                               date_format:str='%Y-%m-%d %H:%M:%S',
                               message_format:str='%(asctime)s :: %(levelname)s :: %(message)s'):
        '''
        Constructs basic_config, will not send logs to console, only
        to files. If both are needed, use either LoggoBlocks.from_dict_config() or 
        LoggoBlocks.construct_default_dict_config()
        
        params:
            logger_name: str, name that logging will invoke
            fp: str, filepath to save
            level: str, defaults to DEBUG (shows all logs)
            date_format: str, format for date
            message_format: str, format of the logs.
        returns:
            LoggoBlocks object
        ''' 
        loggo = cls()
        loggo.logger_name = logger_name
        loggo.config = {"name":logger_name, 
                        "fp":fp,
                        "level":level, 
                        "datefmt":date_format,
                        "message_format":message_format}
        logging.basicConfig(filename=loggo.config["fp"], 
                            filemode="a",
                            level=loggo.config['level'],
                            format=loggo.config['message_format'],
                            datefmt=loggo.config['datefmt'])
        return loggo

    
    @classmethod
    def construct_default_dict_config(cls, handler_list:list=None,
                                      logger_name:str="default",
                                      fp:str=None, 
                                      date_format='%Y-%m-%d %H:%M:%S'):
        '''
        Classmethod that builds a hardcoded dict_config as a starting point to change
        in the future. Choose options from the handler list to determine
        how logs will be handled, options in params.
            params:
                handler_list: str, options are:\n
                                - "console", will push every log to stdout\n
                                - "file", stores all logs produced by logger to single file.
                                    Cannot be used with rotating_file.\n
                                - "rotating_file", stores logs into multiple files after they
                                    reach a certain number of bytes (1024 atm)\n
                                - "smtp", not yet implemented\n
                              example: ['console', 'file']
                logger_name: str, defaults as "default". This is the name that
                             logging will invoke when building a logger.
                fp: str, filepath to store logs if using "file" OR "rotating_file" handlers
                date_format: str, date format in logs
        returns:
            LoggoBlocks object
        '''
        loggo = cls()
        loggo.logger_name = logger_name
        brief_format = '%(asctime)s :: %(levelname)s :: %(message)s'
        precise_format = '%(asctime)s :: %(levelname)s :: %(funcName)s :: %(message)s'
        
        dict_config = {"version":1, "disable_existing_loggers":False, 
                       "formatters":{}, "loggers":{}}
        
        dict_config['formatters']['brief'] = {"format":brief_format,"datefmt":date_format}
        dict_config['formatters']['precise'] = {"format":precise_format,"datefmt":date_format}

        dict_config['handlers'] = loggo.__choose_handlers(handler_list, fp)

        dict_config['loggers'][loggo.logger_name] = {"level":"DEBUG", "handlers":handler_list}
        loggo.config = dict_config
        logging.config.dictConfig(loggo.config)

        return loggo

    
    def __choose_handlers(self, handler_list:list, fp:str=None)->dict:
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
    
    @property
    def logger(self):
        return logging.getLogger(self.logger_name)
    
    
    def config_to_yaml(self, fp:str)->None:
        '''
        Save self.config as a yaml file
        '''
        with open(fp, "w") as yaml_file:
            yaml.dump(self.config, yaml_file)

    def refresh_dict_config(self, dict_config:dict)->None:
        '''
        Refreshes logging configuration with new
        dict_config, if for some reason required
        mid runtime.
        '''
        logging.config.dictConfig(dict_config)

    def set_logger_name(self, logger_name:str)->None:
        '''
        Only useful if the dict_config that's used has multiple
        logger configurations. Otherwise, this will return
        the root configuration logger.
        '''
        self.logger_name = logger_name

    @staticmethod
    def construct_message_format(choice_list:list, joiner:str="  "):
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
    
    