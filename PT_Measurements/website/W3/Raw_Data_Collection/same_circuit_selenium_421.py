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
from subprocess import run
import sys
import keyboard
import stem.control
#sys.path.append("/")
#from tor_config import conf

## Tor config parameters
conf = {}

conf["__DisablePredictedCircuits"] =  "1"
#conf["__LeaveStreamsUnattached"]   =  "1"

conf["MaxClientCircuitsPending"]   =  "1"
conf["MaxCircuitDirtiness"]        =  "999999999"
conf["NewCircuitPeriod"]           =  "999999999"


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
			for circ in circuits:
			     print(circ.path)
			     #for i, entry in enumerate(circ.path):
			     #	print(entry[0])

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

def print_circuits_used(port):
	with stem.control.Controller.from_port(port = port) as controller:
		controller.authenticate()
		circuits = controller.get_circuits()
		for circ in circuits:
			print("!!!!!!!!!!!!!!!!!!!!!!!!!!PRINT CIRCUIT USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			print(circ.path)


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
                        return -1, -1


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
pathc_4 = f'cd {os.getenv("HOME")}/stegotorus/; ./stegotorus --log-min-severity=debug --timestamp-logs chop client --passphrase "correct passphrase" --trace-packets --disable-retransmit 127.0.0.1:5001 nosteg_rr <server-ip>:5000 &'

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
paths_13 = '' 
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
pt_ports = ['8050', '9050', '8079', '9050', '5001', '1984', '9050', '9050', '9011', '9050', '9050', '9050', '9050', '7050']

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
	n=os.path.join(f"{os.getenv('HOME')}/","Page.html")
	f = codecs.open(n, "w", "utf−8")
	h = browser.page_source
	f.write(h)

	os.system(f"echo {website} >> n-trf-tr{pt_num}.txt")
	print_circuits_used(port)
	result = "Dl Size (Bits): " + str((run("ls -l Page.html".split(), capture_output=True).stdout)).split()[4] + " Time_Taken = " + str(time_taken) + " circuitCount = " + str(get_circuitCount(port))
	os.system(f'''echo "{result}" >> n-trf-tr{pt_num}.txt''')

	os.system("rm Page.html")
	return result


def initialiseSeleniumForPT(pt_num):
	#server
	if pt_num == 13:
		#os.system(f"{startups[pt_num][0]}" + '&')
		time.sleep(2)

	#client
	#if pt_num == 13:
	#	os.system(f"{startups[pt_num][1]}")
	#	time.sleep(10)

	if pt_num == 7:
		print('Meek takes time in bootstrapping::\n')
		time.sleep(40)



def cleanupPT(pt_num, browser):
	#os.system(f"{os.getenv('HOME')}/autoScript/kill_{pt_num}.sh")
	if pt_num == 13:
		os.system("kill -9 $(ps aux | grep '[t]orrc-webtunnel2' | awk '{print $2}')")
	browser.quit()
def cleanupPT13(pt_num):
	os.system("kill -9 $(ps aux | grep '[t]orrc-webtunnel2' | awk '{print $2}')")
	initialiseSeleniumForPT(pt_num)

if __name__ == "__main__":
	#do stuff
	our_node = '<your_Tor_guard_node_fingerprint>'
	obfs4_node = '<private-obfs4-server-fingerprint>'
	webTunnel_node = '<private-webTunnel-server-fingerprint>'
	if os.getcwd() != os.getenv('HOME')+'':
		print("Please run the script from home folder...")
		quit()

	if len(sys.argv) < 2:
		print('run this script in the following format:')
		print('python3 selenium_curl.py <type of experiment>')
		print('types: tranco, blocked')
		quit()
	else:
		mode = sys.argv[1]

	website_tr20 = ['https://www.youtube.com/', 'https://www.nytimes.com/', 'https://www.wikipedia.org/', 'https://www.spotify.com/', 'https://104.248.52.118/']

	websites = website_tr20 if mode == 'tranco' else website_url

	os.system(f'mkdir {mode}')

	vdisplay = Xvfb()
	vdisplay.start()

	get_relay_info(8051)
	j = -1
	k = 0
	for iteration in range(0,500):

		print(f"############  ITERATIION {iteration}  ############")
		os.system(f"mkdir result_web{iteration+1}")

		for pt_num1, pt_num2, pt_num3 in zip([0],[1],[13]):
			print(pt_num1)
			print(pt_num2)
			print(pt_num3)
			initialiseSeleniumForPT(pt_num1)
			initialiseSeleniumForPT(pt_num2)
			initialiseSeleniumForPT(pt_num3)
			print(f"\n\n{pt_names[pt_num1]}\n\n")
			print(f"\n\n{pt_names[pt_num2]}\n\n")
			print(f"\n\n{pt_names[pt_num3]}\n\n")

			for website in websites:
				time.sleep(2)
				#j = j + 1
				#while ((new_circuit(obfs4_node, relay_fingerprints[(j)%count1], relay_exits[(j)%count], 9051) < 0) or (new_circuit(our_node, relay_fingerprints[(j)%count1], relay_exits[(j)%count], 8051) < 0)) or (new_circuit(webTunnel_node, relay_fingerprints[(j)%count1], relay_exits[(j)%count], 7051) < 0):
				#	j = j + 1

				print("--------" + website + "--------")
				print('Initiating browser...\n\n')
				try:
					vdisplay = Xvfb()
					vdisplay.start()
					browser_instance1 = setup_selenium(pt_num1)
				except:
					vdisplay.stop()
					exit(1)
				print(f"Initiated {pt_names[pt_num1]}\n\n")

				m = -1
				e = -1
				while m == -1 or cir_id1 < 0:
					m, e = get_middle_exit(8051)
					try:
						cir_id1 = new_circuit(our_node, m, e, 8051)
					except:
						print("Could not make circuit through m,e:: trying new m,e")
				time.sleep(3)
				result1 = testWebsite(website, iteration, pt_num1, browser_instance1, 8051)
				print(result1)
				browser_instance1.quit()
				vdisplay.stop()

				print('Initiating browser...\n\n')
				
				try:
					vdisplay = Xvfb()
					vdisplay.start()
					browser_instance2 = setup_selenium(pt_num2)
				except:
					vdisplay.stop()
					exit(1)
				print(f"Initiated {pt_names[pt_num2]}\n\n")
				try:
					cir_id2 = new_circuit(obfs4_node, m, e, 9051)
				except:
					print("Could not make circuit through m,e:: ")
					#continue

				time.sleep(3)
				result2 = testWebsite(website, iteration, pt_num2, browser_instance2, 9051)
				print(result2)
				vdisplay.stop()

				browser_instance2.quit()
				print("----------------------------------------")
				print("\n\n")

				print('Initiating browser...\n\n')
				try:
					vdisplay = Xvfb()
					vdisplay.start()
					browser_instance3 = setup_selenium(pt_num3)
				except:
					vdisplay.stop()
					exit(1)
				print('Initiated.\n\n')
				print(f"Initiated {pt_names[pt_num3]}\n\n")
				try:
					cir_id3 = new_circuit(webTunnel_node, m, e, 7051)
				except:
					print("Could not make circuit through m,e:: ")
					#continue

				time.sleep(3)
				result3 = testWebsite(website, iteration, pt_num3, browser_instance3, 7051)
				print(result3)
				browser_instance3.quit()
				vdisplay.stop()

			os.system(f"mv n-trf-tr{pt_num1}.txt result_web{iteration+1}/")
			os.system(f"mv n-trf-tr{pt_num2}.txt result_web{iteration+1}/")
			os.system(f"mv n-trf-tr{pt_num3}.txt result_web{iteration+1}/")
			print(f"\n\n{pt_names[pt_num1]} finished execution...\ncleaning up...\n\n")

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
