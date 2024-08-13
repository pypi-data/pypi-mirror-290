#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import os
from .pysongenerator import PYSONGenerator


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMBEDDEDDATANAME : str = "__embeddeddata__"
EMBEDDEDDATAFILENAME : str = f"{EMBEDDEDDATANAME}.py"
SLASH : str = "/"
COLON : str = "."
PYEXTENSION : str = ".py"
PACKAGE : str = "PACKAGE"
MODULE : str = "MODULE"
CLASS : str = "CLASS"
FUNCTION : str = "FUNCTION"
CARRIAGERETURN : str = "\r"
EMPTY : str = ""
LINEFEED : str = "\n"
READ : str = "r"
WRITE : str = "w"
UTF8 : str = "utf-8"
ASTERISK : str = "*"
DOUBLEQUOTATION : str = "\""
DEFAULT_REMOTEDEBUGPORT : int = 4885


#--------------------------------------------------------------------------------
# 내장 하려고 하는 데이터.
#--------------------------------------------------------------------------------
class EmbeddingData:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	RemoteDebugPort : int
	Symbols : set[str]


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.Symbols = set()
		self.RemoteDebugPort = DEFAULT_REMOTEDEBUGPORT


#--------------------------------------------------------------------------------
# 데이터 내장 처리기 클래스.
# - 데이터를 파이썬 코드로 변형해서 저장하므로 이후 추가 비용 없이 파일 이름만 알고 있으면 불러와 사용 가능.
# - 단, 이미 모듈이 리로드 되었다는 전제.
#--------------------------------------------------------------------------------
class Embedder:
	#--------------------------------------------------------------------------------
	# 데이터를 코드로 만들어 저장.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Embed(sourcePath : str, embeddingData : EmbeddingData) -> None:

		# 파일 경로 생성.
		embeddedDataFilePath : str = f"{sourcePath}/{EMBEDDEDDATAFILENAME}"

		# 기존 파일 제거.
		if os.path.exists(embeddedDataFilePath):
			os.remove(embeddedDataFilePath)

		# 코드 생성.
		pysonGenerator = PYSONGenerator()
		content = pysonGenerator.Generate("EMBEDDEDDATA", embeddingData)

		# 파일 기록.
		with open(embeddedDataFilePath, WRITE, encoding = UTF8) as file:
			file.write(content)