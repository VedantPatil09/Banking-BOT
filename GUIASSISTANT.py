#########################
# GLOBAL VARIABLES USED #
#########################
ai_name ='S.A.M.'.lower()
EXIT_COMMANDS = ['bye','exit','quit','shut down', 'shutdown']

ownerName = "BankBot"
ownerDesignation = "Sir"
ownerPhoto = "1"
rec_email, rec_phoneno = "", ""
WAEMEntry = None

avatarChoosen = 0
choosedAvtrImage = None

botChatTextBg = "#007cc7"
botChatText = "white"
userChatTextBg = "#4da8da"


# chatBgColor = '#12232e'
chatBgColor = '#778899'
background = '#203647'

textColor = 'white'
AITaskStatusLblBG = '#203647'
# AITaskStatusLblBG = 'white'
KCS_IMG = 1 #0 for light, 1 for dark
voice_id = 0 #0 for female, 1 for male
ass_volume = 1 #max volume
ass_voiceRate = 200 #normal voice rate

####################################### IMPORTING MODULES ###########################################
""" User Created Modules """
try:
	import normalChat
	import appControl
	from userHandler import UserData
	import webScrapping
except Exception as e:
	raise e

""" System Modules """
try:
	import os
	import speech_recognition as sr
	import pyttsx3
	from tkinter import *
	from tkinter import ttk
	from tkinter import messagebox
	from tkinter import colorchooser
	from PIL import Image, ImageTk
	from time import sleep
	from threading import Thread
except Exception as e:
	print(e)

if os.path.exists('userData')==False:
	os.mkdir('userData')

########################################## BOOT UP WINDOW ###########################################
def ChangeSettings(write=False):
	import pickle
	global background, textColor, chatBgColor, voice_id, ass_volume, ass_voiceRate, AITaskStatusLblBG, KCS_IMG, botChatTextBg, botChatText, userChatTextBg
	setting = {'background': background,
				'textColor': textColor,
				'chatBgColor': chatBgColor,
				'AITaskStatusLblBG': AITaskStatusLblBG,
				'KCS_IMG': KCS_IMG,
				'botChatText': botChatText,
				'botChatTextBg': botChatTextBg,
				'userChatTextBg': userChatTextBg,
				'voice_id': voice_id,
				'ass_volume': ass_volume,
				'ass_voiceRate': ass_voiceRate
			}
	if write:
		with open('userData/settings.pck', 'wb') as file:
			pickle.dump(setting, file)
		return
	try:
		with open('userData/settings.pck', 'rb') as file:
			loadSettings = pickle.load(file)
			background = loadSettings['background']
			textColor = loadSettings['textColor']
			chatBgColor = loadSettings['chatBgColor']
			AITaskStatusLblBG = loadSettings['AITaskStatusLblBG']
			KCS_IMG = loadSettings['KCS_IMG']
			botChatText = loadSettings['botChatText']
			botChatTextBg = loadSettings['botChatTextBg']
			userChatTextBg = loadSettings['userChatTextBg']
			voice_id = loadSettings['voice_id']
			ass_volume = loadSettings['ass_volume']
			ass_voiceRate = loadSettings['ass_voiceRate']
	except Exception as e:
		pass

if os.path.exists('userData/settings.pck')==False:
	ChangeSettings(True)
	
def getChatColor():
	global chatBgColor
	chatBgColor = myColor[1]
	colorbar['bg'] = chatBgColor
	chat_frame['bg'] = chatBgColor
	root1['bg'] = chatBgColor

def changeTheme():
	global background, textColor, AITaskStatusLblBG, KCS_IMG, botChatText, botChatTextBg, userChatTextBg, chatBgColor
	if themeValue.get()==1:
		background, textColor, AITaskStatusLblBG, KCS_IMG = "#203647", "white", "#203647",1
		cbl['image'] = cblDarkImg
		kbBtn['image'] = kbphDark
		settingBtn['image'] = sphDark
		AITaskStatusLbl['bg'] = AITaskStatusLblBG
		botChatText, botChatTextBg, userChatTextBg = "white", "#007cc7", "#4da8da"
		# chatBgColor = "#12232e"
		chatBgColor = "#778899"
		colorbar['bg'] = chatBgColor
	else:
		background, textColor, AITaskStatusLblBG, KCS_IMG = "#F6FAFB", "#303E54", "#14A769", 0
		cbl['image'] = cblLightImg
		kbBtn['image'] = kbphLight
		settingBtn['image'] = sphLight
		AITaskStatusLbl['bg'] = AITaskStatusLblBG
		botChatText, botChatTextBg, userChatTextBg = "#494949", "#EAEAEA", "#23AE79"
		chatBgColor = "#F6FAFB"
		colorbar['bg'] = '#E8EBEF'

	root['bg'], root2['bg'] = background, background
	settingsFrame['bg'] = background
	settingsLbl['fg'], userPhoto['fg'], userName['fg'], assLbl['fg'], voiceRateLbl['fg'], volumeLbl['fg'], themeLbl['fg'], chooseChatLbl['fg'] = textColor, textColor, textColor, textColor, textColor, textColor, textColor, textColor
	settingsLbl['bg'], userPhoto['bg'], userName['bg'], assLbl['bg'], voiceRateLbl['bg'], volumeLbl['bg'], themeLbl['bg'], chooseChatLbl['bg'] = background, background, background, background, background, background, background, background
	s.configure('Wild.TRadiobutton', background=background, foreground=textColor)
	volumeBar['bg'], volumeBar['fg'], volumeBar['highlightbackground'] = background, textColor, background
	chat_frame['bg'], root1['bg'] = chatBgColor, chatBgColor
	userPhoto['activebackground'] = background
	ChangeSettings(True)

def changeVoice(e):
	global voice_id
	voice_id=0
	if assVoiceOption.get()=='Male': voice_id=1
	engine.setProperty('voice', voices[voice_id].id)
	ChangeSettings(True)

def changeVolume(e):
	global ass_volume
	ass_volume = volumeBar.get() / 100
	engine.setProperty('volume', ass_volume)
	ChangeSettings(True)

def changeVoiceRate(e):
	global ass_voiceRate
	temp = voiceOption.get()
	if temp=='Very Low': ass_voiceRate = 100
	elif temp=='Low': ass_voiceRate = 150
	elif temp=='Fast': ass_voiceRate = 250
	elif temp=='Very Fast': ass_voiceRate = 300
	else: ass_voiceRate = 200
	print(ass_voiceRate)
	engine.setProperty('rate', ass_voiceRate)
	ChangeSettings(True)

ChangeSettings()

############################################ SET UP VOICE ###########################################
try:
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[voice_id].id) #male
	engine.setProperty('volume', ass_volume)
except Exception as e:
	print(e)


####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
	AITaskStatusLbl['text'] = 'Speaking...'
	if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)
	if display: attachTOframe(text, True)
	print('\n'+ai_name.upper()+': '+text)
	try:
		engine.say(text)
		engine.runAndWait()
	except:
		print("Try not to type more...")

####################################### SET UP SPEECH TO TEXT #######################################
def record(clearChat=True, iconDisplay=True):
	print('\nListening...')
	AITaskStatusLbl['text'] = 'Listening...'
	r = sr.Recognizer()
	r.dynamic_energy_threshold = False
	r.energy_threshold = 4000
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
		said = ""
		try:
			AITaskStatusLbl['text'] = 'Processing...'
			said = r.recognize_google(audio)
			print(f"\nUser said: {said}")
			if clearChat:
				clearChatScreen()
			if iconDisplay: Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			attachTOframe(said)
		except Exception as e:
			print(e)
			# speak("I didn't get it, Say that again please...")
			if "connection failed" in str(e):
				speak("Your System is Offline...", True, True)
			return 'None'
	return said.lower()

def voiceMedium():
	while True:
		query = record()
		if query == 'None': continue
		if isContain(query, EXIT_COMMANDS):
			speak("Shutting down the System. Good Bye "+ownerDesignation+"!", True, True)
			break
		else: main(query.lower())
	appControl.Win_Opt('close')

def keyboardInput(e):
	user_input = UserField.get().lower()
	if user_input!="":
		clearChatScreen()
		if isContain(user_input, EXIT_COMMANDS):
			speak("Shutting down the System. Good Bye "+ownerDesignation+"!", True, True)
		else:
			Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			attachTOframe(user_input.capitalize())
			Thread(target=main, args=(user_input,)).start()
		UserField.delete(0, END)

###################################### TASK/COMMAND HANDLER #########################################
def isContain(txt, lst):
	for word in lst:
		if word in txt:
			return True
	return False

def main(text):

		if "project" in text:
			if isContain(text, ['make', 'create']):
				speak("What do you want to give the project name ?", True, True)
				projectName = record(False, False)
				speak(fileHandler.CreateHTMLProject(projectName.capitalize()), True)
				return

		if "create" in text and "file" in text:
			speak(fileHandler.createFile(text), True, True)
			return

		if "translate" in text:
			speak("What do you want to translate?", True, True)
			sentence = record(False, False)
			speak("Which langauage to translate ?", True)
			langauage = record(False, False)
			result = normalChat.lang_translate(sentence, langauage)
			if result=="None": speak("This langauage doesn't exists")
			else:
				speak(f"In {langauage.capitalize()} you would say:", True)
				if langauage=="hindi":
					attachTOframe(result.text, True)
					speak(result.pronunciation)
				else: speak(result.text, True)
			return

		if 'list' in text:
			if isContain(text, ['add', 'create', 'make']):
				speak("What do you want to add?", True, True)
				item = record(False, False)
				ToDo.toDoList(item)
				speak("Alright, I added to your list", True)
				return
			if isContain(text, ['show', 'my list']):
				items = ToDo.showtoDoList()
				if len(items)==1:
					speak(items[0], True, True)
					return
				attachTOframe('\n'.join(items), True)
				speak(items[0])
				return

		if isContain(text, ['battery', 'system info']):
			result = appControl.OSHandler(text)
			if len(result)==2:
				speak(result[0], True, True)
				attachTOframe(result[1], True)
			else:
				speak(result, True, True)
			return
			
		if isContain(text, ['meaning', 'dictionary', 'definition', 'define']):
			result = dictionary.translate(text)
			speak(result[0], True, True)
			if result[1]=='': return
			speak(result[1], True)
			return

		if 'volume' in text:
			appControl.volumeControl(text)
			Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)		
			attachTOframe('Volume Settings Changed', True)
			return
			
		if isContain(text, ['timer', 'countdown']):
			Thread(target=timer.startTimer, args=(text,)).start()
			speak('Ok, Timer Started!', True, True)
			return
	
		if 'whatsapp' in text:
			speak("Sure "+ownerDesignation+"...", True, True)
			speak('Whom do you want to send the message?', True)
			WAEMPOPUP("WhatsApp", "Phone Number")
			attachTOframe(rec_phoneno)
			speak('What is the message?', True)
			message = record(False, False)
			Thread(target=webScrapping.sendWhatsapp, args=(rec_phoneno, message,)).start()
			speak("Message is on the way. Do not move away from the screen.")
			attachTOframe("Message Sent", True)
			return

		if 'email' in text:
			speak('Whom do you want to send the email?', True, True)
			WAEMPOPUP("Email", "E-mail Address")
			attachTOframe(rec_email)
			speak('What is the Subject?', True)
			subject = record(False, False)
			speak('What message you want to send ?', True)
			message = record(False, False)
			Thread(target=webScrapping.email, args=(rec_email,message,subject,) ).start()
			speak('Email has been Sent', True)
			return

		if isContain(text, ['covid','virus']):
			result = webScrapping.covid(text)
			if 'str' in str(type(result)):
				speak(result, True, True)
				return
			speak(result[0], True, True)
			result = '\n'.join(result[1])
			attachTOframe(result, True)
			return

		if isContain(text, ['youtube','video']):
			speak("Ok "+ownerDesignation+", here a video for you...", True, True)
			try:
				speak(webScrapping.youtube(text), True)
			except Exception as e:
				speak("Desired Result Not Found", True)
			return

		if isContain(text, ['search', 'image']):
			if 'image' in text and 'show' in text:
				Thread(target=showImages, args=(text,)).start()
				speak('Here are the images...', True, True)
				return
			speak(webScrapping.googleSearch(text), True, True)
			return
			
		if isContain(text, ['map', 'direction']):
			if "direction" in text:
				speak('What is your starting location?', True, True)
				startingPoint = record(False, False)
				speak("Ok "+ownerDesignation+", Where you want to go?", True)
				destinationPoint = record(False, False)
				speak("Ok "+ownerDesignation+", Getting Directions...", True)
				try:
					distance = webScrapping.giveDirections(startingPoint, destinationPoint)
					speak('You have to cover a distance of '+ distance, True)
				except:
					speak("I think location is not proper, Try Again!")
			else:
				webScrapping.maps(text)
				speak('Here you go...', True, True)
			return


		if "joke" in text:
			speak('Here is a joke...', True, True)
			speak(webScrapping.jokes(), True)
			return

		if isContain(text, ['news']):
			speak('Getting the latest news...', True, True)
			headlines,headlineLinks = webScrapping.latestNews(2)
			for head in headlines: speak(head, True)
			speak('Do you want to read the full news?', True)
			text = record(False, False)
			if isContain(text, ["no","don't"]):
				speak("No Problem "+ownerDesignation, True)
			else:
				speak("Ok "+ownerDesignation+", Opening browser...", True)
				webScrapping.openWebsite('https://indianexpress.com/latest-news/')
				speak("You can now read the full news from this website.")
			return

		if isContain(text, ['weather']):
			data = webScrapping.weather()
			speak('', False, True)
			showSingleImage("weather", data[:-1])
			speak(data[-1])
			return

		if isContain(text, ['screenshot']):
			Thread(target=appControl.Win_Opt, args=('screenshot',)).start()
			speak("Screen Shot Taken", True, True)
			return

		if isContain(text, ['window','close that']):
			appControl.Win_Opt(text)
			return

		if isContain(text, ['tab']):
			appControl.Tab_Opt(text)
			return

		if isContain(text, ['setting']):
			raise_frame(root2)
			clearChatScreen()
			return

		if isContain(text, ['open','type','save','delete','select','press enter']):
			appControl.System_Opt(text)
			return

		if isContain(text, ['wiki', 'who is']):
			Thread(target=webScrapping.downloadImage, args=(text, 1,)).start()
			speak('Searching...', True, True)
			result = webScrapping.wikiResult(text)
			showSingleImage('wiki')
			speak(result, True)
			return
		
		
		if isContain(text, ['time','date']):
			speak(normalChat.chat(text), True, True)
			return

		if 'my name' in text:
			speak('Your name is, ' + ownerName, True, True)
			return

		if isContain(text, ['voice']):
			global voice_id
			try:
				if 'female' in text: voice_id = 0
				elif 'male' in text: voice_id = 1
				else:
					if voice_id==0: voice_id=1
					else: voice_id=0
				engine.setProperty('voice', voices[voice_id].id)
				ChangeSettings(True)
				speak("Hello "+ownerDesignation+", I have changed my voice. How may I help you?", True, True)
				assVoiceOption.current(voice_id)
			except Exception as e:
				print(e)
			return


		# if isContain(text, ['create new bank account']):
    	# 		webScrapping.openWebsite('https://www.youtube.com/')
    	# 		speak('To open new bank account we will redirect to our TVS Bank website for filling your credentials to open new bank account. ', True, True)
				
		# 		# speak("You can now read the full news from this website.")
		
		# 	return

		if isContain(text,['how to deposit money to bank account']):
			speak('''There are 3 ways to Deposit money to bank 
			1. Is to Deposit cash at an ATM 
			2. Is to Deposit cash at a local bank or credit union and 
			3. Is to Deposit cash at an online bank.''',True,True)
			return

		if isContain(text,['how to create new bank account']):
			speak('For opening bank account, visit Bank Branch or apply online and submit all documents of proof for KYC then wait for Bank to assess the documents. After proper assement and approval by bank, your bank account has been created successfully. Collect your account details and essential credentials.',True,True)
			return
		
		# if isContain(text,['create new bank account']):
    	# 		speak('To open new bank account we will redirect to our TVS Bank website for filling your credentials to open new bank account. ',True,True)
    	# 		return
		
		if isContain(text,['what documents are required to open a bank account']):
			speak('''The documents required to open a bank account are:
			1. A filled-up application form.
			2. Identity and address proof such as valid passport, voter ID card, PAN card, permanent driving license, Aadhar card, NREGA job card, or ID card issued by central or state governments.
			3. Latest passport size photographs.''',True,True)
			return

		if isContain(text,['what is process for transferring money']):
			speak('''You can transfer money from your one account to another account by cheque you have to simply draw a stating payee as your name along with the account number wherein you want to transfer the amount along with your signature its done immediately at a branch if the transfer is within your bank.''',True,True)
			return

		if isContain(text,['what is process to take loan']):
			speak('''The process to take loan is as follows:
			Step 1: Choose the lender you would like to borrow from based on your research and check for your eligibility.
			Step 2: Visit the bank branch or their official website to apply for the loan.
			Step 3: Submit or upload all the necessary documents and proofs.''',True,True)
			return

		if isContain(text,['what is process to pay loan back to bank']):
			speak('''The process to pay loan back to bank in efficent way is make bi-weekly payments, instead of making monthly payments toward your loan, submit half-payments every two weeks.Round up your monthly payments and make one extra payment each year. Boost your income and put all extra earning towards the loan and cover it as soon as possible.Later on Refinance your money for proft.''',True,True)
			return

		if isContain(text,['what is process to take gold loan']):
			speak('''To do so, you visit a lending institution with the gold you want to pledge and the required documents. The lender performs gold purity checks and determines its weight on the basis of which it evaluates its market value. Gold loans can be sanctioned up to 80 percent of the calculated value of the pledged gold. Once the value of the pledged gold is evaluated, the documents are verified. And once everything seems good and promising to your lender, they approve your loan.''',True,True)
			return

		if isContain(text,['how to open a savings account']):
			speak('''Apply for account through online or filling form at bank.Provide your details and attach documents.Select a single or joint account and accept the terms and conditions. After depositing amount your account will be activated.''',True,True)
			return

		if isContain(text,['what is procedure to apply for debit or credit card']):
			speak('''A savings,fixed or recurring bank deposit account can be opened by a minor of any age through his or her natural or legally appointed guardian. Minors above the age of 10 years may be allowed to open and operate savings bank accounts independently, if they so desire.''',True,True)
			return

		if isContain(text,['what is banking customer care']):
			speak('''A savings,fixed or recurring bank deposit account can be opened by a minor of any age through his or her natural or legally appointed guardian. Minors above the age of 10 years may be allowed to open and operate savings bank accounts independently, if they so desire.''',True,True)
			return

		if isContain(text,['what is process for paying e challan on official site']):
			speak('''Steps to Pay Traffic Challan on e-challan Official Website: 
            Step 1: Visit echallan.parivahan.gov.
            Step 2: Select Check Challan Status from the drop-down menu under Check Online Services.
            Step 3: Enter the required details and captcha.
            Step 4: Click on Get Detail.
            Step 5: Click on Pay Now option.''',True,True)
			return

		if isContain(text,['what is a credit limit']):
			speak('''A credit limit is the maximum amount of credit that a lender or credit card issuer extends to a borrower. It represents the maximum outstanding balance that the borrower can carry on a credit account''',True,True)
			return

		if isContain(text,['what is a notary public']):
			speak('''A notary public is an authorized individual who can witness and certify the signing of important documents, administer oaths, and verify the authenticity of signatures. Banks often have notary services available to their customers''',True,True)
			return

		if isContain(text,['what is the role of the fiu in the banking industry']):
			speak('''The Financial Intelligence Unit (FIU) is a government agency that collects, analyzes, and disseminates financial intelligence related to money laundering, terrorist financing, and other financial crimes. Banks are required to report suspicious transactions to the FIU''',True,True)
			return

		if isContain(text,['what is the purpose of a banks annual general meeting']):
			speak('''A bank's annual general meeting (AGM) is a gathering of shareholders to discuss and vote on important matters, such as the election of directors, approval of financial statements, and any proposed changes to the bank's articles of incorporation''',True,True)
			return

		if isContain(text,['what is a cash advance']):
			speak('''A cash advance is a short-term loan provided by a credit card issuer, allowing the cardholder to withdraw cash against their credit limit. Cash advances often carry higher interest rates and additional fees compared to regular credit card purchases''',True,True)
			return


		if isContain(text,['what is the role of the financial services authority in the banking sector']):
			speak('''The Financial Services Authority (FSA) was a regulatory body in the UK that supervised financial services firms, including banks, until its responsibilities were transferred to other regulatory bodies, such as the Financial Conduct Authority (FCA) and the Prudential Regulation Authority (PRA)''',True,True)
			return

		if isContain(text,['what is a standing order']):
			speak('''A standing order is an instruction given by an account holder to their bank to make regular, fixed payments to a specific recipient. It is commonly used for recurring payments such as rent, mortgage installments, or subscription fees''',True,True)
			return

		if isContain(text,['what is the purpose of a banks compliance department']):
			speak('''A bank's compliance department ensures that the institution operates in accordance with applicable laws, regulations, and internal policies. It develops and implements compliance programs, monitors activities for compliance risks, and educates employees on regulatory requirements''',True,True)
			return

		if isContain(text,['what is a credit default swap']):
			speak('''A credit default swap is a financial derivative contract in which one party agrees to compensate another party if a specific borrower defaults on their debt obligations. It is often used as a risk management tool to hedge against credit risks''',True,True)
			return

		if isContain(text,['what is a negotiable certificate of deposit']):
			speak('''A negotiable certificate of deposit is a time deposit issued by a bank with a specified maturity date. Unlike regular certificates of deposit, NCDs can be bought and sold on the secondary market before their maturity, making them a tradable instrument''',True,True)
			return
				
		if isContain(text,['what is a bridge loan']):
			speak('''A bridge loan is a short-term loan used to bridge a financial gap between the purchase of a new property and the sale of an existing one. It provides temporary financing until the borrower secures permanent financing or completes the sale of the property''',True,True)
			return

		if isContain(text,['what is the purpose of a banks customer due diligence process']):
			speak('''A bank's customer due diligence (CDD) process is a series of procedures conducted to verify the identity of customers, assess their risk profile, and ensure compliance with anti-money laundering (AML) and know your customer (KYC) requirements''',True,True)
			return

		if isContain(text,['what is an electronic funds transfer']):
			speak('''An electronic funds transfer is a method of transferring money electronically from one bank account to another. It can be initiated through online banking, mobile banking, wire transfers, or automated clearinghouse (ACH) transactions''',True,True)
			return

		if isContain(text,['what is the purpose of a safe deposit box']):
			speak('''A safe deposit box is a secure storage space provided by a bank where customers can store valuable items such as important documents, jewelry, or other valuable possessions''',True,True)
			return


		if isContain(text,['what is the role of the securities and exchange commission in the banking industry']):
			speak('''The Securities and Exchange Commission (SEC) regulates and supervises securities markets, including the activities of banks that engage in securities-related transactions. It ensures transparency, investor protection, and the integrity of the banking and financial markets''',True,True)
			return

		if isContain(text,['what are the factors that affect mortgage interest rates']):
			speak('''Several factors can influence mortgage interest rates, including the borrower's credit score, loan-to-value ratio, market conditions, inflation rates, economic indicators, and the type and term of the mortgage loan''',True,True)
			return

		if isContain(text,['what is a certificate of deposit']):
			speak('''A certificate of deposit (CD) is a time deposit offered by banks where customers deposit a specific amount of money for a fixed period at a fixed interest rate. CDs typically offer higher interest rates compared to regular savings accounts''',True,True)
			return

		if isContain(text,['what is the role of the consumer financial protection bureau']):
			speak('''The Consumer Financial Protection Bureau (CFPB) is a government agency responsible for protecting consumers in the financial marketplace. It enforces consumer protection laws, regulates financial institutions, and educates consumers about their rights and responsibilities''',True,True)
			return

		if isContain(text,['what is the purpose of a swift code']):
			speak('''A SWIFT code, also known as a Bank Identifier Code (BIC), is a unique code used to identify specific banks or financial institutions worldwide. It is primarily used for international wire transfers and ensures accurate routing of funds''',True,True)
			return

		if isContain(text,['what are the advantages of using contactless payment methods']):
			speak('''Contactless payment methods, such as mobile wallets or contactless cards, offer convenience, speed, and enhanced security. They allow for quick and secure transactions by simply tapping or waving the payment device near a contactless-enabled terminal''',True,True)
			return

		if isContain(text,['what is a money market account']):
			speak('''A money market account is a type of savings account that typically offers higher interest rates than regular savings accounts. It may require a higher minimum balance and often allows a limited number of transactions per month''',True,True)
			return

		if isContain(text,['what is the purpose of a banks routing number']):
			speak('''A bank's routing number is a unique nine-digit code used to identify the financial institution in the United States. It is primarily used for electronic funds transfers, such as direct deposits, bill payments, and wire transfers''',True,True)
			return
				
		if isContain(text,['what is the role of the international monetary fund in the banking sector']):
			speak('''The International Monetary Fund (IMF) promotes global financial stability and provides financial assistance to member countries facing economic challenges. It also conducts surveillance on the global financial system and offers policy advice to member nations''',True,True)
			return

		if isContain(text,['what is the difference between a checking account and a savings account']):
			speak('''A checking account is designed for frequent transactions, providing easy access to funds through checks, debit cards, and electronic transfers. A savings account, on the other hand, is primarily for saving money and earning interest, with limited transaction capabilities''',True,True)
			return

		if isContain(text,['what is the purpose of the know your customer process in banking']):
			speak('''The Know Your Customer (KYC) process is a regulatory requirement in the banking industry that aims to verify the identity and assess the suitability of customers. It helps prevent money laundering, fraud, and other illicit activities''',True,True)
			return

		if isContain(text,['what is the role of the bank for international settlements in the global banking system']):
			speak('''The Bank for International Settlements (BIS) serves as a central bank for central banks. It fosters international monetary and financial cooperation, acts as a hub for information sharing and research, and provides a forum for discussions among central banks and financial institutions''',True,True)
			return

		if isContain(text,['what is an overdraft fee']):
			speak('''An overdraft fee is a fee charged by a bank when an account holder spends more money than is available in their account. It typically occurs when a transaction exceeds the account balance, and the bank covers the shortfall temporarily, charging a fee for this service''',True,True)
			return

		if isContain(text,['what are the common types of credit cards']):
			speak('''Common types of credit cards include rewards cards, cashback cards, travel cards, secured cards, balance transfer cards, and co-branded cards affiliated with specific retailers or organizations''',True,True)
			return

		if isContain(text,['what is the role of a banks board of directors']):
			speak('''A bank's board of directors is responsible for overseeing the bank's operations, setting strategic goals, ensuring regulatory compliance, appointing senior management, and representing the interests of shareholders''',True,True)
			return

		if isContain(text,['what is the purpose of the dodd frank act in the banking industry']):
			speak('''The Dodd-Frank Act is a U.S. legislation that aims to regulate the financial industry, enhance consumer protection, prevent systemic risks, and provide a framework for the orderly resolution of failing financial institutions''',True,True)
			return

		if isContain(text,['what is a wire transfer']):
			speak('''A wire transfer is a method of electronically transferring funds from one bank account to another, either domestically or internationally. It provides a secure and efficient way to send money quickly''',True,True)
			return

		if isContain(text,['what is the role of the bank secrecy act in combating money laundering']):
			speak('''The Bank Secrecy Act (BSA) requires financial institutions to establish robust anti-money laundering (AMLprocedures. It mandates the reporting of certain transactions and suspicious activities to the appropriate authorities, helping to detect and prevent money laundering and other illicit financial activities''',True,True)
			return

		if isContain(text,['what is a mortgage']):
			speak('''A mortgage is a loan provided by a bank or lender to finance the purchase of a property. It is secured by the property itself and typically repaid in monthly installments over a predetermined period, often spanning several years''',True,True)
			return

		if isContain(text,['what is the role of the office of the comptroller of the currency in the banking sector']):
			speak('''The Office of the Comptroller of the Currency (OCC) is a U.S. federal agency that regulates and supervises national banks. It ensures the safety and soundness of the banking system, promotes fair and equal access to financial services, and enforces compliance with banking laws and regulations''',True,True)
			return

		if isContain(text,['what is a credit score and how is it calculated']):
			speak('''A credit score is a numerical representation of an individual's creditworthiness, based on their credit history. It is calculated using various factors, including payment history, credit utilization, length of credit history, types of credit, and new credit applications''',True,True)
			return

		if isContain(text,['what is the purpose of the financial stability oversight council in the banking industry']):
			speak('''The Financial Stability Oversight Council (FSOC) is a U.S. government body responsible for identifying and addressing risks to the stability of the financial system. It coordinates the activities of various regulatory agencies to ensure a comprehensive approach to maintaining financial stability''',True,True)
			return

		if isContain(text,['what is the purpose of a banks annual report']):
			speak('''A bank's annual report provides comprehensive information about its financial performance, strategic objectives, risk management practices, and governance structure. It is designed to keep shareholders, regulators, and other stakeholders informed about the bank's operations and results''',True,True)
			return

		if isContain(text,['what is the role of the basel committee on banking supervision in the global banking system']):
			speak('''The Basel Committee on Banking Supervision (BCBS) is a global forum that develops and promotes international standards for banking supervision. Its primary objective is to enhance the stability and resilience of the banking system and foster global cooperation among regulators''',True,True)
			return

		if isContain(text,['what is a home equity loan']):
			speak('''A home equity loan is a type of loan that allows homeowners to borrow against the equity they have built in their property. The loan is secured by the property and can be used for various purposes, such as home improvements or debt consolidation''',True,True)
			return

		if isContain(text,['what is the role of the financial action task force in combating money laundering and terrorist financing']):
			speak('''The Financial Action Task Force (FATF) is an intergovernmental organization that sets global standards and promotes effective measures to combat money laundering, terrorist financing, and other threats to the integrity of the international financial system''',True,True)
			return

		if isContain(text,['what is the purpose of a banks stress test']):
			speak('''A bank's stress test is a financial analysis conducted to assess its ability to withstand adverse economic conditions. It helps evaluate the bank's capital adequacy and risk management practices under various hypothetical scenarios''',True,True)
			return

		if isContain(text,['what is a debit card']):
			speak('''A debit card is a payment card that allows you to access funds directly from your bank account to make purchases or withdraw cash. It deducts the purchase amount immediately from your account, unlike a credit card where you borrow money to make purchases''',True,True)
			return

		if isContain(text,['what is the role of the financial crimes enforcement network in the banking industry']):
			speak('''The Financial Crimes Enforcement Network (FinCEN) is a U.S. government agency responsible for collecting, analyzing, and disseminating financial intelligence to combat money laundering, terrorist financing, and other financial crimes''',True,True)
			return
				
		if isContain(text,['what is a pre approval for a mortgage']):
			speak('''A pre-approval for a mortgage is a preliminary assessment by a lender indicating the amount you may be eligible to borrow for a home purchase. It is based on an initial review of your financial information and helps you understand your budget and negotiate with sellers''',True,True)
			return

		if isContain(text,['what is the purpose of a banks liquidity ratio']):
			speak('''A bank's liquidity ratio measures its ability to meet short-term obligations and withstand unexpected cash outflows. It compares a bank's liquid assets, such as cash and easily marketable securities, to its short-term liabilities''',True,True)
			return

		if isContain(text,['what is the role of the office of thrift supervision in the banking sector']):
			speak('''The Office of Thrift Supervision (OTS) was a U.S. federal agency responsible for regulating and supervising federal savings associations and their parent companies. However, as of 2011, its supervisory responsibilities were transferred to other regulatory agencies''',True,True)
			return

		if isContain(text,['what is the purpose of the community reinvestment act in the banking industry']):
			speak('''The Community Reinvestment Act (CRA) is a U.S. legislation that encourages banks to meet the credit needs of the communities they serve, particularly low- and moderate-income neighborhoods. It aims to prevent discriminatory lending practices and promote access to credit in underserved areas''',True,True)
			return

		if isContain(text,['what is a trust account']):
			speak('''A trust account is a legal arrangement where a trustee holds and manages assets on behalf of a beneficiary. Trust accounts are commonly used for estate planning, managing funds for minors, or protecting assets in specific circumstances''',True,True)
			return

		if isContain(text,['what is the purpose of a banks asset liability management framework']):
			speak('''A bank's asset-liability management (ALM) framework helps it manage the balance between its assets (loans, investments) and liabilities (deposits, borrowings). It aims to minimize interest rate and liquidity risks and ensure the bank's financial stability''',True,True)
			return

		if isContain(text,['what is a money order']):
			speak('''A money order is a prepaid payment instrument that functions similar to a check. It is issued by a financial institution or postal service and allows the recipient to receive a specified amount of money, usually without the need for a bank account''',True,True)
			return

		if isContain(text,['what is the role of the office of foreign assets control in the banking industry']):
			speak('''The Office of Foreign Assets Control (OFAC) is a U.S. government agency that administers and enforces economic and trade sanctions against targeted foreign countries, individuals, and entities. Banks are required to comply with OFAC regulations to prevent financial transactions involving sanctioned parties''',True,True)
			return

		if isContain(text,['what is the purpose of a banks capital adequacy ratio']):
			speak('''A bank's capital adequacy ratio measures its capital in relation to its risk-weighted assets. It helps assess the bank's ability to absorb losses and maintain solvency, as required by regulatory guidelines''',True,True)
			return

		if isContain(text,['what is a negotiable instrument']):
			speak('''A negotiable instrument is a document that guarantees the transfer of a specified amount of money from one party to another. Examples include checks, promissory notes, and bills of exchange, which can be transferred or endorsed to facilitate payments''',True,True)
			return

		if isContain(text,['what is the role of the financial services compensation scheme in the banking sector']):
			speak('''The Financial Services Compensation Scheme (FSCS) is a UKcompensation fund that protects customers of financial services firms, including banks. It provides compensation to eligible customers in the event of a firm's failure, up to a certain limit, to help maintain confidence in the financial system''',True,True)
			return

		if isContain(text,['what is a credit report']):
			speak('''A credit report is a detailed record of an individual's credit history, including information about their borrowing and repayment behavior. It includes credit accounts, payment history, outstanding debts, and inquiries made by lenders or creditors''',True,True)
			return

		if isContain(text,['what is the purpose of a banks anti money laundering program']):
			speak('''A bank's anti-money laundering (AML) program is designed to detect and prevent money laundering and other illicit financial activities. It includes measures such as customer due diligence, transaction monitoring, and reporting suspicious activities to regulatory authorities''',True,True)
			return

		if isContain(text,['what is a co signer']):
			speak('''A co-signer is a person who agrees to take equal responsibility for repaying a loan or debt if the primary borrower fails to do so. Co-signers provide an additional layer of assurance to lenders, particularly when the primary borrower has a limited credit history or low credit score''',True,True)
			return

		if isContain(text,['what is the role of the central bank in the banking system']):
			speak('''The Central Bank, also known as the monetary authority or reserve bank, is responsible for formulating and implementing monetary policy, regulating and supervising banks, maintaining financial stability, and issuing currency in a country''',True,True)
			return

		if isContain(text,['what is a foreign exchange market']):
			speak('''The foreign exchange market is a global decentralized marketplace where currencies are bought and sold. It facilitates international trade and investment by allowing participants to exchange one currency for another at agreed-upon exchange rates''',True,True)
			return

		if isContain(text,['what is the purpose of a banks loan loss provision']):
			speak('''A bank's loan loss provision is an accounting practice where a portion of profits is set aside as a reserve to cover potential loan losses. It helps mitigate the impact of bad loans on the bank's financial stability and ensures adequate capital to absorb potential credit losses''',True,True)
			return

		if isContain(text,['what is a wire transfer fee']):
			speak('''A wire transfer fee is a charge levied by banks for facilitating the transfer of funds electronically from one bank to another. The fee covers the operational and administrative costs associated with processing the wire transfer''',True,True)
			return

		if isContain(text,['what is the role of the financial ombudsman service in the banking industry']):
			speak('''The Financial Ombudsman Service is an independent organization that helps resolve disputes between consumers and financial services providers, including banks. It provides a neutral platform for customers to seek a fair resolution when they are dissatisfied with a bank's response to a complaint''',True,True)
			return

		if isContain(text,['what is a savings bond']):
			speak('''A savings bond is a government-issued debt security that individuals can purchase to lend money to the government. It accrues interest over a fixed period and can be redeemed at maturity for the principal amount plus accrued interest''',True,True)
			return

		if isContain(text,['what is the purpose of a banks credit risk management']):
			speak('''A bank's credit risk management involves identifying, assessing, and mitigating the risks associated with lending activities. It aims to ensure that borrowers have the ability and willingness to repay their debts, thereby minimizing potential credit losses''',True,True)
			return

		if isContain(text,['what is a dormant account']):
			speak('''A dormant account is a bank account that has had no customer-initiated activity or transactions for an extended period. Banks may classify accounts as dormant to safeguard funds and prevent unauthorized access, but customers can reactivate them by following the bank's reactivation process''',True,True)
			return

		if isContain(text,['what is the role of the financial accounting standards board in the banking industry']):
			speak('''The Financial Accounting Standards Board (FASB) establishes and improves accounting standards in the United States, including those related to the banking industry. It ensures transparency and consistency in financial reporting, enabling stakeholders to make informed decisions''',True,True)
			return

		if isContain(text,['what is a prime rate']):
			speak('''A prime rate is the interest rate that commercial banks charge their most creditworthy customers. It serves as a benchmark for determining interest rates on various loans, such as mortgages, personal loans, and business loans''',True,True)
			return

		if isContain(text,['what is the purpose of a banks information security measures']):
			speak('''A bank's information security measures aim to protect sensitive customer data, prevent unauthorized access, and mitigate the risk of cyber threats. These measures include firewalls, encryption, multi-factor authentication, employee training, and regular security audits''',True,True)
			return

		if isContain(text,['what is a merchant account']):
			speak('''A merchant account is a type of bank account that enables businesses to accept and process credit card payments from customers. It allows the funds from credit card transactions to be deposited into the merchant's account after deducting fees and charges''',True,True)
			return
				
		if isContain(text,['what is the role of the fca in the banking sector']):
			speak('''The Financial Conduct Authority (FCA) is a regulatory body in the UK that oversees the conduct of financial firms, including banks. It sets and enforces standards to ensure fair treatment of customers, market integrity, and effective competition''',True,True)
			return

		if isContain(text,['what is a foreclosure']):
			speak('''A foreclosure is a legal process where a lender takes ownership of a property when the borrower fails to make mortgage payments as agreed. The lender typically sells the property to recover the outstanding debt''',True,True)
			return

		if isContain(text,['what is the purpose of a banks trust department']):
			speak('''A bank's trust department manages trusts and provides fiduciary services, acting as a trustee or executor for individuals and organizations. It administers assets, manages investments, distributes funds, and ensures compliance with legal and fiduciary responsibilities''',True,True)
			return

		if isContain(text,['what is the purpose of a banks trust department']):
			speak('''A bank's trust department manages trusts and provides fiduciary services, acting as a trustee or executor for individuals and organizations. It administers assets, manages investments, distributes funds, and ensures compliance with legal and fiduciary responsibilities''',True,True)
			return

		if isContain(text,['what is the role of the financial industry regulatory authority in the banking industry']):
			speak('''The Financial Industry Regulatory Authority (FINRA) is a self-regulatory organization that oversees and regulates brokerage firms and registered representatives in the United States. It establishes rules and standards to protect investors and ensure fair and transparent markets''',True,True)
			return

		if isContain(text,['what is a joint tenancy with right of survivorship']):
			speak('''Joint tenancy with right of survivorship is a form of property ownership where two or more individuals hold equal ownership rights to a property. In the event of the death of one owner, their share automatically transfers to the surviving owner(s)''',True,True)
			return

		if isContain(text,['what is the purpose of a banks investment banking division']):
			speak('''A bank's investment banking division provides a range of financial services to corporations, institutions, and governments. These services include underwriting securities offerings, advising on mergers and acquisitions, facilitating capital raising, and providing strategic financial advice''',True,True)
			return

		if isContain(text,['what is a negotiable certificate of deposit']):
			speak('''A negotiable certificate of deposit is a time deposit issued by a bank with a specified maturity date. Unlike regular certificates of deposit, NCDs can be bought and sold on the secondary market before their maturity, making them a tradable instrument''',True,True)
			return

		if isContain(text,['what is the role of the international swaps and derivatives association in the banking industry']):
			speak('''The International Swaps and Derivatives Association (ISDA) is a trade association that represents participants in the global derivatives market. It develops and promotes standardized documentation and best practices, and provides a forum for addressing industry issues''',True,True)
			return

		if isContain(text,['what is an eft']):
			speak('''An electronic funds transfer is a method of transferring money electronically from one bank account to another. It can be initiated through online banking, mobile banking, wire transfers, or automated clearinghouse (ACH) transactions''',True,True)
			return

		if isContain(text,['what is the role of the financial stability board in the banking sector']):
			speak('''The Financial Stability Board (FSB) is an international body that monitors and makes recommendations about the global financial system. It promotes financial stability, coordinates regulatory policies, and assesses vulnerabilities and risks in the global economy''',True,True)
			return

		if isContain(text,['what is a credit counseling service']):
			speak('''A credit counseling service is a nonprofit organization that provides assistance to individuals struggling with debt management. They offer financial education, budgeting advice, and debt repayment plans to help individuals regain control of their finances''',True,True)
			return

		if isContain(text,['what is a securities brokerage account']):
			speak('''A securities brokerage account is an account provided by a brokerage firm that allows investors to buy, sell, and hold various types of securities, such as stocks, bonds, mutual funds, and exchange-traded funds (ETFs)''',True,True)
			return

		if isContain(text,['what is the role of the ncua in the banking sector']):
			speak('''The National Credit Union Administration (NCUA) is a U.S. government agency that regulates and supervises federal credit unions. It ensures the safety and soundness of credit unions and protects the deposits of credit union members''',True,True)
			return

		if isContain(text,['what is a credit freeze']):
			speak('''A credit freeze, also known as a security freeze, is a measure taken by individuals to restrict access to their credit reports. It helps prevent identity theft by making it difficult for unauthorized parties to open new credit accounts in the individual's name''',True,True)
			return

		if isContain(text,['what is a credit freeze']):
			speak('''A credit freeze, also known as a security freeze, is a measure taken by individuals to restrict access to their credit reports. It helps prevent identity theft by making it difficult for unauthorized parties to open new credit accounts in the individual's name''',True,True)
			return

		if isContain(text,['what is the purpose of a banks overdraft protection service']):
			speak('''A bank's overdraft protection service is an optional feature that allows customers to link their checking accounts to another account or line of credit. It provides a safety net by covering insufficient funds in the checking account, preventing overdraft fees and declined transactions''',True,True)
			return

		if isContain(text,['what is a letter of credit']):
			speak('''A letter of credit is a financial instrument issued by a bank on behalf of a buyer to guarantee payment to a seller upon meeting specific conditions. It provides assurance to the seller that they will receive payment, and it mitigates the risk for the buyer''',True,True)
			return

		if isContain(text,['what is the role of the financial services compensation scheme in the banking sector']):
			speak('''The Financial Services Compensation Scheme (FSCS) is a UK compensation fund that protects customers of financial services firms, including banks. It provides compensation to eligible customers in the event of a firm's failure, up to a certain limit, to help maintain confidence in the financial system''',True,True)
			return

		if isContain(text,['what is a payday loan']):
			speak('''A payday loan is a short-term, high-interest loan typically used by individuals to cover unexpected expenses until their next paycheck. Payday loans often come with high fees and are intended for short-term use''',True,True)
			return
				
		if isContain(text,['what is the purpose of a banks compliance officer']):
			speak('''A bank's compliance officer is responsible for ensuring that the institution adheres to all applicable laws, regulations, and internal policies. They develop and implement compliance programs, conduct risk assessments, and monitor activities to mitigate compliance risks''',True,True)
			return

		if isContain(text,['what is a credit default']):
			speak('''A credit default occurs when a borrower fails torepay their debt obligation as agreed, resulting in a default. It indicates that the borrower is unable or unwilling to fulfill their financial obligations, potentially leading to financial losses for the lender or investor''',True,True)
			return

		if isContain(text,['what is the role of the bis in the global banking system']):
			speak('''The Bank for International Settlements (BIS) serves as a central bank for central banks. It fosters international monetary and financial cooperation, acts as a hub for information sharing and research, and provides a forum for discussions among central banks and financial institutions''',True,True)
			return

		if isContain(text,['what is a clo']):
			speak('''A collateralized loan obligation is a structured financial product that pools together a portfolio of loans, typically corporate loans, and issues multiple tranches of securities backed by those loans. Investors can invest in different tranches based on their risk and return preferences''',True,True)
			return

		if isContain(text,['what is the purpose of a banks trade finance services']):
			speak('''A bank's trade finance services facilitate international trade by providing financial solutions to businesses involved in importing and exporting goods and services. These services may include letters of credit, documentary collections, export financing, and trade risk mitigation''',True,True)
			return

		if isContain(text,['what is a credit inquiry']):
			speak('''A credit inquiry is a request made by a lender or creditor to access an individual's credit report and assess their creditworthiness. Credit inquiries can be either hard inquiries, which may impact credit scores, or soft inquiries, which do not affect credit scores''',True,True)
			return

		if isContain(text,['what is the role of the imf in the banking sector']):
			speak('''The International Monetary Fund (IMF) promotes global financial stability and provides financial assistance to member countries facing economic challenges. It also conducts surveillance on the global financial system and offers policy advice to member nations''',True,True)
			return

		if isContain(text,['what is a small business loan']):
			speak('''A small business loan is a type of loan specifically designed to meet the financing needs of small businesses. It can be used for various purposes, such as starting a business, expanding operations, purchasing equipment, or managing cash flow''',True,True)
			return

		if isContain(text,['what is the purpose of a banks compliance training program']):
			speak('''A bank's compliance training program aims to educate employees about applicable laws, regulations, and internal policies. It helps ensure that employees understand their responsibilities, promote ethical conduct, and mitigate compliance risks within the organization''',True,True)
			return

		if isContain(text,['what is a credit bureau']):
			speak('''A credit bureau is a company that collects and maintains credit information on individuals and businesses. It compiles credit reports that contain credit history, payment patterns, outstanding debts, and other relevant information used by lenders to assess creditworthiness''',True,True)
			return

		if isContain(text,['what is the role of the fincen in the banking industry']):
			speak('''The Financial Crimes Enforcement Network (FinCEN) is a U.S. government agency responsible for collecting, analyzing, and disseminating financial intelligence to combat money laundering, terrorist financing, and other financial crimes''',True,True)
			return

		if isContain(text,['what is the role of the fincen in the banking industry']):
			speak('''The Financial Crimes Enforcement Network (FinCEN) is a U.S. government agency responsible for collecting, analyzing, and disseminating financial intelligence to combat money laundering, terrorist financing, and other financial crimes''',True,True)
			return

		if isContain(text,['what is a mortgage backed security']):
			speak('''A mortgage-backed security is a type of financial instrument that represents an ownership interest in a pool of mortgage loans. Investors receive regular payments based on the interest and principal payments made by the underlying mortgage borrowers''',True,True)
			return

		if isContain(text,['what is the purpose of a banks risk management framework']):
			speak('''A bank's risk management framework aims to identify, assess, and mitigate various risks that the institution faces. It includes processes, policies, and controls to manage credit risk, market risk, operational risk, liquidity risk, and other potential threats to the bank's stability and profitability''',True,True)
			return

		if isContain(text,['what is a business line of credit']):
			speak('''A business line of credit is a flexible financing option that provides businesses with access to a predetermined credit limit. It allows businesses to borrow funds as needed and repay them over time, providing financial flexibility for managing cash flow and short-term expenses''',True,True)
			return

		if isContain(text,['what is the role of the fca in the banking sector']):
			speak('''The Financial Conduct Authority (FCA) is a regulatory body in the UK that oversees the conduct of financial firms, including banks. It sets and enforces standards to ensure fair treatment of customers, market integrity, and effective competition''',True,True)
			return

		if isContain(text,['what is a financial statement']):
			speak('''A financial statement is a formal record of the financial activities and position of an individual, company, or organization. It includes balance sheets, income statements, cash flow statements, and other relevant information that provides an overview of the entity's financial performance''',True,True)
			return

		if isContain(text,['what is the purpose of a banks asset management division']):
			speak('''A bank's asset management division is responsible for managing investment portfolios on behalf of clients, including individuals, institutions, and corporations. It involves making investment decisions, providing financial advice, and monitoring the performance of assets to achieve clients' financial goals''',True,True)
			return

		if isContain(text,['what is a money market fund']):
			speak('''A money market fund is a type of mutual fund that investsin short-term, low-risk securities such as Treasury bills, certificates of deposit, and commercial paper. It aims to provide investors with stability and liquidity while generating a modest level of interest income''',True,True)
			return

		if isContain(text,['what is the role of the occ in the banking sector']):
			speak('''The Office of the Comptroller of the Currency (OCC) is a U.S. federal agency that regulates and supervises national banks. It ensures the safety and soundness of the banking system, promotes fair and equal access to financial services, and enforces compliance with banking laws and regulations''',True,True)
			return

		if isContain(text,['what is a home equity line of credit']):
			speak('''A home equity line of credit (HELOC) is a revolving line of credit that allows homeowners to borrow against the equity in their property. It functions similar to a credit card, where funds can be accessed as needed, and the borrower only pays interest on the amount borrowed''',True,True)
			return

		if isContain(text,['what is the purpose of a banks chief risk officer']):
			speak('''A bank's chief risk officer (CRO) is responsible for overseeing and managing the institution's overall risk management activities. They assess and mitigate risks across various areas, including credit risk, market risk, operational risk, and compliance risk, to ensure the bank's stability and regulatory compliance''',True,True)
			return

		if isContain(text,['what is a business credit card']):
			speak('''A business credit card is a payment card specifically designed for business use. It allows businesses to make purchases, track expenses, and separate business and personal finances. Business credit cards often offer additional features and rewards tailored to the needs of businesses''',True,True)
			return

		if isContain(text,['what is the role of the fiu in the banking industry']):
			speak('''The Financial Intelligence Unit (FIU) is a government agency that collects, analyzes, and disseminates financial intelligence related to money laundering, terrorist financing, and other financial crimes. Banks are required to report suspicious transactions to the FIU''',True,True)
			return

		if isContain(text,['what is a home appraisal']):
			speak('''A home appraisal is an assessment conducted by a qualified appraiser to determine the market value of a property. It takes into account factors such as location, condition, size, and comparable sales to provide an unbiased estimate of the property's worth''',True,True)
			return

		if isContain(text,['what is the purpose of a banks compliance audit']):
			speak('''A bank's compliance audit is an independent review of the institution's operations, policies, and procedures to ensure compliance with applicable laws, regulations, and internal policies. It helps identify areas of non-compliance, assess the effectiveness of controls, and recommend improvements''',True,True)
			return

		if isContain(text,['what is a chargeback']):
			speak('''A chargeback is a reversal of a credit card transaction initiated by the cardholder, typically due to a dispute or fraudulent activity. It allows the cardholder to request a refund from the card issuer, who investigates the claim and may refund the transaction amount if it is deemed valid''',True,True)
			return

		if isContain(text,['what is the role of the fscs in the banking sector']):
			speak('''The Financial Services Compensation Scheme (FSCS) is a UK compensation fund that protects customers of financial services firms, including banks. It provides compensation to eligible customers in the event of a firm's failure, up to a certain limit, to help maintain confidence in the financial system''',True,True)
			return

		if isContain(text,['what is a term deposit']):
			speak('''A term deposit, also known as a fixed deposit or certificate of deposit (CD), is a type of investment where funds are deposited with a financial institution for a specified period at a fixed interest rate. The funds are locked in for the term, and early withdrawals may incur penalties''',True,True)
			return

		if isContain(text,['what is the purpose of a banks private banking division']):
			speak('''A bank's private banking division provides personalized financial services and investment management to high-net-worth individuals and families. It offers tailored solutions, including wealth planning, estate management, investment advice, and access to exclusive investment opportunities''',True,True)
			return

		if isContain(text,['what is the procedure to file complaint against in case of wrong transaction']):
			speak('''First Go To The Bank Employee and take the complaint form then fill out your details like your Bank ID number, Name, Mobile number, address, and all others details required. Write in brief about the problem/complaint and submit the form''',True,True)
			return

		if isContain(text,['what are the benefits of having a savings account']):
			speak('''Some benefits of having a savings account include earning interest on your deposits, the ability to save money for future goals, easy access to your funds, and the opportunity to establish a banking relationship''',True,True)
			return

		if isContain(text,['how can i check my bank account balance']):
			speak('''You can check your bank account balance through various methods such as online banking, mobile banking apps, ATM machines, or by visiting your bank's branch and inquiring with a bank representative''',True,True)
			return

		if isContain(text,['what are the different types of loans offered by banks']):
			speak('''Banks offer various types of loans, including personal loans, home loans, car loans, education loans, business loans, and credit card loans, each designed to fulfill specific financial needs''',True,True)
			return

		if isContain(text,['what is the role of a bank in the economy']):
			speak('''The role of a bank in the economy is to facilitate financial transactions, provide loans and credit, offer a safe place for individuals and businesses to deposit their money, and promote economic growth''',True,True)
			return

		if isContain(text,['what are the advantages of using online banking']):
			speak('''The advantages of using online banking include 24/7 access to your accounts, the ability to view transactions and statements online, transfer funds between accounts, pay bills electronically, and convenience in managing your finances from anywhere with an internet connection''',True,True)
			return

		if isContain(text,['how can i protect my bank account from unauthorized access']):
			speak('''To protect your bank account from unauthorized access, you should use strong and unique passwords, enable two-factor authentication, avoid sharing personal information online, regularly monitor your account statements, and be cautious of phishing attempts or suspicious links''',True,True)
			return

		if isContain(text,['what is a fixed deposit account']):
			speak('''A fixed deposit account, also known as a term deposit, is a type of bank account where a specific amount of money is deposited for a fixed period at a predetermined interest rate. The funds are locked in for the agreed-upon period, and the account holder earns interest on the deposited amount''',True,True)
			return

		if isContain(text,['what are the common fees associated with a checking account']):
			speak('''Common fees associated with a checking account may include monthly maintenance fees, overdraft fees, ATM usage fees, wire transfer fees, and fees for additional services such as check printing or stop payment requests''',True,True)
			return

		if isContain(text,['what is the difference between a debit card and a credit card']):
			speak('''A debit card allows you to spend money by drawing funds directly from your checking account, whereas a credit card allows you to borrow money up to a certain credit limit. Debit card purchases are deducted from your account immediately, while credit card purchases accumulate as a balance to be paid off later''',True,True)
			return

		if isContain(text,['how can i improve my credit score']):
			speak('''To improve your credit score, you can pay your bills on time, keep credit card balances low, avoid opening multiple new accounts within a short period, maintain a diverse mix of credit accounts, and regularly review your credit reports for any errors''',True,True)
			return

		if isContain(text,['what is the role of the federal reserve in the banking system']):
			speak('''The Federal Reserve, often referred to as the central bank of the United States, is responsible for implementing monetary policy, supervising and regulating banks, providing financial services to depository institutions, and maintaining the stability of the financial system''',True,True)
			return

		if isContain(text,['what is compound interest']):
			speak('''Compound interest is the interest calculated on the initial amount deposited (principal) as well as any accumulated interest. It means that the interest you earn is added to the principal, and future interest calculations are based on the new total, resulting in exponential growth over time''',True,True)
			return

		if isContain(text,['what should i do if i lose my credit card']):
			speak('''If you lose your credit card, you should immediately contact your card issuer to report the loss and request a card replacement. They will help you cancel the lost card and issue a new one to ensure the security of your account''',True,True)
			return

		if isContain(text,['what is the difference between a savings account and a current account']):
			speak('''A savings account is typically used for storing money and earning interest, while a current account is designed for frequent transactions and does not usually earn interest. Additionally, savings accounts often have limitations on withdrawals, whereas current accounts provide more flexibility''',True,True)
			return

		if isContain(text,['how can i apply for a bank loan']):
			speak('''To apply for a bank loan, you can visit your preferred bank's branch or their website and request an application form. Fill out the necessary information, provide supporting documents such as income proof and collateral details if required, and submit the completed application along with the required documentation''',True,True)
			return

		if isContain(text,['what are the benefits of online banking']):
			speak('''Online banking offers several benefits, including 24/7 access to your accounts, the ability to view transactions and statements online, transfer funds between accounts, pay bills electronically, and convenient management of your finances from anywhere with an internet connection''',True,True)
			return

		if isContain(text,['what is the role of a bank teller']):
			speak('''A bank teller is responsible for assisting customers with routine banking transactions such as deposits, withdrawals, check cashing, and account inquiries. They also handle currency transactions, provide information on bank products and services, and ensure accuracy in all transactions''',True,True)
			return

		if isContain(text,['what is the purpose of a credit score']):
			speak('''A credit score is a numerical representation of an individual's creditworthiness. It helps lenders assess the likelihood of a borrower repaying debts based on their credit history. A higher credit score indicates lower credit risk, making it easier to obtain loans, credit cards, and favorable interest rates''',True,True)
			return

		if isContain(text,['what are the types of electronic payment systems']):
			speak('''There are several types of electronic payment systems, including credit and debit cards, mobile wallets, online banking transfers, automated clearinghouse (ACH) payments, and digital payment platforms such as PayPal, Venmo, and Google Pay''',True,True)
			return

		if isContain(text,['what is the purpose of a bank statement']):
			speak('''A bank statement is a summary of all transactions made in a bank account over a specific period. It provides an overview of deposits, withdrawals, cleared checks, fees, and other charges. Bank statements are essential for reconciling account balances, tracking expenses, and verifying transactions''',True,True)
			return

		if isContain(text,['What is the role of the fdic']):
			speak('''The FDIC is a government agency that provides deposit insurance to depositors in U.S. banks. Its primary role is to protect depositors' funds in the event of a bank failure, ensuring that customers are reimbursed up to the insured limit, currently set at $250,000 per depositor per bank''',True,True)
			return

		if isContain(text,['how can i prevent identity theft']):
			speak('''To prevent identity theft, you should safeguard personal information such as Social Security numbers, bank account details, and passwords. Be cautious of phishing attempts, regularly monitor your financial accounts, use strong passwords, update your computer's security software, and shred sensitive documents before disposing of them''',True,True)
			return

		if isContain(text,['what is the purpose of a cashiers check']):
			speak('''A cashier's check is a secure form of payment that guarantees the funds are available. It is often used for large transactions where a personal check or cash is not practical, such as purchasing a vehicle or making a substantial down payment''',True,True)
			return

		if isContain(text,['how can i protect my debit card from unauthorized use']):
			speak('''To protect your debit card from unauthorized use, you should keep it in a safe place, avoid sharing your PIN with anyone, regularly monitor your account for suspicious activity, and immediately report any lost or stolen cards to your bank''',True,True)
			return

		if isContain(text,['what is the difference between a credit union and a bank']):
			speak('''While both credit unions and banks offer financial services, credit unions are member-owned cooperatives that typically focus on serving specific communities or groups. Banks, on the other hand, are for-profit institutions owned by shareholders''',True,True)
			return

		if isContain(text,['what is the purpose of a bank reconciliation']):
			speak('''Bank reconciliation is the process of comparing your bank statement with your own records to ensure they match. It helps identify any discrepancies, such as missing transactions or errors, and ensures that your account balance is accurate''',True,True)
			return

		if isContain(text,['what are the advantages of using mobile banking apps']):
			speak('''Mobile banking apps offer convenience and accessibility, allowing you to check account balances, transfer funds, pay bills, deposit checks, and manage your finances on the go, using your smartphone or tablet''',True,True)
			return

		if isContain(text,['what is the role of a bank loan officer']):
			speak('''A bank loan officer is responsible for evaluating loan applications, assessing the creditworthiness of borrowers, determining loan terms and interest rates, and assisting customers throughout the loan application process''',True,True)
			return

		if isContain(text,['what is a joint account']):
			speak('''A joint account is a bank account shared by two or more individuals. Each account holder has equal access to the funds and can make deposits, withdrawals, and other transactions''',True,True)
			return


		if isContain(text,['who made this chatbot']):
			speak('''This chatbot is made by Suyog, Tanmay and Vedant''',True,True)
			return
			
		if isContain(text,['customer 101']):
			speak('''Bank ID: 101
                Name: Suyog Dhote
                Savings Balance: 50,000
                Loan: 1,00,000
                Mobile number: 9975896597
                Address: Bansi Nagar,Nagpur,440022''',True,True)
			return

		if isContain(text,['customer 102']):
			speak('''Bank ID: 102
                Name: Tanmay Mandlik
                Savings Balance: 79,000
                Loan: 1,50,000
                Mobile number: 9823459190
                Address: Bapu Nagar,Nagpur,440021''',True,True)
			return

		if isContain(text,['customer 103']):
			speak('''Bank ID: 103
                Name: Vedant Patil
                Savings Balance: 45,000
                Loan: 2,00,000
                Mobile number: 9623977183
                Address: Shatabdi Square,Nagpur,440021''',True,True)
			return

		if isContain(text,['customer 104']):
			speak('''Bank ID: 104
                Name: Komal Kadam
                Savings Balance: 1,00,000
                Loan: nil
                Mobile number: 7781345610
                Address: Main road,Ramtek,Nagpur,440016''',True,True)
			return

		if isContain(text, ['morning','evening','noon']) and 'good' in text:
			speak(normalChat.chat("good"), True, True)
			return
			
		
		result = normalChat.reply(text)
		if result != "None": speak(result, True, True)
		else:
			speak("I couldn't understand your query... ", True, True)
			#speak("Here's what I found on the web... ", True, True)
			#webScrapping.googleSearch(text) #uncomment this if you want to show the result on web, means if nothing found
		

##################################### DELETE USER ACCOUNT #########################################
def deleteUserData():
	result = messagebox.askquestion('Alert', 'Are you sure you want to exit ?')
	if result=='no': return
	root.destroy()
						#####################
						####### GUI #########
						#####################

############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########
def attachTOframe(text,bot=False):
	if bot:
		botchat = Label(chat_frame,text=text, bg=botChatTextBg, fg=botChatText, justify=LEFT, wraplength=250, font=('Montserrat',12, 'bold'))
		botchat.pack(anchor='w',ipadx=5,ipady=5,pady=5)
	else:
		userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white', justify=RIGHT, wraplength=250, font=('Montserrat',12, 'bold'))
		userchat.pack(anchor='e',ipadx=2,ipady=2,pady=5)

def clearChatScreen():
	for wid in chat_frame.winfo_children():
		wid.destroy()

### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
	frame.tkraise()
	clearChatScreen()

################# SHOWING DOWNLOADED IMAGES ###############
img0, img1, img2, img3, img4 = None, None, None, None, None
def showSingleImage(type, data=None):
	global img0, img1, img2, img3, img4
	try:
		img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((90,110), Image.ANTIALIAS))
	except:
		pass
	img1 = ImageTk.PhotoImage(Image.open('extrafiles/images/heads.jpg').resize((220,200), Image.ANTIALIAS))
	img2 = ImageTk.PhotoImage(Image.open('extrafiles/images/tails.jpg').resize((220,200), Image.ANTIALIAS))
	img4 = ImageTk.PhotoImage(Image.open('extrafiles/images/WeatherImage.png'))

	if type=="weather":
		weather = Frame(chat_frame)
		weather.pack(anchor='w')
		Label(weather, image=img4, bg=chatBgColor).pack()
		Label(weather, text=data[0], font=('Arial Bold', 45), fg='white', bg='#3F48CC').place(x=65,y=45)
		Label(weather, text=data[1], font=('Montserrat', 15), fg='white', bg='#3F48CC').place(x=78,y=110)
		Label(weather, text=data[2], font=('Montserrat', 10), fg='white', bg='#3F48CC').place(x=78,y=140)
		Label(weather, text=data[3], font=('Arial Bold', 12), fg='white', bg='#3F48CC').place(x=60,y=160)

	elif type=="wiki":
		Label(chat_frame, image=img0, bg='#EAEAEA').pack(anchor='w')
	elif type=="head":
		Label(chat_frame, image=img1, bg='#EAEAEA').pack(anchor='w')
	elif type=="tail":
		Label(chat_frame, image=img2, bg='#EAEAEA').pack(anchor='w')
	else:
		img3 = ImageTk.PhotoImage(Image.open('extrafiles/images/dice/'+type+'.jpg').resize((200,200), Image.ANTIALIAS))
		Label(chat_frame, image=img3, bg='#EAEAEA').pack(anchor='w')
	
def showImages(query):
	global img0, img1, img2, img3
	webScrapping.downloadImage(query)
	w, h = 150, 110
	#Showing Images
	imageContainer = Frame(chat_frame, bg='#EAEAEA')
	imageContainer.pack(anchor='w')
	#loading images
	img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((w,h), Image.ANTIALIAS))
	img1 = ImageTk.PhotoImage(Image.open('Downloads/1.jpg').resize((w,h), Image.ANTIALIAS))
	img2 = ImageTk.PhotoImage(Image.open('Downloads/2.jpg').resize((w,h), Image.ANTIALIAS))
	img3 = ImageTk.PhotoImage(Image.open('Downloads/3.jpg').resize((w,h), Image.ANTIALIAS))
	#Displaying
	Label(imageContainer, image=img0, bg='#EAEAEA').grid(row=0, column=0)
	Label(imageContainer, image=img1, bg='#EAEAEA').grid(row=0, column=1)
	Label(imageContainer, image=img2, bg='#EAEAEA').grid(row=1, column=0)
	Label(imageContainer, image=img3, bg='#EAEAEA').grid(row=1, column=1)


############################# WAEM - WhatsApp Email ##################################
def sendWAEM():
	global rec_phoneno, rec_email
	data = WAEMEntry.get()
	rec_email, rec_phoneno = data, data
	WAEMEntry.delete(0, END)
	appControl.Win_Opt('close')
def send(e):
	sendWAEM()

def WAEMPOPUP(Service='None', rec='Reciever'):
	global WAEMEntry
	PopUProot = Tk()
	PopUProot.title(f'{Service} Service')
	PopUProot.configure(bg='white')

	if Service=="WhatsApp": PopUProot.iconbitmap("extrafiles/images/whatsapp.ico")
	else: PopUProot.iconbitmap("extrafiles/images/email.ico")
	w_width, w_height = 410, 200
	s_width, s_height = PopUProot.winfo_screenwidth(), PopUProot.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	PopUProot.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	Label(PopUProot, text=f'Reciever {rec}', font=('Arial', 16), bg='white').pack(pady=(20, 10))
	WAEMEntry = Entry(PopUProot, bd=10, relief=FLAT, font=('Arial', 12), justify='center', bg='#DCDCDC', width=30)
	WAEMEntry.pack()
	WAEMEntry.focus()

	SendBtn = Button(PopUProot, text='Send', font=('Arial', 12), relief=FLAT, bg='#14A769', fg='white', command=sendWAEM)
	SendBtn.pack(pady=20, ipadx=10)
	PopUProot.bind('<Return>', send)
	PopUProot.mainloop()

######################## CHANGING CHAT BACKGROUND COLOR #########################
def getChatColor():
	global chatBgColor
	myColor = colorchooser.askcolor()
	if myColor[1] is None: return
	chatBgColor = myColor[1]
	colorbar['bg'] = chatBgColor
	chat_frame['bg'] = chatBgColor
	root1['bg'] = chatBgColor
	ChangeSettings(True)

chatMode = 1
def changeChatMode():
	global chatMode
	if chatMode==1:
		appControl.volumeControl('mute')
		VoiceModeFrame.pack_forget()
		TextModeFrame.pack(fill=BOTH)
		UserField.focus()
		chatMode=0
	else:
		appControl.volumeControl('full')
		TextModeFrame.pack_forget()
		VoiceModeFrame.pack(fill=BOTH)
		root.focus()
		chatMode=1

#####################################  MAIN GUI ####################################################

#### SPLASH/LOADING SCREEN ####
def progressbar():
	s = ttk.Style()
	s.theme_use('clam')
	s.configure("white.Horizontal.TProgressbar", foreground='white', background='#778899')
	progress_bar = ttk.Progressbar(splash_root,style="white.Horizontal.TProgressbar", orient="horizontal",mode="determinate", length=303) 
	progress_bar.pack()
	splash_root.update()
	progress_bar['value'] = 0
	splash_root.update()
 
	while progress_bar['value'] < 100:
		progress_bar['value'] += 5
		# splash_percentage_label['text'] = str(progress_bar['value']) + ' %'
		splash_root.update()
		sleep(0.1)

def destroySplash():
	splash_root.destroy()

if __name__ == '__main__':
	splash_root = Tk()
	splash_root.configure(bg='#778899')
	splash_root.overrideredirect(True)
	splash_label = Label(splash_root, text="Processing...", font=('montserrat',15),bg='#778899',fg='white')
	splash_label.pack(pady=40)
	# splash_percentage_label = Label(splash_root, text="0 %", font=('montserrat',15),bg='#3895d3',fg='white')
	# splash_percentage_label.pack(pady=(0,10))

	w_width, w_height = 400, 200
	s_width, s_height = splash_root.winfo_screenwidth(), splash_root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	splash_root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30))

	progressbar()
	splash_root.after(10, destroySplash)
	splash_root.mainloop()	

	root = Tk()
	root.title('S.A.M.')
	w_width, w_height = 400, 650
	s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	root.configure(bg=background)
	# root.resizable(width=False, height=False)
	root.pack_propagate(0)

	root1 = Frame(root, bg=chatBgColor)
	root2 = Frame(root, bg=background)
	root3 = Frame(root, bg=background)

	for f in (root1, root2, root3):
		f.grid(row=0, column=0, sticky='news')	
	
	################################
	########  CHAT SCREEN  #########
	################################

	#Chat Frame
	chat_frame = Frame(root1, width=380,height=551,bg=chatBgColor)
	chat_frame.pack(padx=10)
	chat_frame.pack_propagate(0)

	bottomFrame1 = Frame(root1, bg='#ccc', height=100)
	bottomFrame1.pack(fill=X, side=BOTTOM)
	VoiceModeFrame = Frame(bottomFrame1, bg='#ccc')
	VoiceModeFrame.pack(fill=BOTH)
	TextModeFrame = Frame(bottomFrame1, bg='#ccc')
	TextModeFrame.pack(fill=BOTH)

	# VoiceModeFrame.pack_forget()
	TextModeFrame.pack_forget()

	cblLightImg = PhotoImage(file='extrafiles/images/centralButton.png')
	cblDarkImg = PhotoImage(file='extrafiles/images/centralButton1.png')
	if KCS_IMG==1: cblimage=cblDarkImg
	else: cblimage=cblLightImg
	cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#ccc')
	cbl.pack(pady=17)
	AITaskStatusLbl = Label(VoiceModeFrame, text='    Offline', fg='white', bg=AITaskStatusLblBG, font=('montserrat', 16))
	AITaskStatusLbl.place(x=140,y=32)
	
	#Settings Button
	sphLight = PhotoImage(file = "extrafiles/images/setting.png")
	sphLight = sphLight.subsample(2,2)
	sphDark = PhotoImage(file = "extrafiles/images/setting1.png")
	sphDark = sphDark.subsample(2,2)
	if KCS_IMG==1: sphimage=sphDark
	else: sphimage=sphLight
	settingBtn = Button(VoiceModeFrame,image=sphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf",command=lambda: raise_frame(root2))
	settingBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Keyboard Button
	kbphLight = PhotoImage(file = "extrafiles/images/keyboard.png")
	kbphLight = kbphLight.subsample(2,2)
	kbphDark = PhotoImage(file = "extrafiles/images/keyboard1.png")
	kbphDark = kbphDark.subsample(2,2)
	if KCS_IMG==1: kbphimage=kbphDark
	else: kbphimage=kbphLight
	kbBtn = Button(VoiceModeFrame,image=kbphimage,height=30,width=30, bg='#ccc',borderwidth=0,activebackground="#ccc", command=changeChatMode)
	kbBtn.place(x=25, y=30)

	#Mic
	micImg = PhotoImage(file = "extrafiles/images/mic.png")
	micImg = micImg.subsample(2,2)
	micBtn = Button(TextModeFrame,image=micImg,height=30,width=30, bg='#ccc',borderwidth=0,activebackground="#ccc", command=changeChatMode)
	micBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Text Field
	TextFieldImg = PhotoImage(file='extrafiles/images/textField.png')
	UserFieldLBL = Label(TextModeFrame, fg='white', image=TextFieldImg, bg='#ccc')
	UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
	UserField = Entry(TextModeFrame, fg='white', bg='#203647', font=('Montserrat', 16), bd=6, width=22, relief=FLAT)
	UserField.place(x=20, y=30)
	UserField.insert(0, "Ask me anything...")
	UserField.bind('<Return>', keyboardInput)
	
	#User and Bot Icon
	userIcon = PhotoImage(file="extrafiles/images/avatars/ChatIcons/a"+str(ownerPhoto)+".png")
	botIcon = PhotoImage(file="extrafiles/images/assistant2.png")
	botIcon = botIcon.subsample(2,2)
	

	###########################
	########  SETTINGS  #######
	###########################

	settingsLbl = Label(root2, text='Settings', font=('Arial Bold', 15), bg=background, fg=textColor)
	settingsLbl.pack(pady=10)
	separator = ttk.Separator(root2, orient='horizontal')
	separator.pack(fill=X)
	#User Photo
	userProfileImg = Image.open("extrafiles/images/avatars/a"+str(ownerPhoto)+".png")
	userProfileImg = ImageTk.PhotoImage(userProfileImg.resize((120, 120)))
	userPhoto = Button(root2, image=userProfileImg, bg=background, bd=0, relief=FLAT, activebackground=background)
	userPhoto.pack(pady=(20, 5))

	#Username
	userName = Label(root2, text=ownerName, font=('Arial Bold', 15), fg=textColor, bg=background)
	userName.pack()

	#Settings Frame
	settingsFrame = Frame(root2, width=300, height=300, bg=background)
	settingsFrame.pack(pady=20)

	assLbl = Label(settingsFrame, text='Assistant Voice', font=('Arial', 13), fg=textColor, bg=background)
	assLbl.place(x=0, y=20)
	n = StringVar()
	assVoiceOption = ttk.Combobox(settingsFrame, values=('Female', 'Male'), font=('Arial', 13), width=13, textvariable=n)
	assVoiceOption.current(voice_id)
	assVoiceOption.place(x=150, y=20)
	assVoiceOption.bind('<<ComboboxSelected>>', changeVoice)

	voiceRateLbl = Label(settingsFrame, text='Voice Rate', font=('Arial', 13), fg=textColor, bg=background)
	voiceRateLbl.place(x=0, y=60)
	n2 = StringVar()
	voiceOption = ttk.Combobox(settingsFrame, font=('Arial', 13), width=13, textvariable=n2)
	voiceOption['values'] = ('Very Low', 'Low', 'Normal', 'Fast', 'Very Fast')
	voiceOption.current(ass_voiceRate//50-2) #100 150 200 250 300
	voiceOption.place(x=150, y=60)
	voiceOption.bind('<<ComboboxSelected>>', changeVoiceRate)
	
	volumeLbl = Label(settingsFrame, text='Volume', font=('Arial', 13), fg=textColor, bg=background)
	volumeLbl.place(x=0, y=105)
	volumeBar = Scale(settingsFrame, bg=background, fg=textColor, sliderlength=30, length=135, width=16, highlightbackground=background, orient='horizontal', from_=0, to=100, command=changeVolume)
	volumeBar.set(int(ass_volume*100))
	volumeBar.place(x=150, y=85)



	themeLbl = Label(settingsFrame, text='Theme', font=('Arial', 13), fg=textColor, bg=background)
	themeLbl.place(x=0,y=143)
	themeValue = IntVar()
	s = ttk.Style()
	s.configure('Wild.TRadiobutton', font=('Arial Bold', 10), background=background, foreground=textColor, focuscolor=s.configure(".")["background"])
	darkBtn = ttk.Radiobutton(settingsFrame, text='Dark', value=1, variable=themeValue, style='Wild.TRadiobutton', command=changeTheme, takefocus=False)
	darkBtn.place(x=150,y=145)
	lightBtn = ttk.Radiobutton(settingsFrame, text='Light', value=2, variable=themeValue, style='Wild.TRadiobutton', command=changeTheme, takefocus=False)
	lightBtn.place(x=230,y=145)
	themeValue.set(1)
	if KCS_IMG==0: themeValue.set(2)


	chooseChatLbl = Label(settingsFrame, text='Chat Background', font=('Arial', 13), fg=textColor, bg=background)
	chooseChatLbl.place(x=0,y=180)
	cimg = PhotoImage(file = "extrafiles/images/colorchooser.png")
	cimg = cimg.subsample(3,3)
	colorbar = Label(settingsFrame, bd=3, width=18, height=1, bg=chatBgColor)
	colorbar.place(x=150, y=180)
	if KCS_IMG==0: colorbar['bg'] = '#E8EBEF'
	Button(settingsFrame, image=cimg, relief=FLAT, command=getChatColor).place(x=261, y=180)

	backBtn = Button(settingsFrame, text='   Back   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=lambda:raise_frame(root1))
	clearFaceBtn = Button(settingsFrame, text='   Close the ChatBot   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=deleteUserData)
	backBtn.place(x=5, y=250)
	clearFaceBtn.place(x=120, y=250)

	try:
		# pass
		Thread(target=voiceMedium).start()
	except:
		pass
	try:
		# pass
		Thread(target=webScrapping.dataUpdate).start()
	except Exception as e:
		print('System is Offline...')
	
	root.iconbitmap('extrafiles/images/assistant2.ico')
	raise_frame(root1)
	root.mainloop()