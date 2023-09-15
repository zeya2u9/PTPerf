from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from xvfbwrapper import Xvfb
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import pandas as pd
import codecs
import subprocess
from subprocess import run
import sys
import keyboard
import stem.control
import atexit

def all_done():
	print('Killing Display')
	os.system("kill -9 $(ps aux | grep '[X]vfb' | awk '{print $2}')")

print('Registering')
atexit.register(all_done)
print('Registered')

#sys.path.append("/")
#from tor_config import conf

## Tor config parameters
conf = {}

conf["__DisablePredictedCircuits"] =  "1"
conf["__LeaveStreamsUnattached"]   =  "1"

conf["MaxClientCircuitsPending"]   =  "1"
conf["MaxCircuitDirtiness"]        =  "999999999"
conf["NewCircuitPeriod"]           =  "999999999"

static_m = '9171E15EBF665768F8EFAE2271D47D922C4EED46'
static_e = '776542D611661D6FE3839FE2D7AFB92A435C5D81'

# TODO
# hope for the best
######## STEM ##################################################################################

#getting all relay information
def get_circuitCount(port):
	with stem.control.Controller.from_port(port=port) as controller:
		controller.authenticate()

		circuits = controller.get_circuits()
		cids = list(map(lambda c: c.id, circuits))
		count = len(cids)
	return count

def get_relay_info(port):
	with stem.control.Controller.from_port(port=port) as controller:
		controller.authenticate()

		global relay_fingerprints
		global count, count1, relay_guard, relay_exits
		
		relay_fingerprints = [desc.fingerprint for desc in controller.get_network_statuses()]

		count = 0
		count1 = 0
		relay_exits = ['']*7000
		relay_guard = ['']*7000
		for relay in relay_fingerprints:
			info = controller.get_info('ns/id/'+relay)
			if info.find('Exit')>-1:
				relay_exits[count] = relay
				count = count + 1  
				print(f"Exit Relay: {info} \n {count}")
			elif info.find('Guard')>-1:
				relay_guard[count1] = relay
				count1 = count1 + 1  
				print(f"Exit Relay: {info} \n {count1}")

		print(f"Total relays: {len(relay_fingerprints)}")
		print(f"Total exit relays: {count}")
		print(f"Total guard relays: {count1}")
		print(f"Total exclusive middle relay: {len(relay_fingerprints) - (count+count1)}")

def new_circuit(g, m, e, port):
	with stem.control.Controller.from_port(port = port) as controller:
		controller.authenticate()

		#sys.path.append("/")
		#from tor_config import conf
		print("[stem] Setting required Tor config.")
		for key, val in conf.items():
			controller.set_conf(key, val)

		#killing all previous circuits
		circuits = controller.get_circuits()
		cids = list(map(lambda c: c.id, circuits))
		if len(cids) == 0:
			print("No circuits to close!!")
		else:
			map(controller.close_circuit, cids)
			print("[stem {}] Closed Circuit(s):".format(port), *cids)
			for cid in cids:
				controller.close_circuit(cid)

		#making a new circuit
		try:
			circuit_id = controller.new_circuit([g, m, e], await_build = True)
			print(f"New circuit for {port}: {circuit_id}\n")
		except Exception as exc:
			print(f"%s %s => %s {g, m ,e}")
			return -1
		return int(circuit_id)
def get_middle_exit(port):
	relays = ['']*3
	with stem.control.Controller.from_port(port = port) as controller:
		controller.authenticate()
		#kill all existing circuits
		circuits = controller.get_circuits()
		cids = list(map(lambda c: c.id, circuits))
		if len(cids) == 0:
			print("No circuits to close!!")
		else:
			map(controller.close_circuit, cids)
			print("[stem {}] Closed Circuit(s):".format(port), *cids)
			for cid in cids:
				controller.close_circuit(cid)

		#execute curl to force tor to make a new circuit and fetch its middle and exit
		try:
			os.system("curl --socks5 127.0.0.1:8050 -o /dev/null https://www.wikipedia.org/")
			circuits = controller.get_circuits()
			for circ in circuits:
				count = 0
				for i, entry in enumerate(circ.path):
					relays[count] = entry[0]
					count = count + 1
				return relays[1], relays[2]
		except:
			return  static_m, static_e

######## METADATA ################################################################################
#tor - 0
paths_0 = ''
pathc_0 = 'tor -f /etc/tor/torrc-basic &'

#obfs4 - 1
paths_1 = ''
pathc_1 = 'tor -f /etc/tor/obfs4_torrc &'

#marionette - 2
paths_2 = "sshpass -p <server-pass> ssh root@<server-ip> './marionette/start2.sh'"
pathc_2 = './pt_mar.sh'

#shadowsocks - 3
paths_3 = "sshpass -p <server-pass> ssh root@<server-ip>  '/usr/bin/ss-server -c /etc/shadowsocks-libev/config.json &'"
pathc_3 = './start_3.sh'

#stegotorus - 4
paths_4 = "sshpass -p <server-pass> ssh root@<server-ip> './stegotorus/startn.sh'"
pathc_4 = f'cd {os.getenv("HOME")}/stegotorus/; ./stegotorus --log-min-severity=debug --timestamp-logs chop client --passphrase "correct passphrase" --trace-packets --disable-retransmit 12>

#Cloak - 5
paths_5 = "sshpass -p <server-pass> ssh root@<server-ip> 'cd /root/pTesting/Cloak/ && { tor -f /etc/tor/torrc-basic & build/ck-server -c ckserver.json; } &'"
pathc_5 = f"cd {os.getenv('HOME')}/Cloak/ && build/ck-client -c ckclient.json -s <server-ip> &"

#Snowflake - 6
paths_6 = ''
pathc_6 = 'tor -f /etc/tor/snowflake_client_torrc_mod &'

#Meek - 7
paths_7 = ''  #server-side
pathc_7 = 'cd /root/meek/meek-client/; tor -f /etc/tor/meek_torrc &' #client-side

#Camoufler - 8
paths_8 = 'cd /root/file_download_tg_socks-main/; ./start_camo.sh'
pathc_8 = 'echo Done'

#Dnstt - 9
paths_9 = 'echo "Done"'
pathc_9 = './start_9.sh'

#MassBrowser - 10
paths_10 = './start_10.sh'
pathc_10 = 'echo "Done"'

#Psiphon - 11
paths_11 = ''
pathc_11 = './start_11.sh'

#Conjure - 12
paths_12 = ''
pathc_12 = 'cd /root/conjure/client/; tor -f torrc &'

#Webtunnel - 13
paths_13 = "sshpass -p <server-pass> ssh root@<server-ip>  'systemctl restart nginx.service; systemctl restart webTunnel.service '"
pathc_13 = 'cd /root/webtunnel/main/client/; tor -f /etc/tor/torrc-webtunnel2 &'


startups = {
	0 : [paths_0, pathc_0],
	1 : [paths_1, pathc_1],
	2 : [paths_2, pathc_2],
	3 : [paths_3, pathc_3],
	4 : [paths_4, pathc_4],
	5 : [paths_5, pathc_5],
	6 : [paths_6, pathc_6],
	7 : [paths_7, pathc_7],
	8 : [paths_8, pathc_8],
	9 : [paths_9, pathc_9],
	10: [paths_10, pathc_10],
        11: [paths_11, pathc_11],
        12: [paths_12, pathc_12],
        13: [paths_13, pathc_13]

}

pt_names = {
    0 : "tor",
    1 : "obfs4",
    2 : "marionette",
    3 : "shadowsocks",
    4 : "stegotorus",
    5 : "cloak",
    6 : "snowflake",
    7 : "meek",
    8 : "camoufler",
    9 : "dnstt",
    10: "massbrowser",
    11: "psiphon",
    12: "conjure",
    13: "webtunnel"
}

pt_protocol = ['socks5', 'socks5', 'socks4a', 'socks5', 'socks4', 'socks5', 'socks5', 'socks5', 'socks5', 'socks5', 'socks5h', 'socks5', 'socks5', 'socks5']
pt_ports = ['9050', '9050', '8079', '9050', '5001', '1984', '9050', '9050', '9011', '9050', '9050', '9050', '9050', '9050']

##################################################################################################

def get_clear_browsing_button(driver):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver, timeout=60):
    """Clear the cookies and cache for the ChromeDriver instance."""
    # navigate to the settings page
    driver.get('chrome://settings/clearBrowserData')

    # wait for the button to appear
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)

    # click the button to clear the cache
    get_clear_browsing_button(driver).click()

    # wait for the button to be gone before returning
    wait.until_not(get_clear_browsing_button)

def setup_selenium(pt_num):

	try:
		chrome_options = Options()
		chrome_options.add_argument(f'--proxy-server={pt_protocol[pt_num]}://127.0.0.1:{pt_ports[pt_num]}')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--ignore-certificate-errors')
		chrome_options.add_argument("--disable-gpu")
		chrome_options.add_argument("--incognito")
		chrome_options.add_argument("--headless=chrome")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--remote-debugging-port=9222")
		#chrome_options.add_experimental_option("prefs", {"download.default_directory" : "/root/autoScript/"})
		chrome_options.add_extension(os.getenv('HOME') + "/selenium_testing/uBlock.crx")
		print('DOING')
		browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
		print('DONE!!!')
		browser.set_page_load_timeout(120)
		#browser.implicitly_wait(60)  ##newly added

		time.sleep(3)
		return browser
	except:
		browser.quit()
		print('CRY ABT IT')
		raise(e)


def testWebsite(website, iteration, pt_num, browser, port):
	start = time.time()
	try:
		browser.get(website)
	except Exception as e:
		print(e)
	end = time.time()
	time_taken = (end-start)
	n=os.path.join(f"{os.getenv('HOME')}/autoScript/","Page.html")
	f = codecs.open(n, "w", "utf−8")
	h = browser.page_source
	f.write(h)

	os.system(f"echo {website} >> n-trf-tr{pt_num}.txt")
	result = "Dl Size (Bits): " + str((run("ls -l Page.html".split(), capture_output=True).stdout)).split()[4] + " Time_Taken = " + str(time_taken) + " circuitCount = " + str(get_circuitCount(port))
	os.system(f'''echo "{result}" >> n-trf-tr{pt_num}.txt''')

	os.system("rm Page.html")
	return result


def initialiseSeleniumForPT(pt_num):
	#server
	
	if pt_num == 13:
		os.system(f"{startups[pt_num][0]}" + '&')
		time.sleep(5)
		
	if pt_num == 13:
		print('webtunnel is starting')
		time.sleep(15)
	#client
	if pt_num == 13:
		os.system(f"{startups[pt_num][1]}")
		time.sleep(10)

	if pt_num == 7:
		print('Meek takes time in bootstrapping::\n')
		time.sleep(40)



def cleanupPT(pt_num, browser):
	#os.system(f"{os.getenv('HOME')}/autoScript/kill_{pt_num}.sh")
	if pt_num == 13:
		os.system("kill -9 $(ps aux | grep '[t]orrc-webtunnel2' | awk '{print $2}')")
		os.system("sshpass -p pT@123pt ssh root@139.59.17.150 'systemctl stop webTunnel.service'")
		os.system("sshpass -p pT@123pt ssh root@139.59.17.150 'systemctl stop nginx.service'")
	browser.quit()
def cleanupPT13(pt_num):
	os.system("kill -9 $(ps aux | grep '[t]orrc-webtunnel2' | awk '{print $2}')")
	os.system("sshpass -p pT@123pt ssh root@139.59.17.150 'systemctl stop webTunnel.service'")
	os.system("sshpass -p pT@123pt ssh root@139.59.17.150 'systemctl stop nginx.service'")
	#starting again 
	initialiseSeleniumForPT(pt_num)



if __name__ == "__main__":
	#do stuff
	our_node = '633166A26D5E533973DEEB8BDEA78AEAC63B334B'
	obfs4_node = '2C7A6652D5C5877227608FEEF89462578BD5B5C8'
	webTunnel_node = '3C24EAEDEB4618B5DCD3EBE500324AB2598FB2FD'
	middle =  ['8358BDDA9C9A680B4E3A2809E5C24F5B3624D5C2','8E98732FE1959764937C92CB2A5C89D52E6AA6B3', '874D84382C892F3F61CC9E106BF08843DE0B865A', '5C124A27FFD658CB76165718DABFFD4093F5C827']
	exit =  ['C51579E3A6611562DDF28FC67CCD16EE5E05717F', '64EEA511984F2C862F09E77755DC657EC31E6483', 'FDCFEA18CC64461455DE5EA3FC31834C6B42FEC7', '615ABEA2DE76EB3760BC51E7306BAA59F15CD8F2']
	#G_10relays = ['0040A5B04C7E309D37CBE7EDB2B72D3E15D057C1', '006AE565CA934C6EE5E82FC64008D61426E8C317','00B57BF614F7ED3051073B5D4526FF0B23AF217B', '00C2B794F74B8759D26786EE363009C9C59088F5','00D2CE3C2153EA09786F2105F26B138CF759424F', '00E1649E69FF91D7F01E74A5E62EF14F7D9915E4',  '010C315D4E7CA71687C0102C0CBF6F8FAD0F804D', '0136696B025AC5503847D736FE9F3D65EB27A596','01759BAA5DE5FA19E36FADAF7D9BC64C15573ABC', '017B08CC163424CD6ABA4ADD4042B4174D494732']
	G_10relays = ['1AA63474AB2277A944E452649EB19044F21314E4', '1B0CCDBADAFF988E92C20EE4A51FF2D13C33B77D', 
	              '1B7F47827E2FFAFE05B92B1C5A92B8F9A4AF67DD', '1BA2F9436C0018A4B52625D071B72F648522B748', 
	              '1BD6462B856754E9C826B220B4C47E59D0479109', '1C0736CF3744A3B87C2D2269B8BD3388C7E60552', 
	              '1C53F213C9BBAB2EB39015DD5A1BC89CE152A0F7', '1C5FCA222C6BC297424AAA0E6C9769C98C3F27BF', 
	              '1C7C6841D0B7F10B72608DD37F992F186AFB5342', '1D3894E248CF8DAB1B22BE9835797931548DC06C']

	if os.getcwd() != os.getenv('HOME')+'/autoScript':
		print("Please run the script from autoScript folder...")
		quit()

	if len(sys.argv) < 2:
		print('run this script in the following format:')
		print('python3 selenium_curl.py <type of experiment>')
		print('types: tranco-500, blocked-200')
		quit()
	else:
		mode = sys.argv[1]

	data20 = pd.read_csv(os.getenv('HOME') + '/autoScript/websiteList/tranco/tranco_bas_krdo.csv')
	website_tr20 = data20.iloc[0:1000,0]
	#website_tr20 = [ 'https://104.248.52.'   ]  #'https://www.youtube.com/', 'https://www.nytimes.com/', 'https://www.wikipedia.org/', 'https://www.spotify.com/', 'https://104.248.52.118/']
	#website_tr20 = ['https://147.182.134.83/5MB.zip']
	#website_tr20 = ['https://www.wikipedia.org/']

	data3 = pd.read_csv(os.getenv('HOME') + '/autoScript/websiteList/url-lists/1000-websites.csv')
	website_url = data3.iloc[0:10,0]

	websites = website_tr20 if mode == 'tranco-500' else website_url
	#os.system("sshpass -p pT@123pt ssh root@139.59.17.150 'systemctl stop webTunnel.service'")
	#os.system("sshpass -p pT@123pt ssh root@139.59.17.150 'systemctl stop nginx.service'")

	os.system(f'mkdir {mode}')

	vdisplay = Xvfb()
	vdisplay.start()

	get_relay_info(9051)
	j = -1
	k = 0
	print("First 100 guards",relay_guard[250:270])
	for iteration in range(5):

		print(f"############  ITERATIION {iteration}  ############")
		os.system(f"mkdir result_web{iteration+1}")

		initialiseSeleniumForPT(0)
		print('Initiating browser...\n\n')
		try:
			vdisplay = Xvfb()
			vdisplay.start()
			browser_instance1 = setup_selenium(0)
		except:
			os.system("kill -9 $(ps aux | grep '[X]vfb' | awk '{print $2}')")
			vdisplay.stop()
			exit(1)
		print('Initiated.\n\n')

		#cir_id = new_circuit(G_10relays[0], middle, exit, 9051)
		#os.system('truncate circuit_id.txt --size 0')
		#os.system(f'echo {cir_id} >> circuit_id.txt')


		for website in websites:
			for pt_num1 in range(4):
				#making circuit through ignoredChild2
				#m, e = get_middle_exit(8051)
				cir_id = new_circuit(G_10relays[0], middle[pt_num1], exit[pt_num1], 9051)
				cir = str(cir_id)

				print(f"New circuit : {cir_id} created through our fixed guard and middle-exit-indexd at:{pt_num1}")
				subprocess.Popen(["carml","stream","--attach",cir])
				print("--------------------------- __||__ taking a break of 5 seconds for carml to stabilize __||__ --------------------------")
				time.sleep(5)
				print("--------" + website + "--------")
				result1 = testWebsite(website, iteration, pt_num1, browser_instance1, 9051)

				os.system("kill $(ps aux | grep '[c]arml' | awk '{print $2}')")
				print(result1)

		os.system(f"mv n-trf-tr* result_web{iteration+1}/")
		print(f"\n\n{pt_names[pt_num1]} finished execution...\ncleaning up...\n\n")
		cleanupPT(0, browser_instance1)

	os.system(f'mv result_web* {mode}/')

	vdisplay.stop()

####################################################################################################################

# CODE GRAVE

# time for fetching (jugaadu)
'''
start = time.time()
browser.get("https://www.atlasobscura.com/articles/venice-traditional-bookbinding?utm_source=pocket-newtab-intl-en")
end = time.time()
print(end-start)
'''

# save a page
'''
n=os.path.join("/path/to/some/test/folder/","Page.html")
f = codecs.open(n, "w", "utf−8")
h = driver.page_source
file.write(h)
'''

# Socks5 Host SetUp:-
'''
profile = webdriver.FirefoxProfile()
myProxy = "127.0.0.1:9050"
ip, port = myProxy.split(':')
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', ip)
profile.set_preference('network.proxy.socks_port', int(port))

browser = webdriver.Firefox(firefox_profile=profile)
'''

# install extension
'''
browser.install_addon("/home/nsl400/.mozilla/firefox/y9sdrczm.default-release/extensions/uBlock0@raymondhill.net.xpi", temporary=True)
'''

# headless firefox
'''
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)
'''

# quirky stuff
'''
browser.maximise_window()
'''
