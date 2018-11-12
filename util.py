#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import openpyxl

#extra
import xlrd
import datetime


#needs to install Gnumeric spreadsheet program to convert the files

def xlsx_to_csv(target_home):

	mutants_list = []

	for file in os.listdir(target_home):

		#read only xlsx files, ignore other files
		if ".xlsx" not in file and 'xls' not in file:
			continue

		if 'xlsx' in file:
			new_file = file[:-5] + '.csv'
		else:
			new_file = file[:-4] + '.csv' 
		
		#print statment
		statment = 'ssconvert {} {}'.format(file,new_file)
		os.system(statment)


"""
	Convert xls files to xlsx files. Credits -> https://stackoverflow.com/questions/9918646/how-to-convert-xls-to-xlsx
"""
def xls_to_xlsx(*args, **kw):
	"""
	open and convert an XLS file to openpyxl.workbook.Workbook
	----------
	@param args: args for xlrd.open_workbook
	@param kw: kwargs for xlrd.open_workbook
	@return: openpyxl.workbook.Workbook
	"""
	
	book_xls = xlrd.open_workbook(*args, formatting_info=True, ragged_rows=True, **kw)
	book_xlsx = openpyxl.workbook.Workbook()

	sheet_names = book_xls.sheet_names()
	for sheet_index in range(len(sheet_names)):
		sheet_xls = book_xls.sheet_by_name(sheet_names[sheet_index])
		if sheet_index == 0:
			sheet_xlsx = book_xlsx.active
			sheet_xlsx.title = sheet_names[sheet_index]
		else:
			sheet_xlsx = book_xlsx.create_sheet(title=sheet_names[sheet_index])
		for crange in sheet_xls.merged_cells:
			rlo, rhi, clo, chi = crange
			sheet_xlsx.merge_cells(start_row=rlo + 1, end_row=rhi,
			start_column=clo + 1, end_column=chi,)

		def _get_xlrd_cell_value(cell):
			value = cell.value
			if cell.ctype == xlrd.XL_CELL_DATE:
				datetime_tup = xlrd.xldate_as_tuple(value,0)	
				if datetime_tup[0:3] == (0, 0, 0):   # time format without date
					value = datetime.time(*datetime_tup[3:])
				else:
					value = datetime.datetime(*datetime_tup)
			return value

		for row in range(sheet_xls.nrows):
			sheet_xlsx.append((
				_get_xlrd_cell_value(cell)
				for cell in sheet_xls.row_slice(row, end_colx=sheet_xls.row_len(row))
			))
	
	filename = str(*args)
	filename = filename.replace('xls', 'xlsx')
	book_xlsx.save(filename)