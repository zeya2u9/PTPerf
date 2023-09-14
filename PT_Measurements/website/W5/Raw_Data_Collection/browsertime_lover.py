import time
import os
import pandas as pd
import codecs
from subprocess import run
import sys
import json

# TODO

######## METADATA ################################################################################
#obfs4 - 1
paths_0 = ''
pathc_0 = 'tor -f /etc/tor/torrc-basic &'

#obfs4 - 1
paths_1 = ''
pathc_1 = 'tor -f /etc/tor/obfs4_torrc &'

#marionette - 2
paths_2 = "sshpass -p <server-pass> ssh root@<server-ip> './marionette/start2.sh'"
pathc_2 = './pt_mar.sh'

#shadowsocks - 3
paths_3 = "sshpass -p <server-pass> ssh root@<server-ip> '/usr/bin/ss-server -c /etc/shadowsocks-libev/config.json &'"
pathc_3 = 'tor -f /etc/tor/torrc-shadow & /usr/bin/ss-local -c /etc/shadowsocks-libev/config.json &'

#stegotorus - 4
paths_4 = "sshpass -p <server-pass> ssh root@<server-ip> './stegotorus/startn.sh'"
pathc_4 = f'cd {os.getenv("HOME")}/stegotorus/; ./stegotorus --log-min-severity=debug --timestamp-logs chop client --passphrase "correct passphrase" --trace-packets --disable-retransmit 127.0.0.1:5001 nosteg_rr <server-ip>:5000 &'

#Cloak - 5
paths_5 = "sshpass -p <server-pass> ssh root@<server-ip> 'cd /root/Cloak/ && { tor -f /etc/tor/torrc-basic & build/ck-server -c ckserver.json; } &'"
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
paths_13 = "sshpass -p <server-pass> ssh root@<server-ip>  'systemctl restart webTunnel.service &'"
pathc_13 = 'cd /root/webtunnel/main/client/; tor -f /etc/tor/torrc-webtunnel &'


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


def setup_selenium(pt_num):

	try:
		chrome_options = Options()
		chrome_options.add_argument(f'--proxy-server={pt_protocol[pt_num]}://127.0.0.1:{pt_ports[pt_num]}')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument("--disable-gpu")
		chrome_options.add_argument("--headless=chrome")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--remote-debugging-port=9222")
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


def testWebsite(website, pt_num):

	os.system(f"rm -rdf {os.getenv('HOME')}/browsertime-results/")
	os.system(f'browsertime -n 5 --xvfb --chrome.args="--no-sandbox" --chrome.args="--proxy-server=socks5://127.0.0.1:{pt_ports[pt_num]}" --visualMetrics {website}')

	os.system(f"echo {website} >> n-trf-tr{pt_num}.txt")

	try:
		bt_output = json.load(open(f"{os.getenv('HOME')}/{(run('find . -name browsertime.json'.split(), capture_output=True).stdout).decode(encoding='utf-8')[2:-1]}"))

		median_val = bt_output[0]['statistics']['visualMetrics']['SpeedIndex']['median']
		mean_val = bt_output[0]['statistics']['visualMetrics']['SpeedIndex']['mean']
	except Exception as e:
		median_val = 0
		mean_val = 0

	result = "SpeedIndex (seconds): Median= " + str(median_val) + " Mean= " + str(mean_val)
	os.system(f'''echo "{result}" >> n-trf-tr{pt_num}.txt''')

	return result


def initialisePT(pt_num):
	os.system(f"{startups[pt_num][0]}" + '&')
	time.sleep(5)

	os.system(f"{startups[pt_num][1]}")
	time.sleep(20)

	if pt_num == 7 or pt_num == 6:
		print('Meek takes time in bootstrapping::\n')
		time.sleep(120)

	print(f'Initialised PT : {pt_names[pt_num]}')


def cleanupPT(pt_num):
	os.system(f"{os.getenv('HOME')}/kill_{pt_num}.sh")
	print(f'Killed PT : {pt_names[pt_num]}')


if __name__ == "__main__":
	#do stuff

	if os.getcwd() != os.getenv('HOME')+'':
		print("Please run the script from autoScript folder...")
		quit()

	if len(sys.argv) < 2:
		print('run script with syntax:')
		print('python3 browsertime_lover.py <type of experiment>')
		print('types: tranco, blocked')
		quit()
	else:
		mode = sys.argv[1]

	data20 = pd.read_csv(os.getenv('HOME') + 'websiteList/tranco_bas_krdo.csv')
	website_tr20 = data20.iloc[0:1000,0]

	data3 = pd.read_csv(os.getenv('HOME') + 'websiteList/1000-websites.csv')
	website_url = data3.iloc[0:1000,0]

	websites = website_tr20 if mode == 'tranco' else website_url

	os.system(f'mkdir {mode}')

	os.system(f"mkdir result_web_combine")

	#os.system(f'mkdir result_all')

	for pt_num in [6]:
		print(f"\n\n{pt_names[pt_num]}\n\n")
		print('Initiating...\n\n')
		initialisePT(pt_num)
		for website in websites:
			time.sleep(2)
			print("--------" + website + "--------")
			result = testWebsite(website, pt_num)
			print(result)
			print("----------------------------------------")
			print("\n\n")

		os.system(f"mv n-trf-tr{pt_num}.txt result_web_combine/")
		print(f"\n\n{pt_names[pt_num]} finished execution...\ncleaning up...\n\n")
		cleanupPT(pt_num)

	os.system(f'mv result_web* {mode}/')
	os.system(f"rm -rdf {os.getenv('HOME')}/browsertime-results/")

####################################################################################################################
