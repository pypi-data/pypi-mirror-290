import logging
import os
import types
import datetime
import inspect
from typing import Callable
from functools import wraps, update_wrapper, singledispatch
from .parameter_config import LogConfig

class LogManager:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(LogManager, cls).__new__(cls)
            cls._instance.config = LogConfig()
        return cls._instance
        
    def __init__(self):
        self.logger_dict={}

    def setup(self, root_log_path=None):
        assert self.check_root_log_path(root_log_path), f"Invalid Root Log Path Given: {root_log_path}"
        self.config.root_log_path = root_log_path
        self.create_cache_log()
        
    def check_root_log_path(self, root_log_path):
        if not root_log_path:
            return False
        try:
            os.makedirs(self.config.root_log_path, exist_ok=True)
        except Exception as e:
            print("Error during creating the folder.",e)
            return False
        return True
        
    def setup_check(func):
        def decorator(self, *args, **kwargs):
            print(self.config)
            if not hasattr(self, 'config') or not self.config.root_log_path:
                raise ValueError("Root log path must be set before using loggers.")
            return func(self, *args, **kwargs)
        return decorator
    
    @staticmethod
    def get_log_string(*args, **kwargs):
            modified_args = []
            for arg in args:
                if isinstance(arg, pd.DataFrame):
                    # Convert DataFrame to string with added lines
                    spliter="\n--------------------------------------\n"
                    df_str =  spliter + arg.to_string(max_rows=kwargs.get("max_rows", 10), max_cols=kwargs.get("max_cols", 10), max_colwidth=kwargs.get("max_colwidth", 35), show_dimensions=True) + spliter
                    modified_args.append(df_str)
                elif isinstance(arg, dict):
                    spliter="\n- - - - - - - - - - - - - - - - - - - \n"
                    rows = []
                    for k, v in arg.items():
                        rows.append({'key': k, 'value': v})

                    df_str = spliter + pd.DataFrame(rows).to_string(max_rows=kwargs.get("max_rows", 10), max_cols=kwargs.get("max_cols", 10), max_colwidth=kwargs.get("max_colwidth", 35), show_dimensions=True) + spliter
                    modified_args.append(df_str)
                elif isinstance(arg, float):
                    modified_args.append("{:.6f}".format(arg).rstrip('0'))
                else:
                    modified_args.append(str(arg))

            msg = ' '.join(modified_args)
            return msg

    def cache_log_cleaner(self, days=7):
        self.config.cache_log_path
        pass

    def create_cache_log(self):
        self.cache_log_cleaner()
        logger=self.create_logger("__cache", folderpath=self.config.cache_log_path)
        self.logger_dict["__cache"]=logger
        
    @setup_check
    def create_logger(self, logname, filename=None, folderpath=None, log_level=logging.DEBUG, timestamp=True):
        if not folderpath:
            folderpath = self.config.root_log_path
        if not filename:
            filename = logname
        else:
            filename = os.path.splitext(filename)[0]
        
        time_stamp=datetime.datetime.now().strftime("%y%m%d_%H%M%S")

        if timestamp:
            filename = f"{filename}_{time_stamp}.log"
        else:
            filename = f"{filename}.log"
        
        full_log_path = os.path.join(folderpath, filename)
        os.makedirs(folderpath, exist_ok=True)
        logger = logging.getLogger(logname)
        handler = logging.FileHandler(full_log_path)
        formatter = logging.Formatter('%(asctime)s-%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(log_level)

        def split_kwargs(**kwargs):
            log_kwargs = {key[5:]: value for key, value in kwargs.items() if key.startswith('_log_')}
            if "verbose" in kwargs:
                log_kwargs["verbose"]=kwargs["verbose"]
            other_kwargs = {key: value for key, value in kwargs.items() if not key.startswith('_log_') and key=="verbose"}
            return log_kwargs, other_kwargs
    
        def print_and_log(log_method):
            @wraps(log_method)
            def wrapper(*args, **kwargs):
                func_name = inspect.stack()[2].function
                log_kwargs, remaining_kwargs = split_kwargs(**kwargs)
                msg = LogManager.get_log_string(*args, **log_kwargs)
                log_method(msg, extra={'caller_func_name': func_name}, **remaining_kwargs)
                if log_kwargs.get("verbose", True):
                    print(msg)
                if log_kwargs.get("notify", False):
                    # Place holder for email notification/kafka message sending
                    pass 

            return wrapper

        logger.pinfo = print_and_log(logger.info)
        logger.pdebug = print_and_log(logger.debug)
        logger.pwarning = print_and_log(logger.warning)
        logger.perror = print_and_log(logger.error)
        logger.pcritical = print_and_log(logger.critical)
        
        self.logger_dict[logname] = logger
        return logger
    
    @setup_check
    def get_logger(self, logname, filename=None, folderpath=None, log_level=logging.DEBUG):
        if logname not in self.logger_dict:
            self.create_logger(logname, filename, folderpath, log_level)
        
        logger = self.logger_dict[logname]
        return logger
        
    @setup_check    
    def get_log(self, logname, filename=None, folderpath=None, log_level=logging.DEBUG):       
        logger = self.get_logger(logname, filename=filename, folderpath=folderpath, log_level=log_level)

        @singledispatch
        def decorator(obj):
            raise NotImplementedError("Unsupported type")

        @decorator.register
        def _(cls: type):  # Class decorator
            original_init = cls.__init__
            def wrapped_init(self, *args, **kwargs):
                original_init(self, *args, **kwargs)
                self.log = logger
            
            update_wrapper(wrapped_init, original_init)
            cls.__init__ = wrapped_init
            return cls

        @decorator.register(types.FunctionType)
        def _(func):  # Function decorator
            @wraps(func)
            def wrapper(*args, **kwargs):
                kwargs['log'] = logger
                logger.debug(f'Starting function {func.__name__}')
                result = func(*args, **kwargs)
                logger.debug(f'Function {func.__name__} ended.')
                return result
            return wrapper
        
        return decorator
    
    setup_check=staticmethod(setup_check)
