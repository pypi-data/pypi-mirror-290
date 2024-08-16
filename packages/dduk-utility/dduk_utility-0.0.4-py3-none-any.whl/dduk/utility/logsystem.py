#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import logging
import os
import queue
from logging import Logger, handlers, Handler, StreamHandler, FileHandler, Formatter, LogRecord
from .ansicode import ANSICODE
from .strutility import GetTimestampString


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY : str = ""
NONE : str = "NONE"
COLON : str = ":"
SPACE : str = " "
SLASH : str = "/"
HYPHEN : str = "-"
COMMA : str = ","
UTF8 : str = "utf-8"



# #--------------------------------------------------------------------------------
# # 화면 출력 핸들러.
# #--------------------------------------------------------------------------------
# class PrintHandler(Handler):
# 	#--------------------------------------------------------------------------------
# 	# 호출됨.
# 	#--------------------------------------------------------------------------------
# 	def emit(self, record : LogRecord):
# 		message = self.format(record)
# 		# if record.levelno == FATAL or record.levelno == CRITICAL: Print(f"<bg_red><white><b>{message}</b></white></bg_red>")
# 		# elif record.levelno == ERROR: Print(f"<red>{message}</red>")
# 		# elif record.levelno == WARN or record.levelno == WARNING: Print(f"<yellow>{message}</yellow>")
# 		# elif record.levelno == INFO: Print(f"{message}")
# 		# elif record.levelno == DEBUG: Print(f"<magenta>{message}</magenta>")
# 		PrintLog(message, record.levelno)


#--------------------------------------------------------------------------------
# 로그 시스템 클래스.
#--------------------------------------------------------------------------------
class LOGSystem:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__ansicode : ANSICODE


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__ansicode = ANSICODE()


	#--------------------------------------------------------------------------------
	# 기록 시작.
	# - 로그 파일 사용 설정을 비활성화 하면 로그는 CLI상에서만 출력된다.
	#--------------------------------------------------------------------------------
	def Run(self, loggerName : str, logLevel : int, useLogFile : bool, logPath : str):

		# logLevel : int = logging.NOTSET
		timestamp : str = GetTimestampString(EMPTY, EMPTY, EMPTY, True, EMPTY)
		logFilePath : str = f"{logPath}/{loggerName}-{timestamp}.log"

		# # EXE 파일 실행.
		# if Application.IsBuild():
		# 	useLogFile = False
		# 	logLevel = logging.WARNING
		# # VSCode에서 디버깅 실행.
		# elif Application.IsDebug():
		# 	useLogFile = True
		# 	logLevel = logging.DEBUG
		# 	logFilePath = Application.GetRootPathWithRelativePath(f"logs/pyappcore-debug-{timestamp}.log")
		# # Blender.exe로 소스코드 실행.
		# elif Application.HasSymbol(SYMBOL_SERVICE):
		# 	useLogFile = True
		# 	logLevel = logging.INFO
		# 	logFilePath = Application.GetRootPathWithRelativePath(f"logs/pyappcore-service-{timestamp}.log")
		# # VSCode에서 디버깅 없이 실행.
		# else:
		# 	useLogFile = True
		# 	logLevel = logging.INFO
		# 	logFilePath = Application.GetRootPathWithRelativePath(f"logs/pyappcore-nodebug-{timestamp}.log")


		# 설정.
		logger : Logger = logging.getLogger(loggerName)
		logger.setLevel(logLevel)

		# 로깅 큐 추가.
		# 로그 파일 기록이 자꾸 씹히는 이슈 있어서 사용. (하지만 개선 효과 없음)
		logQueue = queue.Queue()
		ququeHandler = handlers.QueueHandler(logQueue)
		logger.addHandler(ququeHandler)

		# 로그 출력 양식 설정.
		# formatter : Formatter = Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")
		formatter : Formatter = Formatter("[%(asctime)s][%(levelname)s] %(message)s")

		# 프린트 핸들러.
		# printHandler : PrintHandler = PrintHandler()
		# printHandler.setLevel(logLevel)
		# printHandler.setFormatter(formatter)
		# applicationLogger.addHandler(printHandler)

		# 로그파일 설정.
		if useLogFile:
			if not os.path.isdir(logPath):
				os.makedirs(logPath)
			
			fileHandler : StreamHandler = FileHandler(logFilePath, encoding = UTF8)
			fileHandler.setLevel(logLevel)
			fileHandler.setFormatter(formatter)
			# applicationLogger.addHandler(fileHandler)
			# queueListener = handlers.QueueListener(logQueue, printHandler, fileHandler)

			# 큐 시작.
			queueListener = handlers.QueueListener(logQueue, fileHandler)
			queueListener.start()


	#--------------------------------------------------------------------------------
	# 로그 출력.
	#--------------------------------------------------------------------------------
	def PrintLog(self, text : str, logLevel : int) -> None:
		if logLevel == logging.FATAL or logLevel == logging.RITICAL: self.__ansicode.Print(f"<bg_red><white><b>{text}</b></white></bg_red>")
		elif logLevel == logging.ERROR: self.__ansicode.Print(f"<red>{text}</red>")
		elif logLevel == logging.WARN or logLevel == logging.WARNING: self.__ansicode.Print(f"<yellow>{text}</yellow>")
		elif logLevel == logging.INFO: self.__ansicode.Print(f"{text}")
		elif logLevel == logging.DEBUG: self.__ansicode.Print(f"<magenta>{text}</magenta>")
		else: self.__ansicode.Print(text)


	#--------------------------------------------------------------------------------
	# 로그 수준에 대한 문자열 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetStringFromLogLevel(logLevel : int) -> str:
		return logging.getLevelName(logLevel)