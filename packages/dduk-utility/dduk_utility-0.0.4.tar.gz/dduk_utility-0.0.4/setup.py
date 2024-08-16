#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
import builtins
import os
import setuptools


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
UTF8 : str = "utf-8"
READ : str = "r"


#--------------------------------------------------------------------------------
# 참조 메타 데이터 목록.
#--------------------------------------------------------------------------------
NAME : str = "dduk-utility"
VERSION : str = "v0.0.4"
AUTHOR : str = "ddukbaek2"
AUTHOR_EMAIL : str = "ddukbaek2@gmail.com"
DESCRIPTION : str = "ddukbaek2 utility library"
LONG_DESCRIPTION_CONTENT_TYPE : str = "text/markdown"
URL : str = "https://ddukbaek2.com"
PYTHON_REQUIRES : str = ">=3.9"
LONGDESCRIPTION : str = str()
with open(file = "README.md", mode = READ, encoding = UTF8) as file: LONGDESCRIPTION = file.read()


#--------------------------------------------------------------------------------
# 빌드.
#--------------------------------------------------------------------------------
setuptools.setup(
	name = NAME,
	version = VERSION,
	author = AUTHOR,
	author_email = AUTHOR_EMAIL,
	description = DESCRIPTION,
	long_description = LONGDESCRIPTION,
	long_description_content_type = LONG_DESCRIPTION_CONTENT_TYPE,
	url = URL,
	packages = setuptools.find_packages(where = "src"),
	include_package_data = True,
	package_dir = { "": "src" },
	package_data = {
		"": [
			"res/*"
		],
	},
	scripts = [

	],
	entry_points = {
		"console_scripts": [
			# "dduk-utility=dduk.utility.commands:Command"
		]
	},
	install_requires = [
		"dduk-core"
	],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	python_requires = PYTHON_REQUIRES
)