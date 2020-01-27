import unittest
import time
import os

from kubernetes import utils, client, config
from kubernetes.client.rest import ApiException

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

pg_content = "/html/body/kd-root/kd-login/div/kd-card/mat-card/div/mat-card-content/div/div/form"

#class TestLoginDashboard():
def main():
    dashboardPort = getDashboardPort()
    driver = getDriver(dashboardPort)
    token = getToken()

    radioXpath = pg_content + "/mat-radio-group/div[2]/mat-radio-button/label/div[1]"
    radioTokenButton = waitForElementWithXpath(driver, radioXpath)
    radioTokenButton.click()
    
    tokenXpath = pg_content + "/mat-form-field"
    tokenEntry = waitForElementWithXpath(driver, tokenXpath)
    tokenEntry.click()

    tokenFieldXpath = "//*[@id='token']"
    tokenField = waitForElementWithXpath(driver, tokenFieldXpath)
    tokenField.send_keys(token)
    
    signInXpath = pg_content + "/div/button"
    signInButton = waitForElementWithXpath(driver, signInXpath)
    signInButton.click()

    time.sleep(5)
    print("page title %s"%driver.title) # Kubernetes Dashboard
    driver.close()

def getDriver(dashboardPort):
    driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
    driver.get("https://172.26.138.146:" + dashboardPort)
    time.sleep(5)
    return driver

def getToken():
    command = "kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')"
    #command="kubectl describe secret " + str(secretName) #+ " | grep -E '^token' | cut -f2 -d':' | tr -d ' '"
    # print("command to extract token %s"%command)
    stream = os.popen(command)
    kToken = stream.read()
    nToken = kToken.split("token:")
    aToken = nToken[1].strip()
    #print("Using token '%s'"%aToken)
    return aToken

def waitForElementWithXpath(driver, xpath, timeout=30):
    element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH ,xpath)), 'Waiting xpath:{}'.format(xpath)
    )
    return element

def getDashboardPort():
    portRef = ""
    # Create a configuration object
    aConfiguration = config.load_kube_config()
    # Create a ApiClient with our config
    aApiClient = client.ApiClient(aConfiguration)
    core_v1 = client.CoreV1Api(aApiClient)

    response = core_v1.list_namespaced_service("kube-system")
    for i in response.items:
        if "kubernetes-dashboard" in i.metadata.name:
            print("dashboard service: %s"%i)
            for p in i.spec.ports:
                portRef = str(p.node_port)
    return portRef


if __name__ == '__main__':
    main()
