# coding=utf-8

import calendar
import logging
import logging.config
from logging import Logger

import os
import time
from datetime import datetime

from ka_uts_com.ioc import Yaml
from ka_uts_com.ioc import Jinja2
from ka_uts_com.pacmod import Pacmod

from typing import Any, Callable, List, Dict

T_Arr = List[Any]
T_Dic = Dict[Any, Any]

TN_Arr = None | T_Arr
TN_Dic = None | T_Dic


class StandardLog:

    sw_init: bool = False
    cfg: T_Dic = {}
    log: Logger = logging.getLogger('dummy_logger')

    @staticmethod
    def read(pacmod: T_Dic, filename: str) -> Any:
        path: str = Pacmod.Path.Log.sh_cfg(filename=filename)
        tenant: str = pacmod['tenant']
        package: str = pacmod['package']
        module: str = pacmod['module']
        pid = Com.pid
        ts: None | datetime = Com.ts_start
        log_main = Jinja2.read(
            path, tenant=tenant, package=package, module=module,
            pid=pid, ts=ts)
        return log_main

    @classmethod
    def set_level(cls, sw_debug: bool) -> None:
        if sw_debug:
            level = logging.DEBUG
        else:
            level = logging.INFO
        cls.cfg['handlers']['main_debug_console']['level'] = level
        cls.cfg['handlers']['main_debug_file']['level'] = level

    @classmethod
    def init(
            cls, **kwargs) -> None:
        sw_debug: Any = kwargs.get('sw_debug')
        if cls.sw_init:
            return
        cls.sw_init = True
        cls.cfg = cls.read(Com.pacmod_curr, 'log.main.tenant.yml')
        cls.set_level(sw_debug)
        logging.config.dictConfig(cls.cfg)
        cls.log = logging.getLogger('main')
        return cls.log


class PersonLog:

    sw_init: bool = False
    cfg: T_Dic = {}
    log: Logger = logging.getLogger('dummy_logger')

    @classmethod
    def read(
            cls, pacmod: T_Dic, person: Any, filename: str) -> Any:
        path: str = Pacmod.Path.Log.sh_cfg(filename=filename)
        package: str = pacmod['package']
        module: str = pacmod['module']
        return Jinja2.read(
            path, package=package, module=module, person=person,
            pid=Com.pid, ts=Com.ts_start)

    @classmethod
    def set_level(cls, person: str, sw_debug: bool) -> None:
        if sw_debug:
            level = logging.DEBUG
        else:
            level = logging.INFO
        cls.cfg['handlers'][f'{person}_debug_console']['level'] = level
        cls.cfg['handlers'][f'{person}_debug_file']['level'] = level

    @classmethod
    def init(cls, pacmod: T_Dic, person: str, sw_debug: bool) -> None:
        cls.cfg = cls.read(pacmod, person, 'log.person.yml')
        cls.set_level(person, sw_debug)
        logging.config.dictConfig(cls.cfg)
        cls.log = logging.getLogger(person)
        return cls.log


class Cfg:

    @classmethod
    def init(cls, pacmod: T_Dic) -> TN_Dic:
        """ the package data directory has to contain a __init__.py
            file otherwise the objects notation {package}.data to
            locate the package data directory is invalid
        """
        _dic: TN_Dic = Yaml.read(Pacmod.Cfg.sh_path(pacmod))
        return _dic


class Mgo:

    client = None


class App:

    sw_init: bool = False
    httpmod = None
    sw_replace_keys: None | bool = None
    keys: TN_Arr = None
    reqs: T_Dic = {}
    app: T_Dic = {}

    @classmethod
    def init(
            cls, **kwargs) -> Any:
        if cls.sw_init:
            return cls
        cls.sw_init = True

        cls.httpmod = kwargs.get('httpmod')
        cls.sw_replace_keys = kwargs.get('sw_replace_keys', False)

        try:
            if cls.sw_replace_keys:
                pacmod = kwargs.get('pacmod_curr')
                cls.keys = Yaml.read(Pacmod.Pmd.sh_path_keys(pacmod))
        except Exception as e:
            if Com.Log is not None:
                fnc_error: Callable = Com.Log.error
                fnc_error(e, exc_info=True)
            raise
        return cls


class Exit:

    sw_critical: bool = False
    sw_stop: bool = False
    sw_interactive: bool = False


class Com:
    """Communication Class
    """

    sw_init: bool = False
    cfg: TN_Dic = None
    pid = None
    pacmod_curr: T_Dic = {}

    ts_start: None | datetime = None
    ts_end: None | datetime = None
    ts_etime: None | datetime = None
    d_timer: Dict = {}

    Log: Logger = logging.getLogger('dummy_logger')
    App = None
    Exit = Exit

    @classmethod
    def init(cls, **kwargs):
        """ set log and application (module) configuration
        """
        if cls.sw_init:
            return
        cls.sw_init = True

        cls.pacmod_curr = kwargs.get('pacmod_curr')
        cls.ts_start = calendar.timegm(time.gmtime())
        cls.pid = os.getpid()

        cls.cfg = Cfg.init(cls.pacmod_curr)
        cls.Log = StandardLog.init(**kwargs)
        cls.App = App.init(**kwargs)

    # @classmethod
    # def terminate(cls):
    #     """ set log and application (module) configuration
    #     """
    #     cls.Log = StandardLog.log
    #     cls.ts_end = calendar.timegm(time.gmtime())
    #     cls.ts_etime = cls.ts_end - cls.ts_start
