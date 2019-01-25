#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import openpyxl

#extra
import xlrd
import datetime


#needs to install Gnumeric spreadsheet program to convert the files
def xlsx_to_csv(target_dir):

	for file in os.listdir(target_dir):

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


"""
	Some projects have duplicated files, so designite create double entries (duplicated lines) when calculate/export smells to csv.
	Create this rotine to remove the duplicated lines in every csv file.
	https://stackoverflow.com/questions/15741564/removing-duplicate-rows-from-a-csv-file-using-a-python-script  
"""
def remove_duplicated_lines(afile):

	#create a result dir to storage the new files
	result_dir = os.getcwd() + '/new_csv/'
	
	#simple dir check
	try:
        #verifies if its a valid dir	
		os.stat(result_dir)
	except:
        #since the dir doesn't exist, create it!
		os.mkdir(result_dir)
	
	#result file will have the same name
	new_file = result_dir + afile

	#routine
	with open(afile,'r') as in_file, open(new_file,'w') as out_file:
		seen = set() # set for fast O(1) amortized lookup
		for line in in_file:
			if line in seen: continue # skip duplicate

			seen.add(line)
			out_file.write(line)

#used to format some data before run the other scripts
if __name__ == "__main__":

	#this solution relies on python 2.X

	#configurations
	target_dir = 'specify/the/target/dir'
	os.chdir(target_dir)

	#possible methods
	print "1 - Remove duplicates from CSV"
	print "2 - Convert XLSX -> CSV"
	print "3 - Convert XLS  -> XLSX"

	#read the option
	switch = int(raw_input("Chose an method: "))

	#execute according to the option
	if switch not in [1,2,3]:
		print "W: Invalid option!"

	if switch == 1:

		#run for each file from the dir
		for root, dirs, files in os.walk(".", topdown=False):
			for file_name in files:

				#avoid other files				
				if ".csv" not in file_name:
					continue

				#execute on csv
				remove_duplicated_lines(file_name)


	if switch == 2:

		#simple do the conversion for all files in the dir (gnumeric tool required)
		xlsx_to_csv(target_dir)

	if switch == 3:

		#read of files from dir
		for root, dirs, files in os.walk(".", topdown=False):
			for file_name in files:				
				
				#avoid non xls files
				if ".xls" not in file_name:
					continue
				
				#do the conversion 
				xls_to_xlsx(file_name)