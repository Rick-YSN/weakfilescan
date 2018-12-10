# encoding: utf-8
# Fuzz URL列表 生成器
# email: ringzero@0x557.org

import sys
sys.path.append("../")
from config import *
from wyparser import DictParser
import urlparse
from UrlSplitParser import UrlSplitParser

class UrlGenerator(object):
	"""docstring for UrlGenerator"""
	def __init__(self, url, fuzz_bak, fuzz_tmp, extion=default_extion):
		super(UrlGenerator, self).__init__()
		self.url = url
		self.fuzz_bak = fuzz_bak
		self.fuzz_tmp = fuzz_tmp
		self.extion = extion
		self.fuzz_tmp_pre = 0 # 加入临时文件前缀

	def generator(self):
		# 整合其因变量(目录列表、文件名、域名、子域名)，拼接备份文件、临时文件
		parser_obj = UrlSplitParser(urlparse.urlparse(self.url),self.extion)
		# print parser_obj.get_paths()
		url_parser = parser_obj.get_paths()
		urls_result = []

		# 处理其因变量备份文件扩展
		depend_files = []
		for bak_line in self.fuzz_bak:
			for depend in parser_obj.dependent:
				depend_files.append(depend + bak_line)
		# print depend_files

		# 处理临时文件 pattern
		# @author: mads
		# @email: lxzmads@gmail.com
		# @update: 20181210
		script_files = []
		for tmp_line in self.fuzz_tmp:
			if url_parser['path']:
				for path_name in url_parser['path']:
					script_files.append(tmp_line.replace("%ORI%", path_name + '.' + parser_obj.file_ext))
			else:
				script_files.append(tmp_line.replace("%ORI%", 'index.' + parser_obj.file_ext))
		# print script_files
		# 经过正则引擎
		new_script_files = []
		for line_ in script_files:
			# 利用正则引擎遍历一次字典
			parser = DictParser(line_)
			wyparser_result = parser.parse()
			if wyparser_result:
				print wyparser_result
				for parser_line in wyparser_result:
					new_script_files.append(parser_line)
			else:
				new_script_files.append(line_)
		# 需要检测的目录
		for webdir in url_parser['segment']:
			# 拼接备份文件扫描完整URL
			for depend in depend_files:
				if webdir == '/':
					urls_result.append(parser_obj.baseurl + webdir + depend)
				else:
					urls_result.append(parser_obj.baseurl + webdir + '/' + depend)
			# 拼接临时文件扫描完整URL
			for script in new_script_files:
				if webdir == '/':
					urls_result.append(parser_obj.baseurl + webdir + script)
				else:
					urls_result.append(parser_obj.baseurl + webdir + '/' + script)
		return urls_result



