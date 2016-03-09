import xml.dom.minidom

def parseMyXML(path):

    datasource = open(path)
    portList = {}
    dom = xml.dom.minidom.parse(datasource)
    run = dom.getElementsByTagName("nmaprun")
    hosts = dom.getElementsByTagName("hostname")
    address = dom.getElementsByTagName("address")
    ports = dom.getElementsByTagName("port")
    runTime = run[0].getAttribute('startstr')
    hostName = hosts[0].getAttribute('name')
    hostIP = address[0].getAttribute('addr')
    for port in ports:
        temp = []
        service = port.getElementsByTagName("service")
        state = port.getElementsByTagName("state")
        portNumber = port.getAttribute('portid')
        portProtocol = port.getAttribute('protocol')
        serviceName = service[0].getAttribute('name')
        portState = state[0].getAttribute('state')
        temp.append(portProtocol)
        temp.append(serviceName)
        temp.append(portState)
        portList[portNumber] = temp
    return runTime,hostName,hostIP,portList
