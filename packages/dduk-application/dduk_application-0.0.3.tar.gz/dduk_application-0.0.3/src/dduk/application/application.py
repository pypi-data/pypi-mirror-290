#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import logging
import sys
import traceback
from dduk.utility.logsystem import LOGSystem
from .data import Data


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY : str = ""
NONE : str = "NONE"
HYPHEN : str = "-"
COMMA : str = ","
SLASH : str = "/"
BACKSLASH : str = "\\"
COLON : str = ":"
SPACE : str = " "
DEBUG : str = "DEBUG"
SYMBOL_SERVICE : str = "SERVICE" # "PYAPPCORE_SYMBOL_SERVICE"
SYMBOL_SUBPROCESS : str = "SUBPROCESS" # "PYAPPCORE_SYMBOL_SUBPROCESS"
SYMBOL_LOG : str = "LOG" # "PYAPPCORE_SYMBOL_LOG"
SYMBOL_DEBUG : str = "DEBUG" # "PYAPPCORE_SYMBOL_DEBUG"
NODEBUG : str = "NODEBUG" # "PYAPPCORE_SYMBOL_NODEBUG"
LOG_CRITICAL : int  = 50
LOG_ERROR : int = 40
LOG_EXCEPTION : int  = 40
LOG_WARNING : int  = 30
LOG_INFO : int = 20
LOG_DEBUG : int  = 10
LOG_NOTSET : int = 0


#--------------------------------------------------------------------------------
# 애플리케이션 클래스.
#--------------------------------------------------------------------------------
class Application:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__data : Data
	__log : LOGSystem


	#--------------------------------------------------------------------------------
	# 데이터 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Data(self) -> Data:
		return self.__data
	

	#--------------------------------------------------------------------------------
	# 로그 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Log(self) -> LOGSystem:
		return self.log
	

	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__data = Data()
		self.__log = LOGSystem()


	#--------------------------------------------------------------------------------
	# 빌드된 상태인지 여부.
	#--------------------------------------------------------------------------------
	def IsBuild(self) -> bool:
		return self.__data.IsBuild()


	#--------------------------------------------------------------------------------
	# 실제 로그 출력.
	#--------------------------------------------------------------------------------
	def __Log(self, message : str, logLevel : int) -> None:

		# 일단 콘솔에 출력.
		timestamp = GetTimestampString(HYPHEN, SPACE, COLON, True, COMMA)
		logName = GetStringFromLogLevel(logLevel)
		# builtins.print(f"[{timestamp}][{logName}] {message}")
		self.__log.PrintLog(f"[{timestamp}][{logName}] {message}", logLevel)

		# 로그파일 기록시.
		if Application.HasSymbol(SYMBOL_LOG):
			applicationLogger = Application.GetLogger()
			if logLevel == LOG_NOTSET: # logging.NOTSET:
				return
			elif logLevel == LOG_DEBUG: # logging.DEBUG:
				applicationLogger.debug(message)
			elif logLevel == LOG_INFO: # logging.INFO:
				applicationLogger.info(message)
			elif logLevel == LOG_WARNING: # logging.WARN or logging.WARNING:
				applicationLogger.warning(message)
			elif logLevel == LOG_ERROR: # logging.ERROR:
				applicationLogger.error(message)
			elif logLevel == LOG_CRITICAL: # logging.FATAL or logging.CRITICAL:
				applicationLogger.critical(message)


	#--------------------------------------------------------------------------------
	# 로그 디버그 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LogDebug(message : str) -> None:
		Application._Application__Log(message, LOG_DEBUG)


	#--------------------------------------------------------------------------------
	# 로그 인포 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Log(message : str) -> None:
		Application._Application__Log(message, LOG_INFO)


	#--------------------------------------------------------------------------------
	# 로그 인포 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LogInfo(message : str) -> None:
		Application._Application__Log(message, LOG_INFO)


	#--------------------------------------------------------------------------------
	# 로그 워닝 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LogWarning(message : str) -> None:
		Application._Application__Log(message, LOG_WARNING)


	#--------------------------------------------------------------------------------
	# 로그 에러 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LogError(message : str) -> None:
		Application._Application__Log(message, LOG_ERROR)


	#--------------------------------------------------------------------------------
	# 로그 익셉션 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LogException(exception : Exception, useTraceback : bool = True, useExit : bool = True) -> None:
		if useTraceback:
			traceback.print_exc()
			tb = exception.__traceback__
			while tb:
				filename = tb.tb_frame.f_code.co_filename
				lineno = tb.tb_lineno
				funcname = tb.tb_frame.f_code.co_name
				result = traceback.format_exc()
				result = result.strip()
				line = result.splitlines()[-1]
				Application._Application__Log(f"Exception in {filename}, line {lineno}, in {funcname}", LOG_EXCEPTION)
				Application._Application__Log(f"\t{line}", LOG_EXCEPTION)
				tb = tb.tb_next
		else:
			Application._Application__Log(exception, LOG_EXCEPTION)

		if useExit:
			sys.exit(1)
	
	#--------------------------------------------------------------------------------
	# 로그 크리티컬 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LogCritical(message : str) -> None:
		Application._Application__Log(message, LOG_CRITICAL)
	

	#--------------------------------------------------------------------------------
	# 디버깅 상태인지 여부.
	#--------------------------------------------------------------------------------
	def IsDebug(self) -> bool:
		return self.__data.IsDebug()


	#--------------------------------------------------------------------------------
	# 실행된 파일 이름 반환.
	#--------------------------------------------------------------------------------
	def GetExecuteFileName(self) -> str:
		return self.__data.GetExecuteFileName()


	#--------------------------------------------------------------------------------
	# 애플리케이션이 존재하는 경로 / 실행파일이 존재하는 경로.
	#--------------------------------------------------------------------------------
	def GetRootPath(self) -> str:
		return self.__data.GetRootPath()


	#--------------------------------------------------------------------------------
	# 소스 경로 / 실행 파일 실행시 임시 소스 폴더 경로.
	#--------------------------------------------------------------------------------
	def GetSourcePath(self) -> str:
		return self.__data.GetSourcePath()
	

	#--------------------------------------------------------------------------------
	# 리소스 경로 / 실행 파일 실행시 임시 리소스 폴더 경로.
	#--------------------------------------------------------------------------------
	def GetResourcePath(self) -> str:
		return self.__data.GetResourcePath()


	#--------------------------------------------------------------------------------
	# 워크스페이스 폴더 경로.
	#--------------------------------------------------------------------------------
	def GetWorkspacePath(self) -> str:
		return self.__data.GetWorkspacePath()
	

	#--------------------------------------------------------------------------------
	# 애플리케이션이 존재하는 경로에 상대경로를 입력하여 절대경로를 획득.
	#--------------------------------------------------------------------------------
	def GetRootPathWithRelativePath(self, relativePath : str) -> str:
		rootPath = self.__data.GetRootPath()
		if not relativePath:
			return rootPath
		relativePath = relativePath.replace(BACKSLASH, SLASH)
		absolutePath = f"{rootPath}/{relativePath}"
		return self.__data


	#--------------------------------------------------------------------------------
	# 소스가 존재하는 경로에 상대경로를 입력하여 절대경로를 획득.
	#--------------------------------------------------------------------------------
	def GetSourcePathWithRelativePath(self, relativePath : str) -> str:
		sourcePath = self.__data.GetSourcePath()
		if not relativePath:
			return sourcePath
		relativePath = relativePath.replace(BACKSLASH, SLASH)
		absolutePath = f"{sourcePath}/{relativePath}"
		return absolutePath
	

	#--------------------------------------------------------------------------------
	# 리소스가 존재하는 경로에 상대경로를 입력하여 절대경로를 획득.
	#--------------------------------------------------------------------------------
	def GetResourcePathWithRelativePath(self, relativePath : str) -> str:
		resourcePath = self.__data.GetResourcePath()
		if not relativePath:
			return resourcePath
		relativePath = relativePath.replace(BACKSLASH, SLASH)
		absolutePath = f"{resourcePath}/{relativePath}"
		return absolutePath
	
	#--------------------------------------------------------------------------------
	# 워크스페이스 경로에 상대경로를 입력하여 절대경로를 획득.
	# - 워크스페이스 경로.
	# - 프로젝트 일 때 : src와 동일 계층의 workspace 이다.
	# - 실행파일 일 때 : 실행파일과 동일 폴더이다.
	#--------------------------------------------------------------------------------
	def GetWorkspacePathWithRelativePath(self, relativePath : str) -> str:
		workspacePath = self.__data.GetWorkspacePath()
		if not relativePath:
			return workspacePath
		relativePath = relativePath.replace(BACKSLASH, SLASH)
		absolutePath = f"{workspacePath}/{relativePath}"

		return absolutePath
	

	#--------------------------------------------------------------------------------
	# 심볼 목록 반환.
	#--------------------------------------------------------------------------------
	def GetSymbols(self) -> list[str]:
		return self.GetSymbols()
	

	#--------------------------------------------------------------------------------
	# 심볼을 가지고 있는지 여부 반환.
	#--------------------------------------------------------------------------------
	def HasSymbol(self, symbolString) -> bool:		
		return self.HasSymbol(symbolString)