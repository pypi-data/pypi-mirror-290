import xml.dom.minidom, os, json, time, sys
import xml.etree.ElementTree as ET

def update_junit_report(input, output):

    test_case_name = []
    test_id = []

    doc = xml.dom.minidom.parse(input)
    tests = doc.getElementsByTagName("test")
    msgs = doc.getElementsByTagName("msg")
    for name in tests:
        test_case_name.append(name.getAttribute("name"))

    root = ET.parse(input)

    message_elements = root.findall(".//msg")

    for message_element in message_elements:
        if message_element.text and "${TEST_ID}" in message_element.text:
            test_ids = message_element.text.replace('${TEST_ID} = ', '')
            test_id.append(test_ids)

    with open('test_id_temp.txt', 'w') as f:
        f.write(str(test_id))

    docs_temp = xml.dom.minidom.parse(output)
    nodes = docs_temp.getElementsByTagName("properties")

    for node in nodes:
        parent = node.parentNode
        parent.removeChild(node)
        with open(output,'w') as f:
            f.write(docs_temp.toprettyxml())

    time.sleep(1)
    junit_temps = xml.dom.minidom.parse(output)
    testcase = junit_temps.getElementsByTagName("testcase")

    for i in range(testcase.length):
        tag = testcase[i].appendChild(junit_temps.createElement('properties'))
        tag.appendChild(junit_temps.createTextNode(''))
        with open(output,'w') as f:
            f.write(junit_temps.toprettyxml())

    time.sleep(1)
    junit_docs = xml.dom.minidom.parse(output)
    props = junit_docs.getElementsByTagName("properties")

    for i in range(props.length):
        tag = junit_docs.createElement("property")
        tag.setAttribute("name"  , 'test_id')
        tag.setAttribute("value"  , test_id[i])
        props[i].appendChild(tag)
        with open(output,'w') as f:
            f.write(junit_docs.toprettyxml())