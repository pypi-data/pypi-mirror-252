import tempfile
from pathlib import Path
import shutil
from copy import deepcopy
import json,os,base64,time
from datetime import datetime
from sqlalchemy.ext.automap import automap_base
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import zipfile
from colored import Fore,Back,Style
BASE=declarative_base()

class Entry(BASE):
	__tablename__="Entry"
	Code=Column(String)
	Barcode=Column(String)
	#not found in prompt requested by
	'''
	#name {Entryid}
	#name {Entryid} {new_value}
	
	#price {Entryid}
	#price {Entryid} {new_value}

	#note {Entryid}
	#note {Entryid} {new_value}
	
	#size {Entryid} 
	#size {Entryid} {new_value}
	'''
	Name=Column(String)
	Price=Column(Float)
	Note=Column(String)
	Size=Column(String)
	
	CaseCount=Column(Integer)

	Shelf=Column(Integer)
	BackRoom=Column(Integer)
	Display_1=Column(Integer)
	Display_2=Column(Integer)
	Display_3=Column(Integer)
	Display_4=Column(Integer)
	Display_5=Column(Integer)
	Display_6=Column(Integer)
	InList=Column(Boolean)
	Stock_Total=Column(Integer)
	Location=Column(String)
	ListQty=Column(Float)
	upce2upca=Column(String)

	EntryId=Column(Integer,primary_key=True)
	Timestamp=Column(Float)
	def __init__(self,Barcode,Code,upce2upca='',Name='',InList=False,Price=0.0,Note='',Size='',CaseCount=0,Shelf=0,BackRoom=0,Display_1=0,Display_2=0,Display_3=0,Display_4=0,Display_5=0,Display_6=0,Stock_Total=0,Timestamp=datetime.now().timestamp(),EntryId=None,Location='///',ListQty=0.0):
		if EntryId:
			self.EntryId=EntryId
		self.Barcode=Barcode
		self.Code=Code
		self.Name=Name
		self.Price=Price
		self.Note=Note
		self.Size=Size
		self.Shelf=Shelf
		self.CaseCount=CaseCount
		self.BackRoom=BackRoom
		self.Display_1=Display_1
		self.Display_2=Display_2
		self.Display_3=Display_3
		self.Display_4=Display_4
		self.Display_5=Display_5
		self.Display_6=Display_6
		self.Stock_Total=Stock_Total
		self.Location=Location
		self.Timestamp=Timestamp
		self.InList=InList
		self.ListQty=ListQty
		self.upce2upca=upce2upca

	def __repr__(self):
		return f"""{Style.bold}{Style.underline}{Fore.pale_green_1b}Entry{Style.reset}(
		{Fore.hot_pink_2}{Style.bold}{Style.underline}EntryId{Style.reset}={self.EntryId}
		{Fore.violet}{Style.underline}Code{Style.reset}='{self.Code}',
		{Fore.orange_3}{Style.bold}Barcode{Style.reset}='{self.Barcode}',
		{Fore.orange_3}{Style.underline}UPCE from UPCA[if any]{Style.reset}='{self.upce2upca}',
		{Fore.green}{Style.bold}Price{Style.reset}=${self.Price},
		{Fore.red}Name{Style.reset}='{self.Name}',
		{Fore.tan}Note{Style.reset}='{self.Note}',
		{Fore.pale_green_1b}Timestamp{Style.reset}='{datetime.fromtimestamp(self.Timestamp).strftime('%D@%H:%M:%S')}',
		{Fore.deep_pink_3b}Shelf{Style.reset}={self.Shelf},
		{Fore.light_steel_blue}BackRoom{Style.reset}={self.BackRoom},
		{Fore.cyan}Display_1{Style.reset}={self.Display_1},
		{Fore.cyan}Display_2{Style.reset}={self.Display_2},
		{Fore.cyan}Display_3{Style.reset}={self.Display_3},
		{Fore.cyan}Display_4{Style.reset}={self.Display_4},
		{Fore.cyan}Display_5{Style.reset}={self.Display_5},
		{Fore.cyan}Display_6{Style.reset}={self.Display_6},
		{Fore.light_salmon_3a}Stock_Total{Style.reset}={self.Stock_Total},
		{Fore.magenta_3c}InList{Style.reset}={self.InList}
		{Fore.yellow}ListQty{Style.reset}={self.ListQty}
		{Fore.misty_rose_3}Location{Style.reset}={self.Location}
		{Fore.sky_blue_2}CaseCount{Style.reset}={self.CaseCount}
		{Fore.sky_blue_2}Size{Style.reset}={self.Size}
		)
		"""

class ExtractPkg:
	def __str__(self):
		return "ExtractPkg and Update Config"

	def __init__(self,tbl,error_log,engine):
		self.tbl=tbl
		self.error_log=error_log
		self.engine=engine

		while True:
			try:
				path2bck=input("MobileInventoryCLI-BCK Path[filepath+filename/q/b]: ")
				if path2bck in ['q','quit']:
					exit("user quit!")
				elif path2bck in ['b','back']:
					return
				else:
					path2bck=Path(path2bck)
					if path2bck.exists():
						with zipfile.ZipFile(path2bck,"r") as zip:
							#tmpdir=Path(tempfile.mkdtemp())
							for file in zip.namelist():
								if Path(file).suffix == ".db3":
									x=zip.extract(file,path=str(Path("./system.db").absolute()))
									print(x)
									#update db
									print("opening db for updates")
									with Session(engine) as session:
										while True:
											clear_db=input("Clear DB before adding from file[Y/n/q/b]: ")
											if clear_db.lower() in ['y','yes','ye']:
												session.query(Entry).delete()
												session.commit()
												break
											elif clear_db.lower() in ['q','quit','qui','qu','exit']:
												exit("user quit!")
												break
											elif clear_db.lower() in ['b','ba','bac','back']:
												return
											else:
												break

										l_base=automap_base()
										f=f'sqlite:///{Path(x).absolute()}'
										print(f)
										l_engine=create_engine(f)
										l_base.prepare(autoload_with=l_engine)
										ltbl=l_base.classes

										with Session(l_engine) as ses:
											results=ses.query(ltbl.Item).all()
											print(dir(ltbl))
											for num,item in enumerate(results):
												entry=Entry(Name=item.Name,Barcode=item.Barcode,Code=item.Code,Price=item.Price)
												session.add(entry)
												if num % 100 == 0:
													session.commit()
												print(f'{num+1}/{len(results)}')
											session.commit()
									print("done importing")
								else:
									zip.extract(file,path=str(Path("./system.db").absolute()))
								print("Extracting {s1}{v}{e} to {s2}{vv}{e}".format(v=file,vv=str(Path("./system.db").absolute()),e=Style.reset,s1=Fore.light_green,s2=Fore.red))
			except Exception as e:
				print(e)