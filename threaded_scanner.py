from multiprocessing.connection import wait
import socket
import time
import threading
import requests

openPorts = []

# Function that attmepts connection to ports and timeout after 200ms
def portscan(port):
    global target
    global openPorts
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)
    try:
        con = s.connect((target, port))
        print('Port', port, 'is open')# this will tell you if only specific ports are open in the console
        openPorts.append(port)# stores all the open ports in a list called openPorts
        con.close()# Closes the connection after attempt
    except:
        pass
    
# Function that creates a savefile formatted datetime_target.txt
def saveFile():
    global target
    global openPorts
    with open(time.strftime('%Y-%m-%d_%H%M') + '_' + target + '.txt', 'a+') as f:
        for port in openPorts:
            f.write(str(port) + '\n')
        f.close()
        

# Function to scan only user specified ports
def specificPorts():
    global target
    global openPorts
    ports = input('Enter ports to scan (seperate with commas): ')# this will place user input ports in a list called ports
    ports = ports.split(',')
    ports = list(map(int, ports))
    print('Scanning ', target)
    print('Ports: ', ports)
    print('Time started:', time.strftime('%H:%M:%S'))
    for port in ports:
        t = threading.Thread(target=portscan, args=(int(port),))
        t.start()
    t.join() # Close the threads
    print('Time ended:', time.strftime('%H:%M:%S'))
    if 80 in openPorts or 443 in openPorts:
        answerHttp = input('HTTP ports {} are open, send GET header? (y/n)'.format(openPorts))
        if answerHttp == 'y':
            httpScan()
        if answerHttp == 'n':
            pass
    answer = input('Save output to txt file? (y/n): ')
    if answer == 'y':
        saveFile()# this will also save the output to a txt file with the datetime and target ip
    scanMenu()
    
# This will scan all ports 0 - 65535 and saves the output with the save function
def scanAll():
    global target
    global openPorts
    print('Scanning ', target)
    print('Time started:', time.strftime('%H:%M:%S'))
    for port in range(0, 65535):
        t = threading.Thread(target=portscan, args=(port,))
        t.start()
    t.join() # Close the threads
    print('Time ended:', time.strftime('%H:%M:%S'))
    if 80 in openPorts or 443 in openPorts:# Checks for port 80 or 443, if they are open it will give you an option to send a GET request
        answerHttp = input('HTTP ports are open, send GET header? (y/n)')
        if answerHttp == 'y':
            httpScan()
    answer = input('Save output to txt file? (y/n): ')# This saves the output with the save function
    if answer == 'y':
        saveFile()
    scanMenu()
# If port 80 or 443 are open it will send a GET request to the target using the format http://{target}/ or https://{target}/ for 
# https, if the response is 200 OK it will print this is a valid website, if 404 it will print this is not a valid website using the 
# requests module
def httpScan():
    global target
    global openPorts
    attempts = 0
    if 80 in openPorts:
        r = requests.get('http://' + target + '/')
        if r.status_code == 200:
            print('This is a valid website\n')
            print("_"*75)
            print(r.headers)
            print("_"*75)
            attempts += 1
        else:
            print('This is not a valid website')
    elif 443 in openPorts:
        r = requests.get('https://' + target + '/')
        if r.status_code == 200:
            print('This is a valid website')
            print("_"*75)
            print(r.headers)
            print("_"*75)
            attempts += 1
        else:
            print('This is not a valid website')
    else:
        print('No open HTTP ports')
    answer = input('Save output to txt file? (y/n): ')
    if answer == 'y':
        for openPorts in range(0, attempts):
            with open(time.strftime('%Y-%m-%d_%H%M') + '_' + 'target_requests' + '.txt', 'a+') as f:
                f.write(r.headers)
                f.close()
        with open(time.strftime('%Y-%m-%d_%H%M') + '_' + target + '.txt', 'a+') as f:
            f.write(r.headers)
            f.close()
    scanMenu()
 #This will capture a screenshot of the url that the GET request is being sent to

    
# This function sends a blind GET request to the target if it is a url by sending the GET to target URL for HTTPS Connection
# and HTTP connections
def blindGET():
    global target
    global url
    openPorts = [80, 443]
    if 80 in openPorts:
        r = requests.get(url)
        print(r.headers)
    elif 443 in openPorts:
        r = requests.get(url)
        print(r.headers['Server'])
    else:
        print('No open HTTP ports')
    answer = input('Save output to txt file? (y/n): ')
    if answer == 'y':
        with open(time.strftime('%Y-%m-%d_%H%M') + '_' + 'target_requests' + '.txt', 'a+') as f:
            f.write(r.headers['Server'])
            f.close()
    scanMenu()
        
  
# This provides a menu for the user to choose what they want to do
def scanMenu():
    print('''
    1 > Scan all ports
    2 > Scan specific ports
    3 > HTTP GET request
    ''')
    choice = input('Enter choice: ')
    if choice == '1':
        scanAll()
    elif choice == '2':
        specificPorts()
    elif choice == '3':
        blindGET()
    elif choice == '4':
        exit(0)
    else:
        print('Invalid input')
        scanMenu()
        

# this function opens a txt file called foxhuntbanner.txt from portscannerTest\foxhuntbanner.txt and outputs it to console when the program initializes
'''def banner():
    with open('banner.txt', 'r') as f:
        print(f.read())
        print('\t\t\t\tCreated by slyf0x')
        print('_'*75)
        print('\n')
'''     
# This function will determine if the user is scanning a url or ip and change the target variable to the url or ip
def getTarget(): #FIXME this function is not working, will not scan URLs only IPS
    global target
    global url
    target1 = input('Scanning URL or IP? (u/i): ')
    if target1 == 'u':
        url = input('Enter URL: ')
        target = url
        scanMenu()
        
    elif target1 == 'i':
        target = input('Enter IP: ')
        scanMenu()
    else:
        print('Invalid input')
        getTarget()

# This function will ask if you would like to rescan the same target or try another target
def rescan():
    answer = input('Would you like to rescan the same target? (y/n): ')
    if answer == 'y':
        scanMenu()
    elif answer == 'n':
        getTarget()
        scanMenu()
    else:
        print('Invalid input')
        rescan()
       
# our main function, scans the port and then recursively asks if you want to scan another ip before quitting
def main():
    try:
        getTarget()# This is used to get target IP or URL
        rescan()# Asks user if they want to change target or rescan the same target
        main()# loops main
    except KeyboardInterrupt:
        print('Exiting...')
        wait(2)
        exit(0)
    
if __name__ == '__main__':
    #banner()
    main()
    
     