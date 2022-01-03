

#*==========================*#
#*==========================*#
#* Import/Load Data Section *#
#*==========================*#
#*==========================*#
#region

#region

import streamlit as st
import streamlit.components.v1 as components
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from configparser import ConfigParser
import time
import webbrowser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import re
import pymongo
from pymongo import MongoClient
import sys

#endregion


#*=============*#
#*=============*#
#* Var Section *#
#*=============*#
#*=============*#
#region


emails_data_count = 0

### !Loading config.ini Data ###
#region 

# ["cobra_builder_data"]
config_file = "config.ini"
parser = ConfigParser()
parser.read(config_file)
user_id = parser["user_data"]["user_id"]
user_name = parser["cobra_builder_data"]["user_name"]
server_ip = parser["cobra_builder_data"]["server_ip"]
root_password = parser["cobra_builder_data"]["root_password"]
domain = parser["cobra_builder_data"]["domain"]
main_email = parser["cobra_builder_data"]["main_email"]
cyberpanel_user = parser["cobra_builder_data"]["cyberpanel_user"]
cyberpanel_password = parser["cobra_builder_data"]["cyberpanel_password"]
wordpress_user = parser["cobra_builder_data"]["wordpress_user"]
wordpress_password = parser["cobra_builder_data"]["wordpress_password"]
admin_email = parser["cobra_builder_data"]["admin_email"]
admin_email_password = parser["cobra_builder_data"]["admin_email_password"]

# ["cobra_sender_data"]
sender_domain = parser["cobra_sender_data"]["sender_domain"]
sender_email = parser["cobra_sender_data"]["sender_email"]
sender_email_password = parser["cobra_sender_data"]["sender_email_password"]

# ["cobra_reporting_data"]
user_data_dir = parser["cobra_reporting_data"]["user_data_dir"]
user_profile_1 = parser["cobra_reporting_data"]["user_profile_1"]
user_profile_2 = parser["cobra_reporting_data"]["user_profile_2"]
user_profile_3 = parser["cobra_reporting_data"]["user_profile_3"]
user_profile_4 = parser["cobra_reporting_data"]["user_profile_4"]
user_profile_5 = parser["cobra_reporting_data"]["user_profile_5"]
user_profile_6 = parser["cobra_reporting_data"]["user_profile_6"]
user_profile_7 = parser["cobra_reporting_data"]["user_profile_7"]
user_profile_8 = parser["cobra_reporting_data"]["user_profile_8"]
user_profile_9 = parser["cobra_reporting_data"]["user_profile_9"]
user_profile_10 = parser["cobra_reporting_data"]["user_profile_10"]
user_profile_11 = parser["cobra_reporting_data"]["user_profile_11"]
#endregion

#! Config Dictionary
#region
parser = ConfigParser()
parser.read("config.ini")

config_dictionary = {}
for section in parser.sections():
    config_dictionary[section] = {}
    for option in parser.options(section):
        config_dictionary[section][option] = parser.get(section, option)

#endregion



#! Function: Get User Data - UserID Auth ...
#region 
def user_id_authentication(user_id):
    # With Reader User :
    client = MongoClient("mongodb+srv://reader101:jfX7t66Cavm3VAwM@cluster0.xpdoo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    # Targeted Database
    cobra_database = client["cobra"]
    # Targeted Collection
    user_id_collection = cobra_database["user_id"]
    # Request & Get Data From Database
    response = user_id_collection.find_one({"user_id": user_id})

    if response is not None:
        print("UserID - [OK]")
        user_data_dict = response

    else:
        print("UserID - [ERROR]")
        sys.exit("[-] User-ID Error, You have to use a valid [user-id] to work with this program !!")
    return user_data_dict
user_data_dict = user_id_authentication(user_id)
user_id = user_data_dict.get('user_id')
product = user_data_dict.get('product')
user_name = user_data_dict.get('user_name')
user_email = user_data_dict.get('user_email')
user_membership_type = user_data_dict.get('user_membership_type')
#endregion

#endregion


#*================*#
#* Pages Elements *#
#*================*#
#region 

# !Page Elements: Cobra Sniper
#region
next_page_webelement_xpath = "//a[@title='Next page']" 
#endregion


### !📦Page Elements: Connect/Login to CyberPanel ###
#region 
#--- URL Element
cyberpanel_login_page_url = f"https://{server_ip}:8090"
#--- Xpath Elements
advanced_button_xpath = '//*[@id="details-button"]'
proceed_to_link_xpath = '//*[@id="proceed-link"]'
username_input_xpath = '//*[@name="username"]'
password_input_xpath = '//*[@name="password"]'
sign_in_button_xpath = '//*[@type="button"]'
#endregion


### !📦Page Elements: Update Default Package ###
#region 
#--- URL Element
cyberpanel_modifyPackage_page_url = f"https://{server_ip}:8090/packages/modifyPackage"
#--- Xpath Elements
update_default_package_select_dropdown_xpath = '//*[@ng-model="packageToBeModified"]'
domains_number_input_xpath = '//*[@ng-model="allowedDomains"]'
disk_space_input_xpath = '//*[@ng-model="diskSpace"]'
bandwidth_input_xpath = '//*[@ng-model="bandwidth"]'
modify_package_button_xpath = '//*[@ng-click="modifyPackageFunc()"]'
update_default_package_page_process_success_message_xpath = '//*[text()=" Successfully Modified"]'
#endregion


### !📦Page Elements: Create Website ###
#region 
#--- URL Element
createWebsite_page_url = f"https://{server_ip}:8090/websites/createWebsite"
#--- Xpath Elements
select_website_package_dropdown_xpath = '//*[@ng-model="packageForWebsite"]'
select_owner_dropdown_xpath = '//*[@ng-model="websiteOwner"]'
domain_name_input_xpath = '//*[@ng-model="domainNameCreate"]'
email_input_xpath = '//*[@ng-model="adminEmail"]'
select_php_dropdown_xpath = '//*[@ng-model="phpSelection"]'
dkim_support_checkbox_xpath = '//*[@ng-model="dkimCheck"]'
create_website_button_xpath = '//*[@ng-click="createWebsite()"]'
create_website_success_message_xpath = '//*[contains(text(),"Successfully Installed.")]'
#endregion


### !📦Page Elements: Issue SSL ###
#region 
#--- URL Element
issue_ssl_page_url = f"https://{server_ip}:8090/manageSSL/manageSSL"
#--- Xpath Elements
select_website_dropdown_xpath = '//*[@ng-model="virtualHost"]'
issue_ssl_button_xpath = '//*[@ng-click="issueSSL()"]'
issue_ssl_process_success_message_xpath = '//*[contains(text(),"SSL Issued for")]'
#endregion


### !📦Page Elements: Install wordpress ###
#region 
#--- URL Element
install_wordpress_page_url = f"https://{server_ip}:8090/websites/{domain}/wordpressInstall"
#--- Xpath Elements
install_wordpress_page_process_success_message_xpath = '//*[contains(text(),"Successfully Installed.")]'
blog_title_input_xpath = '//*[@ng-model="blogTitle"]'
login_user_input_xpath = '//*[@ng-model="adminUser"]'
login_password_input_xpath = '//*[@ng-model="adminPassword"]'
email_input_xpath = '//*[@ng-model="adminEmail"]'
install_now_button_xpath = '//*[@ng-click="installWordPress()"]'
#endregion


### !📦Page Elements: Issue ssl for mail server ###
#region 
#--- URL Element
ssl_for_mail_server_page_url = f"https://{server_ip}:8090/manageSSL/sslForMailServer"
#--- Xpath Elements
ssl_for_mail_server_page_process_success_message_xpath = '//*[contains(text(),"SSL Issued, your mail server")]'
issue_ssl_for_mail_server_select_website_dropdown_xpath = '//*[@ng-model="virtualHost"]'
issue_ssl_for_mail_server_issue_ssl_button_xpath = '//*[@ng-click="issueSSL()"]'
#endregion


### !📦Page Elements: Create email account page ###
#region 
#--- URL Element
create_email_account_page_url = f"https://{server_ip}:8090/email/createEmailAccount"
#--- Xpath Elements
create_email_account_page_process_success_message_xpath = '//*[contains(text(),"is successfully created.")]' 
create_email_account_select_website_xpath = '//*[@ng-model="emailDomain"]'
create_email_account_user_name_input_xpath = '//*[@ng-model="emailUsername"]'
create_email_account_password_input_xpath = '//*[@class="example-box-wrapper"]/form/div[3]/div[1]/input'
create_email_account_button_xpath = '//*[@ng-click="createEmailAccount()"]' 
#endregion


### !📦Page Elements: List email account page ###
#region 
#--- URL Element
list_emails_page_url = f"https://{server_ip}:8090/email/listEmails"
#--- Xpath Elements
page_process_success_message_xpath = '//*[@attr]'
list_email_page_select_domain_xpath = '//*[@ng-model="selectedDomain"]'
list_email_page_fix_now_xpath = '//*[@ng-click="fixMailSSL()"]'
#endregion


### !📦Page Elements: Add Modify DNS Zone ###
#region
#--- URL Element
add_delete_dns_records_page_url = f"https://{server_ip}:8090/dns/addDeleteDNSRecords"
#--- Xpath Elements
select_domain_dropdown_xpath = '//*[@ng-change="fetchRecords()"]'
# TXT Section
txt_button_xpath = """//*[@ng-click="fetchRecordsTabs('txtRecord')"]"""
spf_record_name_input_xpath = '//tbody/tr[1]/td[2]/input[@ng-model="nameNow"]'
spf_record_value_input_xpath =  '//tbody/tr[1]/td[4]/input[@ng-model="contentNow"]'
dmarc_record_name_input_xpath = '//tbody/tr[2]/td[2]/input[@ng-model="nameNow"]'
dmarc_record_value_input_xpath = '//tbody/tr[2]/td[4]/input[@ng-model="contentNow"]'
dkim_record_name_input_xpath = '//tbody/tr[4]/td[2]/input[@ng-model="nameNow"]'
dkim_record_value_input_xpath = '//tbody/tr[4]/td[4]/input[@ng-value="record.content"]'
# MX Section
select_mx_button_xpath = '//*[contains(text(),"MX")]'
mx_record_name_input_xpath = '//tbody/tr[1]/td[2]/input[@ng-model="nameNow"]'
mx_record_name_value_xpath = '//tbody/tr[1]/td[4]/input[@ng-model="contentNow"]'
#endregion

#endregion



#! Test Mode ###########
#region 
#? Test/Normal Mode
test_mode = "off"

#? Hide Browser Mode
off_screen = "on"
#endregion
#!########################



#endregion




#*==============*#
#*==============*#
#* Core Section *#
#*==============*#
#*==============*#
#region 

#*=========================*#
#* Cobra Builder Functions *#
#*=========================*#
#region

### !📦Function: Element-Vision Stats ###
#!▶️▶️▶️
def element_vision_stats(element_name, element_xpath):
    web_element = driver.find_element(By.XPATH, element_xpath)
    if web_element:
        print(" ")
        print(f"[-EVS-] Page-Key/{element_name}/Element-Vision = %100 - Web-Element: {web_element} - [-Page Loading Success-]")
        print(" ")
    else:
        print(" ")
        print(f"[-EVF-] Page-Key/{element_name}/Element-Vision = %0 - Web-Element: [NOT-DETECTED]")
        print(" ")


### !📦Function: Page Process Success ###
#!▶️▶️▶️
def page_process_success(expected_page_title):
    current_page_title = driver.title

    if current_page_title == expected_page_title:
        page_process_success_result = 1
    else:
        page_process_success_result = 0

    return page_process_success_result


### !📦Function: Set Driver ###
#!▶️▶️▶️
def set_driver():
    global driver
    # Setting Chrome Profile Options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Launch driver
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    driver.maximize_window()
    driver.execute_script("window.open('','_blank')")
    # Hide Browser
    if off_screen == "on":
        driver.set_window_position(11000, 11000, windowHandle='current')
        driver.set_window_size(1920, 1080)
    driver.implicitly_wait(30)
    time.sleep(5)


### !📦Function: Connect/Login to CyberPanel ###
#!▶️▶️▶️
def connect_to_cyberpanel():
    global connect_to_cyberpanel_page_process_success_message

    #region - Login Page Processes
    #--- Navigate to CyberPanel LoginPage
    driver.get(cyberpanel_login_page_url)

    #* --- Page Key Element Vision Stats
    element_vision_stats("Advanced Button", advanced_button_xpath)

    #--- Click on Advanced Button
    advanced_button = driver.find_element(By.XPATH, advanced_button_xpath)
    advanced_button.click()
    time.sleep(3)
    #--- Click on Proceed to ..
    proceed_to_link = driver.find_element(By.XPATH, proceed_to_link_xpath)
    proceed_to_link.click()

    #* --- Page Key Element Vision Stats
    element_vision_stats("username_input", username_input_xpath)

    #--- Type username
    username_input = driver.find_element(By.XPATH, username_input_xpath)
    username_input.clear()
    username_input.send_keys(cyberpanel_user)
    #--- Enter Password
    password_input = driver.find_element(By.XPATH, password_input_xpath)
    password_input.clear()
    password_input.send_keys(cyberpanel_password)
    #--- Click Sign In Button
    sign_in_button = driver.find_element(By.XPATH, sign_in_button_xpath)
    sign_in_button.click()
    time.sleep(7)
    #--- Page Process Success
    login_page_process_success = page_process_success("Home - CyberPanel")
    if login_page_process_success == 1:
        connect_to_cyberpanel_page_process_success_message = "Connected to CyberPanel"
        print(" ")
        print("Connected to CyberPanel ..")
        print(" ")
    else:
        print("Error: Connection to CyberPanel Failed !! - Retry this Step")
    #endregion

 
### !📦Function: Update Default Package ###
#!▶️▶️▶️
def update_default_package():
    global update_default_package_page_process_success_message

    #region - modifyPackage Page Processes
    # --- navigate to modifyPackage Page
    driver.get(cyberpanel_modifyPackage_page_url)
    time.sleep(5)

    #* --- Page Key Element Vision Stats
    element_vision_stats("select_package_dropdown", update_default_package_select_dropdown_xpath)

    # --- Select Package Drop-Down
    select_package_dropdown = Select(driver.find_element(By.XPATH, update_default_package_select_dropdown_xpath))
    select_package_dropdown.select_by_value('Default')
    time.sleep(3)
    # --- Set domains number
    domains_number_input = driver.find_element(By.XPATH, domains_number_input_xpath)
    domains_number_input.clear()
    domains_number_input.send_keys('20')
    # --- Set disk space
    disk_space_input = driver.find_element(By.XPATH, disk_space_input_xpath)
    disk_space_input.clear()
    disk_space_input.send_keys(10000)
    # --- Set bandwidth
    bandwidth_input = driver.find_element(By.XPATH, bandwidth_input_xpath)
    bandwidth_input.clear()
    bandwidth_input.send_keys(0)
    
    #? Test Mode
    if test_mode == "on":
        modify_package_button = driver.find_element(By.XPATH, modify_package_button_xpath)
        print(" ")
        print(f"[+] I can see modify_package_button Web Element --- {modify_package_button}")
        print(" ")
    else:
        # Normal Mode - Take Action
    
        # --- Click Modify Package Button
        modify_package_button = driver.find_element(By.XPATH, modify_package_button_xpath)
        modify_package_button.click()
        
        # --- update_default_package_page Process Success Message
        # Explicit wait
        update_default_package_page_process_success_message_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, update_default_package_page_process_success_message_xpath)))
        # Scrape update_default_package_page Success Message Text
        update_default_package_page_process_success_message = driver.find_element(By.XPATH, update_default_package_page_process_success_message_xpath).text
        # Print update_default_package_page Success Message
        print("\n --- Package Default Successfully Updated" + update_default_package_page_process_success_message + " --- \n")
        update_default_package_page_process_success_message = "Package Default Successfully Updated"
        time.sleep(3)

    #endregion


### !📦Function: Create Website ###
#!▶️▶️▶️
def create_website():
    global create_website_success_message

    #region - createWebsite Page Elements Processes
    # --- navigate to createWebsite Page
    driver.get(createWebsite_page_url)
    time.sleep(5)

    #* --- Page Key Element Vision Stats
    element_vision_stats("select_package_dropdown", select_website_package_dropdown_xpath)

    # --- Select package Drop-Down
    select_package_dropdown = Select(driver.find_element_by_xpath(select_website_package_dropdown_xpath))
    select_package_dropdown.select_by_value('Default')
    # --- Select owner Drop-Down
    select_owner_dropdown = Select(driver.find_element_by_xpath(select_owner_dropdown_xpath))
    select_owner_dropdown.select_by_value('admin')
    # --- Domain input
    domain_name_input = driver.find_element(By.XPATH, domain_name_input_xpath)
    domain_name_input.clear()
    domain_name_input.send_keys(domain)
    # --- Email input
    email_input = driver.find_element(By.XPATH, email_input_xpath)
    email_input.clear()
    email_input.send_keys(main_email)
    # --- Select PHP Drop-Down
    select_php_dropdown = Select(driver.find_element_by_xpath(select_php_dropdown_xpath))
    select_php_dropdown.select_by_value('PHP 7.4')
    # --- click DKIM Support Checkbox
    # [Scroll to Element]
    dkim_support_checkbox = driver.find_element(By.XPATH, dkim_support_checkbox_xpath)
    actions = ActionChains(driver)
    actions.move_to_element(dkim_support_checkbox).perform()
    time.sleep(1)
    # Click it
    dkim_support_checkbox.click()
    # --- Click Create Website Button
    # [Scroll to Element]
    create_website_button = driver.find_element(By.XPATH, create_website_button_xpath)
    actions = ActionChains(driver)
    actions.move_to_element(create_website_button).perform()
    time.sleep(1)


    #? Test/Normal Mode
    if test_mode == "on":
        create_website_button = driver.find_element(By.XPATH, create_website_button_xpath)
        print(" ")
        print(f"[+] I can see create_website_button Web Element --- {create_website_button}")
        print(" ")
    else:
        # Normal Mode - Take Action

        # Click it
        create_website_button.click()
        time.sleep(3)
        #endregion

        #region - Create Website Page Success Message
        # Explicit wait
        create_website_success_message = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, create_website_success_message_xpath)))
        # Scrape Success Message Text
        create_website_success_message = driver.find_element(By.XPATH, create_website_success_message_xpath).text
        # Print Success Message
        print("\n --- Website " + create_website_success_message + " --- \n")
    #endregion


### !📦Function: Issue SSL ### 
#!▶️▶️▶️
def issue_ssl():
    #region - issue_ssl Page Elements Processes
    # --- navigate to issue_ssl Page
    driver.get(issue_ssl_page_url)
    time.sleep(5)

    #* --- Page Key Element Vision Stats
    element_vision_stats("select_website_dropdown", select_website_dropdown_xpath)

    # --- Select Website Drop-Down
    select_website_dropdown = Select(driver.find_element_by_xpath(select_website_dropdown_xpath))
    select_website_dropdown.select_by_value(domain)
    # --- Click issue ssl Button 
    
    #? Test Mode
    if test_mode == "on":
        issue_ssl_button = driver.find_element(By.XPATH, issue_ssl_button_xpath)
        print(" ")
        print(f"[+] I can see SSL Button Web Element --- {issue_ssl_button}")
        print(" ")

    else:
        issue_ssl_button = driver.find_element(By.XPATH, issue_ssl_button_xpath)
        issue_ssl_button.click()
        # --- issue_ssl Process Success Message
        # Explicit wait
        issue_ssl_process_success_message_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, issue_ssl_process_success_message_xpath)))
        # Scrape issue_ssl Success Message Text
        issue_ssl_process_success_message = driver.find_element(By.XPATH, issue_ssl_process_success_message_xpath).text
        # Print issue_ssl Success Message
        print("\n --- " + issue_ssl_process_success_message + " --- \n")
    #endregion


### !📦Function: Install Wordpress ###
#!▶️▶️▶️
def install_wordpress():
    #region - install_wordpress_page Elements Processes
    # --- navigate to install_wordpress_page
    driver.get(install_wordpress_page_url)
    time.sleep(5)

    #* --- Page Key Element Vision Stats
    element_vision_stats("blog_title_input", blog_title_input_xpath)

    # blog_title_input Element
    blog_title_input = driver.find_element(By.XPATH, blog_title_input_xpath)
    blog_title_input.clear()
    blog_title_input.send_keys(domain)

    # login_user_input Element
    login_user_input = driver.find_element(By.XPATH, login_user_input_xpath)
    login_user_input.clear()
    login_user_input.send_keys(wordpress_user)


    # login_password_input Element
    login_password_input = driver.find_element(By.XPATH, login_password_input_xpath)
    login_password_input.clear()
    login_password_input.send_keys(wordpress_password)

    # email_input Element
    email_input = driver.find_element(By.XPATH, email_input_xpath)
    email_input.clear()
    email_input.send_keys(main_email)

    # install_now_button Element
    #? Test Mode
    if test_mode == "on":
        install_now_button = driver.find_element(By.XPATH, install_now_button_xpath)
        print(" ")
        print(f"[+] I can see install_now_button Web Element --- {install_now_button}")
        print(" ")
    else:
        # Normal Mode - Take Action
        install_now_button = driver.find_element(By.XPATH, install_now_button_xpath)
        install_now_button.click()

        #endregion

        #region - install_wordpress_page Process Success Message
        # Explicit wait
        install_wordpress_page_process_success_message_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, install_wordpress_page_process_success_message_xpath)))
        # Scrape install_wordpress_page Success Message Text
        install_wordpress_page_process_success_message = driver.find_element(By.XPATH, install_wordpress_page_process_success_message_xpath).text
        # Print install_wordpress_page Success Message
        print("\n --- " + install_wordpress_page_process_success_message + " --- \n")

    #endregion


### !📦Function: Issue ssl for mail server ###
#!▶️▶️▶️
def issue_ssl_for_mail_server():
    #region - ssl_for_mail_server_page Elements Processes
    # --- navigate to ssl_for_mail_server_page
    driver.get(ssl_for_mail_server_page_url)
    time.sleep(5)

    #* --- Page Key Element Vision Stats
    element_vision_stats("issue_ssl_for_mail_server_select_website_dropdown", issue_ssl_for_mail_server_select_website_dropdown_xpath)

    # Select element Drop-Down
    issue_ssl_for_mail_server_select_website_dropdown = Select(driver.find_element(By.XPATH, issue_ssl_for_mail_server_select_website_dropdown_xpath))
    issue_ssl_for_mail_server_select_website_dropdown.select_by_value(domain)
    # Click issue_ssl_for_mail_server_issue_ssl_button
    
    #? Test Mode
    if test_mode == "on":
        issue_ssl_for_mail_server_issue_ssl_button = driver.find_element(By.XPATH, issue_ssl_for_mail_server_issue_ssl_button_xpath)
        print(" ")
        print(f"[+] I can see issue_ssl_button Web Element --- {issue_ssl_for_mail_server_issue_ssl_button}")
        print(" ")
    else:
        # Normal Mode - Take Action
        issue_ssl_for_mail_server_issue_ssl_button = driver.find_element(By.XPATH, issue_ssl_for_mail_server_issue_ssl_button_xpath)
        issue_ssl_for_mail_server_issue_ssl_button.click()
        #endregion

        #region - ssl_for_mail_server_page Process Success Message
        # Explicit wait
        ssl_for_mail_server_page_process_success_message_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, ssl_for_mail_server_page_process_success_message_xpath)))
        # Scrape ssl_for_mail_server_page Success Message Text
        ssl_for_mail_server_page_process_success_message = driver.find_element(By.XPATH, ssl_for_mail_server_page_process_success_message_xpath).text
        # Print ssl_for_mail_server_page Success Message
        print("\n --- " + ssl_for_mail_server_page_process_success_message + " --- \n")
    #endregion


### !📦Function: Create email account page ###
#!▶️▶️▶️
def create_email_account():
    #region - create_email_account_page Elements Processes
    # --- navigate to create_email_account_page
    driver.get(create_email_account_page_url)
    time.sleep(5)

    #* --- Page Key Element Vision Stats
    element_vision_stats("create_email_account_select_website", create_email_account_select_website_xpath)

    # create_email_account_select_website drop_down
    create_email_account_select_website = Select(driver.find_element(By.XPATH, create_email_account_select_website_xpath))
    create_email_account_select_website.select_by_value(domain)
    time.sleep(5)

    # create_email_account_user_name_input Element
    create_email_account_user_name_input = driver.find_element(By.XPATH, create_email_account_user_name_input_xpath)
    create_email_account_user_name_input.clear()
    create_email_account_user_name_input.send_keys(admin_email)

    # Input Element
    create_email_account_password_input = driver.find_element(By.XPATH, create_email_account_password_input_xpath)
    create_email_account_password_input.clear()
    create_email_account_password_input.send_keys(admin_email_password)

    # Click Element
    
    #? Test Mode
    if test_mode == "on":
        create_email_account_button = driver.find_element(By.XPATH, create_email_account_button_xpath)
        print(" ")
        print(f"[+] I can see create_email_account_button Web Element --- {create_email_account_button}")
        print(" ")
    else:
        # Normal Mode - Take Action
        create_email_account_button = driver.find_element(By.XPATH, create_email_account_button_xpath)
        create_email_account_button.click()

        #region - create_email_account_page Process Success Message

        # Explicit wait
        create_email_account_page_process_success_message_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, create_email_account_page_process_success_message_xpath)))
        # Scrape create_email_account_page Success Message Text
        create_email_account_page_process_success_message = driver.find_element(By.XPATH, create_email_account_page_process_success_message_xpath).text
        # Print create_email_account_page Success Message
        print("\n --- " + create_email_account_page_process_success_message + " --- \n")
        #endregion
    
    #endregion


### !📦Function: List email account page / FIX SSL ###
#!▶️▶️▶️
def list_email_account():
    #region - list_emails_page Elements Processes
    # --- navigate to list_emails_page
    driver.get(list_emails_page_url)
    time.sleep(5)

    #* --- Page Key Element Vision Stats
    element_vision_stats("list_email_page_select_domain_dropdown_element", list_email_page_select_domain_xpath)


    # Select element Drop-Down - select_domain_dropdown
    list_email_page_select_domain_dropdown_element = Select(driver.find_element(By.XPATH, list_email_page_select_domain_xpath))
    list_email_page_select_domain_dropdown_element.select_by_value(domain)
    time.sleep(5)
    #Click Element - fix_now_element

    #? Test Mode
    if test_mode == "on":
        list_email_page_fix_now_button = driver.find_element(By.XPATH, list_email_page_fix_now_xpath)
        print(" ")
        print(f"[+] I can see fix_now_button Web Element --- {list_email_page_fix_now_button}")
        print(" ")
    else:
        # Normal Mode - Take Action
        list_email_page_fix_now_button = driver.find_element(By.XPATH, list_email_page_fix_now_xpath)
        list_email_page_fix_now_button.click()
        time.sleep(11)
        #endregion

        #region - #FIXME:#!list_emails_page Process Success Message
        #TODO: [Abdelkarim] - if "Fix Button" element xpath not exist then print success message !
        #TODO: --- Explicitly wait until the element not exist ..
        # Explicit wait
        #?list_emails_page_process_success_message_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, list_emails_page_process_success_message_xpath)))
        # Scrape list_emails_page Success Message Text
        #?list_emails_page_process_success_message = driver.find_element(By.XPATH, list_emails_page_process_success_message_xpath).text
        # Print list_emails_page Success Message
        #?print("\n --- " + list_emails_page_process_success_message + " --- \n")
        #endregion


### !📦Function: Add Modify DNS Zone / Get Mailing Server DNS Records ###
#!▶️▶️▶️
def get_mailing_dns_records():
    # --- navigate to add_delete_dns_records_page
    driver.get(add_delete_dns_records_page_url)
    time.sleep(5)

    #* --- Page Key Element Vision Stats
    element_vision_stats("select_domain_dropdown", select_domain_dropdown_xpath)

    # Select element Drop-Down - select_domain_dropdown
    select_domain_dropdown = Select(driver.find_element(By.XPATH, select_domain_dropdown_xpath))
    select_domain_dropdown.select_by_value(domain)
    time.sleep(5)

    # Click Element - txt_button
    txt_button = driver.find_element(By.XPATH, txt_button_xpath)
    txt_button.click()
    time.sleep(5)

    # Scrape/Get Element Attribute - spf_record_name_input
    spf_record_name_input = driver.find_element(By.XPATH, spf_record_name_input_xpath).get_attribute('value')

    # Scrape/Get Element Attribute - spf_record_value_input
    spf_record_value_input = driver.find_element(By.XPATH, spf_record_value_input_xpath).get_attribute('value')

    # --- Print Lines
    get_mailing_dns_records.spf_record_lines =f"""SPF Record 
    Type: TXT
    Name: [ @ ] 
    Value: [ {spf_record_value_input} ]
    """
    print(get_mailing_dns_records.spf_record_lines)

    # Scrape/Get Element Attribute - dmarc_record_name_input
    dmarc_record_name_input = driver.find_element(By.XPATH, dmarc_record_name_input_xpath).get_attribute('value')

    # Scrape/Get Element Attribute - dmarc_record_value_input
    dmarc_record_value_input = driver.find_element(By.XPATH, dmarc_record_value_input_xpath).get_attribute('value')

    # --- Print Lines
    get_mailing_dns_records.dmarc_record_lines =f"""DMARC Record 
    Type: TXT
    Name: [ _dmarc ] 
    Value: [ {dmarc_record_value_input} ]
    """
    print(get_mailing_dns_records.dmarc_record_lines)

    # Scrape/Get Element Attribute - dkim_record_name_input
    dkim_record_name_input = driver.find_element(By.XPATH, dkim_record_name_input_xpath).get_attribute('value')

    # Scrape/Get Element Attribute - dkim_record_value_input
    dkim_record_value_input = driver.find_element(By.XPATH, dkim_record_value_input_xpath).get_attribute('value').replace('"', '')

    # --- Print Lines
    get_mailing_dns_records.dkim_record_lines =f"""DKIM Record 
    Type: TXT
    Name: [ default_domainkey ] 
    Value: [ {dkim_record_value_input} ]
    """
    print(get_mailing_dns_records.dkim_record_lines)

    # Click Element - select_mx_button
    select_mx_button = driver.find_element(By.XPATH, select_mx_button_xpath)
    select_mx_button.click()
    time.sleep(5)

    # Scrape/Get Element Attribute - mx_record_name_input
    mx_record_name_input = driver.find_element(By.XPATH, mx_record_name_input_xpath).get_attribute('value')

    # Scrape/Get Element Attribute - mx_record_name_value
    mx_record_name_value = driver.find_element(By.XPATH, mx_record_name_value_xpath).get_attribute('value')

    # --- Print Lines
    get_mailing_dns_records.mx_record_lines =f"""MX Record 
    Type: MX
    Name: [ @ ] 
    Value: [ {mx_record_name_value} ]
    Priority: [ 10 ]
    """
    print(get_mailing_dns_records.mx_record_lines)
    
    driver.quit()


#endregion




#*========================*#
#* Cobra Sniper Functions *#
#*========================*#
#region
#! Function: scrape_targeted_emails_from_results_page_to_text_file()
# Description: This function Scrape Target Emails from a single results page.
def scrape_targeted_emails_from_results_page_to_text_file():
    # Get page text
    page_text = driver.find_element_by_tag_name("body").text
    page_text = page_text.lower()
    # Extract Emails From HTML
    email_regex = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    extracted_emails_list = re.findall(email_regex, page_text)

    # Save Emails to text file
    emails_list_data_text_file_path = "cobra_sniper_emails_list_data.txt" #!ATTENTION
    text_file_obj = open(emails_list_data_text_file_path, "a")
    for email in extracted_emails_list:
        if esp in email:
            text_file_obj.write(email + "\n")
    text_file_obj.close()

    # remove duplicate lines from text file
    unique_lines_list = set(open(emails_list_data_text_file_path).readlines())
    file_data_txt = open(emails_list_data_text_file_path, 'w')
    file_data_txt.writelines(set(unique_lines_list))
    file_data_txt.close()

    # Display Data Count
    emails_data_count = len(unique_lines_list)
    st.write(f"🔄 Extracted Emails :  {emails_data_count}")


#! Function: next_page_based_loop()
# Description: This Function Navigate to the next page & scrape targeted emails.
# USING: scrape_targeted_emails_from_results_page_to_text_file()
def next_page_based_loop():
    while len(keywords_list_based_loop.next_page_webelement_list) > 0 :
        # Set Next Page Web Element
        try :
            next_page_webelement = driver.find_element(By.XPATH, next_page_webelement_xpath)
        except:
            print("ATTENTION: Can't see [next_page_webelement] !!")
            break
        # Scroll to Element
        actions = ActionChains(driver)
        actions.move_to_element(next_page_webelement).perform()
        time.sleep(3)
        # scrape_targeted_emails_to_text_file
        scrape_targeted_emails_from_results_page_to_text_file()
        # Click Next Page WebElement
        next_page_webelement.click()
        time.sleep(5)


#! Function: keywords_list_based_loop()
# Description : 
# USING : 
def keywords_list_based_loop():
    for keyword in keywords_list:
        # Navigate to the targeted URL
        search_url = f"https://www.bing.com/search?q=%22{keyword}%22%2B%22%40{esp}%22%2B%22{area}%22&search=&form=QBLH"
        driver.get(search_url)
        time.sleep(3)
        # Next Page Element List
        keywords_list_based_loop.next_page_webelement_list = driver.find_elements(By.XPATH, next_page_webelement_xpath)
        next_page_based_loop()

#endregion


#*========================*#
#* Cobra Sender Functions *#
#*========================*#
#region

### !📦Function: Send Campaign ###
#!▶️▶️▶️

#%%
def send_campaign(uploaded_emails_list):
    send_count = 0
    sending_report = "Sending Process ..."
    targeted_emails_list = uploaded_emails_list
    # Targeted Emails list
    for targeted_email in targeted_emails_list:
        sending_start_message = f"Sending to : {targeted_email}"

        try:
            #region - Email Content

            # Create MIMEMultipart() object for the Message as "msg"
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = targeted_email
            msg['Subject'] = email_subject
            # Mesage Body as HTML
            msg.attach(MIMEText(msg_html, "html"))
            #endregion

            #region - Connect to Server & Send Email
            with smtplib.SMTP(host=f"mail.{sender_domain}", port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(sender_email, sender_email_password)
                smtp.sendmail(msg['From'], [msg['To'],], msg.as_string())

        #endregion
        except:
            failure_retry_report = f"[-] Unknown Sending Issue !? > Retry sending to: {targeted_email} "
            print(failure_retry_report)
            st.warning(failure_retry_report)
            
            continue

        # Sent to
        send_count += 1
        nl = "\n"
        sending_success_message = f"Email Sent to: {targeted_email}"
        send_count_message = f"Campaign sent to [ {send_count} ] Emails"
        sending_report = f"{sending_start_message} - {sending_success_message} // {send_count_message}"
        print(sending_report)
        st.success(sending_report)

#%%
#endregion


#*=======================*#
#* Page Config Functions *#
#*=======================*#
#region

### !📦Function: config_dictionary_generator ###
#!▶️▶️▶️
def config_dictionary_generator():
    parser = ConfigParser()
    parser.read("config.ini")
    config_dictionary = {}
    for section in parser.sections():
        config_dictionary[section] = {}
        for option in parser.options(section):
            config_dictionary[section][option] = parser.get(section, option)
    return config_dictionary


### !📦Function: generate_config_sections_tuple ###
#!▶️▶️▶️
def generate_config_sections_tuple():
    parser = ConfigParser()
    parser.read("config.ini")
    config_sections_list = parser.sections()
    config_sections_tuple = tuple(config_sections_list)
    return config_sections_tuple


### !📦Function: generate_config_section_options_tuple ###
#!▶️▶️▶️
def generate_config_section_options_tuple(section):
    parser = ConfigParser()
    parser.read("config.ini")
    config_section_options_list = parser.options(section)
    config_section_options_tuple = tuple(config_section_options_list)
    return config_section_options_tuple

#endregion

#*==================*#
#* UserID Functions *#
#*==================*#
#region



#endregion

#endregion


#*=======================*#
#*=======================*#
#* Streamlit GUI Section *#
#*=======================*#
#*=======================*#
#region

#! Streamlit Page Config
#region
st.set_page_config(
    page_title = 'Cobra Inbox',
    page_icon = '🌀',
    layout = 'wide'
)
#endregion


#! Streamlit Remove App footer
#region 
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
#endregion


#! Streamlit sidebar
#region
menu_option = st.sidebar.selectbox(
    "Cobra Server Menu",
    ("Config", "Cobra Sniper", "Cobra Builder", "Cobra Sender", "Cobra Report", "Contact")
)
#endregion



#! GUI Header Container Creation
#region 
header_container = st.container()
cobra_builder_col1, cobra_builder_col2, cobra_builder_col3 = st.columns(3)
#endregion


#! Header Container
#region 
with header_container:
    header_image = './img/logo2.png'
    st.image(header_image, width=200)
    st.text(f"[ {user_membership_type} ] Version 3.0.1 - By Abdelkarim Ben Mohammadi & Ultra Dev-Team")
#endregion

#! Body Container/Columns
#region 

#!========================!#
#! If Config Option !#
#!========================!#
if menu_option == "Config":
    # Create Subheader Container
    config_subheader_container = st.container()
    with config_subheader_container:
        st.subheader(" ")
        st.subheader("📃 Cobra Server Config")

    # Create Columns
    config_edit_col1, config_edit_col2, config_edit_col3 = st.columns(3)
    with config_edit_col1:
        config_sections_tuple = generate_config_sections_tuple()
        config_section_option = st.selectbox('Config Section :', config_sections_tuple)
        config_save_button = st.button('Save Config')
    with config_edit_col2:
        config_section_options_tuple = generate_config_section_options_tuple(config_section_option)
        config_sections_option_option = st.selectbox('Config Section :', config_section_options_tuple)       
    with config_edit_col3:
        config_value = st.text_input('', placeholder='value')

    if config_save_button:
        config_file = "config.ini"
        parser = ConfigParser()
        parser.read(config_file)
        parser.set(config_section_option, config_sections_option_option, config_value)

        with open(config_file, 'w') as configfile:
            parser.write(configfile)

        config_dictionary = config_dictionary_generator()

        st.write(" ")  
        st.write("📃 Config Data :")
        st.write(config_dictionary) 
    
    else:
        config_dictionary = config_dictionary_generator()

        st.write(" ")  
        st.write("📃 Config Data :")
        st.write(config_dictionary)  


#!=========================!#
#! If Cobra Builder Option !#
#!=========================!#
if menu_option == "Cobra Builder":
    with cobra_builder_col1:
        ### !STEP-1 FORM: CyberPanel Installation ###
        #region 
        # Step-1 Subheader: CyberPanel Installation
        st.subheader(" ")
        st.image("./img/step1.png")
        st.subheader("️CyberPanel Installation ")
        st.subheader(" ")
        # Step-1 Get Installation Guide button
        get_installation_guide_button = st.button('Get Installation Guide')
        if get_installation_guide_button:
            url = 'https://community.cyberpanel.net/docs?category=9&topic=82'
            webbrowser.open_new_tab(url)
            step1_progress = 100
            st.progress(step1_progress)
            st.success('✔️ Process Success %100 - Get Installation Guide')
            "🤖 Just go to CyberPanel install guide and apply the 5 simple steps, to install it on your server."

        ### !STEP-1_2 FORM: Save Your CyberPanel Credential ###
        #region 
        # Step-1-2 subheader: Save Your CyberPanel Credential
        st.subheader(" ")
        cyberPanel_credentials_input = st.text_area('Your CyberPanel Credentials :')
        # Step-1 Submit button
        save_cyberpanel_credentials_button = st.button('Save CyberPanel Credentials')
        if save_cyberpanel_credentials_button:
            # Write CyberPanel Credential to a text file
            with open('cyberpanel_credentials.txt', 'w') as f:
                f.write(cyberPanel_credentials_input)

            # Stats Monitor
            step1_2_progress = 100
            st.progress(step1_2_progress)
            st.success('✔️ Process Success %100 - CyberPanel Credentials Saved to [cyberpanel_credentials.txt] file.')
            "🤖 Now, Let's generate some DNS records in th next step."
        #endregion
        #endregion

    with cobra_builder_col2:
        ### !STEP-2 FORM: Generate DNS A Records ###
        #region 
        # step-2 subheader: Generate DNS A Records
        st.subheader(" ")
        st.image("./img/step2.png")
        st.subheader("️Generate Basic DNS ")
        st.subheader(" ")

        # step-2 Submit button
        generate_basic_dns_records_button = st.button('Generate DNS Records')
        if generate_basic_dns_records_button:
            # Generate Record
            st.text('Generated DNS Records :')
            nl = "\n"
            st.code(f'Type: A {nl}Name: {domain} {nl}IPv4 adress: {server_ip} {nl}TTL: Auto')
            st.code(f'Type: A {nl}Name: mail {nl}IPv4 adress: {server_ip} {nl}TTL: Auto')
            st.code(f'Type: A {nl}Name: www.mail {nl}IPv4 adress: {server_ip} {nl}TTL: Auto')
            st.code(f'Type: CNAME {nl}Name: www {nl}Target: {domain} {nl}TTL: Auto')
            "Don't Forget to set your rDNS (Reverse DNS) on your Linode :"
            # Stats Monitor
            step3_progress = 100
            st.progress(step3_progress)
            st.success('✔️ Process Success %100 - DNS Records Generated')
            "🤖 Now, Go to your cloudflare DNS and put this records."
        #endregion

    with cobra_builder_col3:
        ### !step-3 FORM: Build Mailing Server ###
        #region
 
        #* Step-3 subheader: Build Mailing Server
        #region 
        st.subheader(" ")
        st.image("./img/step3.png")
        st.subheader("️Build Mailing Server ")

        st.subheader(" ")
        #endregion

        # Function Control Running System - Select witch function that you want to run before pressing the Button
        #region
        "Mailing Server Build Processes :"
        update_default_package_option = st.checkbox('Update default Package')
        create_a_website_option = st.checkbox('Create Base Website')
        issue_ssl_option = st.checkbox('Issue SSL')
        Install_wordpress_option = st.checkbox('Install Wordpress')
        issue_ssl_for_mailserver_option = st.checkbox('Issue SSL for Mail Server')
        create_email_account_option = st.checkbox('Create Email Account')
        list_email_account_fix = st.checkbox('List Email Accounts & Fix Errors')
        get_mailing_server_dns_records = st.checkbox('Get/Generate Mailing Server DNS Records - Inbox Booster Elements')
        st.subheader(" ")
        #endregion


        # Step-3 [ Build Mailing Server Button ]
        #region 
        build_mailing_server_button = st.button('Build Mailing Server')
        if build_mailing_server_button:
            #region - Setting Stats Monitor Elements
            # --- Progress Bar
            step4_progress_bar = st.progress(0)
            step4_progress_bar.progress(1)
            # --- info box Message
            step4_info_message = '🔁 Process Start'
            info_box = st.info(step4_info_message)
            time.sleep(1)
            # --- Stats Monitor Block
            #region - SM-Block
            step4_progress_bar.progress(11)
            info_box = st.info('🔁 Loading Data ..')
            time.sleep(1)
            #endregion
            #endregion


            #!Step Functions Call
            #region - Functions


            #region - SM-Block
            step4_progress_bar.progress(15)
            info_box = st.info('🔁 COBRA Engine Autopilote Set Driver')
            time.sleep(1)
            #endregion
            #! Set Driver Function
            set_driver()


            #region - SM-Block 
            step4_progress_bar.progress(31)
            info_box = st.info('🔁 Connect to CyberPanel Server')
            time.sleep(1)
            #endregion
            #! Set Connect to CyberPanel Function
            connect_to_cyberpanel()

            if update_default_package_option:
                #region - SM-Block
                step4_progress_bar.progress(44)
                info_box = st.info('🔁 Updating Mailing Server Default Package ..')
                time.sleep(1)
                #endregion
                #! Update Default Package Function
                update_default_package()

            if create_a_website_option:
                #region - SM-Block
                step4_progress_bar.progress(55)
                info_box = st.info('🔁 Create Base Website for your Email Marketing Server ..')
                time.sleep(1)
                #endregion
                #! Create Website Function
                #create_website()

            if issue_ssl_option:
                #region - SM-Block
                step4_progress_bar.progress(61)
                info_box = st.info('🔁 Process Core SSL')
                time.sleep(1)
                #endregion
                #! Issue SSL
                issue_ssl()

            if Install_wordpress_option:
                #region - SM-Block
                step4_progress_bar.progress(67)
                info_box = st.info('🔁 Install Wordpress ..')
                time.sleep(1)
                #endregion
                #! Install Wordpress
                install_wordpress()

            if issue_ssl_for_mailserver_option:
                #region - SM-Block
                step4_progress_bar.progress(67)
                info_box = st.info('🔁 Process Mail-Server SSL')
                time.sleep(1)
                #endregion
                #! Issue ssl for mail server
                issue_ssl_for_mail_server()

            if create_email_account_option:
                #region - SM-Block
                step4_progress_bar.progress(71)
                info_box = st.info('🔁 Create Email Account ..')
                time.sleep(1)
                #endregion
                #! Create email account page
                create_email_account()

            if list_email_account_fix:
                #region - SM-Block
                step4_progress_bar.progress(75)
                info_box = st.info('🔁 List Email Account')
                time.sleep(1)
                #endregion
                #! List email account page
                list_email_account()

            if get_mailing_server_dns_records:
                #region - SM-Block
                step4_progress_bar.progress(79)
                info_box = st.info('🔁 Generate Mailing Server Core DNS DATA ..')
                time.sleep(1)
                #endregion
                #! Add Modify DNS Zone / Get Mailing Server DNS Records
                get_mailing_dns_records()
                st.code(get_mailing_dns_records.spf_record_lines)
                st.code(get_mailing_dns_records.dmarc_record_lines)
                st.code(get_mailing_dns_records.dkim_record_lines)
                st.code(get_mailing_dns_records.mx_record_lines)


            #region - SM-Block
            step4_progress_bar.progress(100)
            info_box = st.info('🔁 Generating SMTP Server info ..')
            time.sleep(1)
            #endregion

            st.code(f"""SMTP Details:
            Server Hostname - mail.{domain}
            Port - 25
            Port - 587 (SSL)
            Port - 465 (SSL)
            SSL - STARTTLS
            """)


            #region - Process Success Message
            info_box = st.success('✔️ Process Success %100 - Mailing Server Built up.')
            f"🤖 Good Job {user_name}, Mailing Server Built up, all package elements updated and ready for work."
            "⚠️ ATTENTION: "
            "1 - You have to add the Generated SPF / DMARC / DKIM / MX Records to your DNS Records"
            "2 - You can test the performance of your Email Marketing server right now .. "

        st.subheader("️ ")

        "Launch WebMail Service to send Emails and test the performance of your mailing server :"
        launch_web_mail_button = st.button("Launch WebMail")
        if launch_web_mail_button:
            webbrowser.open_new_tab(f"https://{server_ip}:8090/rainloop/index.php")
        " "
        "Launch Mail-Tester.com service to test the Inbox score & quality of your mailing server :"
        launch_mailtester_button = st.button("Launch Mail Tester")
        if launch_mailtester_button:
            webbrowser.open_new_tab("https://www.mail-tester.com")
        " "

            #endregion
        #endregion

        #endregion

        #endregion


#!========================!#
#! If Cobra Sniper Option !#
#!========================!#
if menu_option == "Cobra Sniper":
    st.subheader("🎯 Get targeted Emails Data")
    cobra_sniper_col1, cobra_sniper_col2, cobra_sniper_col3 = st.columns(3)
    with cobra_sniper_col1:
        targeted_esp_text_input = st.text_input('', placeholder='Targeted ESP - ex:gmail.com')
        esp = targeted_esp_text_input
        targeted_area_text_input = st.text_input('', placeholder='Targeted Area - ex:usa')
        area = targeted_area_text_input
    uploaded_keywords_list_file = st.file_uploader('📥 Keywords List Data File to use in this Campaign :')

    if uploaded_keywords_list_file is not None:
        # Store file content as binary in "raw_bytes_text" object/variable
        raw_bytes_text = uploaded_keywords_list_file.read() #binary
        raw_string_text = str(raw_bytes_text).replace("b'", "")
        raw_string_text = raw_string_text.replace(r"\r\n'", "")
        uploaded_Keywords_list = raw_string_text.split(r"\r\n")
        # Free Version Limit
        #region 
        free_version_keywords_data_volume_limit = 500
        if user_membership_type == "Free" and len(uploaded_Keywords_list) > free_version_keywords_data_volume_limit :
            st.error(f"ERROR[Data-Volume]: You can't use more than {free_version_keywords_data_volume_limit} keywords in the Free Version !!")
            print((f"ERROR[Data-Volume]: You can't use more than {free_version_keywords_data_volume_limit} keywords in the Free Version !!"))
            uploaded_Keywords_list = []
        #endregion

        
        
        # Print Keywords List Number
        st.success(f"✔️ You have {len(uploaded_Keywords_list)} Keywords in this campaign list.")

    # Extract Emails Button
    extract_targeted_emails_data_button = st.button("Extract Targeted Emails Data")
    if extract_targeted_emails_data_button:
        keywords_list = uploaded_Keywords_list
        set_driver()
        keywords_list_based_loop()
            



#!========================!#
#! If Cobra Sender Option !#
#!========================!#
if menu_option == "Cobra Sender":
    st.subheader("️🎯 Send Campaign ")
    # Email Subject Input
    email_subject_input = st.text_input('' ,placeholder="Email Subject")
    email_subject = email_subject_input

    # Email Body Input
    email_body_input = st.text_area('' ,placeholder="Email Body (HTML) ...")
    msg_html = email_body_input

    # Upload Emails List text File
    uploaded_emails_list_file = st.file_uploader("📥 Choose Emails List Data File to use in this Campaign :")
    
    if uploaded_emails_list_file is not None:
        # Store file content as binary in "raw_bytes_text" object/variable
        raw_bytes_text = uploaded_emails_list_file.read() #binary
        # Decode binary to string
        encoding = 'utf-8'
        list_text = raw_bytes_text.decode(encoding) #string
        uploaded_emails_list = list_text.split()
        
        # Print Emails List Number
        st.write(f"✔️ You have {len(uploaded_emails_list)} emails in this campaign list.")


    send_campaign_button = st.button('Send Campaign')
    if send_campaign_button:
        send_campaign(uploaded_emails_list)


#!========================!#
#! If Cobra Report Option !#
#!========================!#
if menu_option == "Cobra Report":
    st.subheader("️🎯 Boost Reporting ")
    st.image("img/under.png")




#endregion






#endregion