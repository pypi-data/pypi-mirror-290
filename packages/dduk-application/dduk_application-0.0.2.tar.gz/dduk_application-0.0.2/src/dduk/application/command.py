#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import sys
import os


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY : str = ""
NONE : str = "NONE"
COMMA : str = ","
SLASH : str = "/"
BACKSLASH : str = "\\"
COLON : str = ":"
SPACE : str = " "
DEBUG : str = "DEBUG"
READ : str = "r"
WRITE : str = "w"
UTF8 : str = "utf-8"


#--------------------------------------------------------------------------------
# 깃킵 파일 생성.
#--------------------------------------------------------------------------------
def CreateGitKeep(path : str) -> bool:
	try:
		if not path:
			return False

		path = path.replace(BACKSLASH, SLASH)
		if not os.path.isdir(path):
			return False
		
		gitkeepFilePath = f"{path}/.gitkeep"
		if os.path.isfile(gitkeepFilePath):
			return False

		with open(gitkeepFilePath, mode = WRITE, encoding = UTF8) as file:
			file.write(EMPTY)
		return True
	except Exception as exception:
		builtins.print(exception)
		return False




#--------------------------------------------------------------------------------
# 프로젝트 템플릿 생성.
#--------------------------------------------------------------------------------
def CreateProjectTemplate(rootPath : str) -> bool:
	if not rootPath:
		return False
	if not os.path.isdir(rootPath):
		return False


	# builtins.print(f"{rootPath}/.git")
	os.mkdir()
	os.mkdir(f"{rootPath}/.vscode")
	os.mkdir(f"{rootPath}/.vscode/launch.json")
	os.mkdir(f"{rootPath}/.vscode/settings.json")
	os.mkdir(f"{rootPath}/.vscode/tasks.json")
	# builtins.print(f"{rootPath}/.venv")
	os.mkdir(f"{rootPath}/build")
	os.mkdir(f"{rootPath}/docs")
	os.mkdir(f"{rootPath}/hints")
	os.mkdir(f"{rootPath}/hooks")
	os.mkdir(f"{rootPath}/libs")
	builtins.print(f"{rootPath}/logs")
	builtins.print(f"{rootPath}/res")
	builtins.print(f"{rootPath}/src")
	builtins.print(f"{rootPath}/tests")
	builtins.print(f"{rootPath}/workspace")
	builtins.print(f"{rootPath}/.gitignore")
	builtins.print(f"{rootPath}/requirements.txt")


#--------------------------------------------------------------------------------
# 명령어 스크립트 생성.
#--------------------------------------------------------------------------------
def CreateCommandScript(rootPath : str) -> None:
	builtins.print("dduk.application.command.CreateCommandScript()")


#--------------------------------------------------------------------------------
# 명령어 스크립트 제거.
#--------------------------------------------------------------------------------
def DestroyCommandScript(rootPath : str) -> None:
	builtins.print("dduk.application.command.DestroyCommandScript()")


#--------------------------------------------------------------------------------
# 실행 함수.
#--------------------------------------------------------------------------------
def Main() -> None:
	rootPath = os.getcwd()
	rootPath = rootPath.replace(BACKSLASH, SLASH)

	if sys.argv:
		command = sys.argv[0]
		command = command.lower()
		if command == "project":
			CreateProjectTemplate(rootPath)
		elif command == "bat":
			builtins.print(f"{rootPath}/build.bat")
			builtins.print(f"{rootPath}/environment.bat")
			builtins.print(f"{rootPath}/package.bat")
			builtins.print(f"{rootPath}/run.bat")
			builtins.print(f"{rootPath}/service.bat")
			builtins.print(f"{rootPath}/variable.bat")
			builtins.print(f"{rootPath}/venv.bat")
		elif command == "sh":
			builtins.print(f"{rootPath}/build.sh")
			builtins.print(f"{rootPath}/environment.sh")
			builtins.print(f"{rootPath}/package.sh")
			builtins.print(f"{rootPath}/run.sh")
			builtins.print(f"{rootPath}/service.sh")
			builtins.print(f"{rootPath}/variable.sh")
			builtins.print(f"{rootPath}/venv.sh")
		else:
			builtins.print(f"잘못된 명령어: {command}, 오류: 1")
	else:
		builtins.print("Usage: dduk-application \{project|bat|sh\}")
		builtins.print("dduk-application project: 현재 경로를 루트로 삼아 프로젝트 템플릿 생성.")
		builtins.print("dduk-application bat: 현재 경로를 루트로 삼아 프로젝트 배치파일 생성. (Windows)")
		builtins.print("dduk-application sh: 현재 경로를 루트로 삼아 프로젝트 쉘스크립트 생성. (Linux/MacOS)")