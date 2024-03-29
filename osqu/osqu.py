#!/usr/bin/env python3
##################################################
#                     osqu                       #
#      https://github.com/franjsco/osqu          #
#                   @franjsco                    #
##################################################

# Built-in
import re
import traceback

# Libs
from colored import fg, bg, attr
from tabulate import tabulate
from requests_html import HTMLSession

# Modules
from . import utils
from . import errors


def fetch_data_from_openqa():
    URL="https://openqa.opensuse.org/group_overview/1"

    sel_xpath_builds = "//div[@id='build-results']/div"
    sel_xpath_build_name = "div[1]//span/a/text()"
    sel_xpath_build_date = "div[1]//*/abbr/@title"
    sel_xpath_build_published_flag= "div[1]//*/i[@title='published']/text()"
    sel_xpath_build_dashboard = "//div[2]/div[contains(@class,'build-dashboard')]/@title"

    builds = []

    try:
        session = HTMLSession()
        res = session.get(URL)
        res.html.render()
    except:
        raise errors.FetchError
 
    try:
        for build in res.html.xpath(sel_xpath_builds):
            dashboard = ''.join(build.xpath(sel_xpath_build_dashboard)).split("\n")
            buildname = ''.join(build.xpath(sel_xpath_build_name))
            date = ''.join(build.xpath(sel_xpath_build_date))[:10]
            published = 'Yes' if ''.join(build.xpath(sel_xpath_build_published_flag)) else 'No'

            regexp_total = re.compile("total")
            regexp_passed = re.compile("passed")

            total_test =  int(''.join(list(filter(regexp_total.match, dashboard))).split(":")[1])
            passed_test = int(''.join(list(filter(regexp_passed.match, dashboard))).split(":")[1])
           
            percent_passed_test = round(passed_test / total_test * 100)

            builds.append({
                'S': ' ',
                'Build': buildname,  
                'Date':  date,
                'Published': published,
                'Passed test': '{0}% ({1}/{2})'.format(percent_passed_test, passed_test, total_test)
            })
    except:
        raise errors.SelectorError

    return builds


def main():
    openqa_data = None
    current_version = None
    latest_version = None
    final_table = None

    try:
        print('%sopenSUSE QA Updates (osqu) %s' % (fg("#73ba25"), attr(0)))
        
        if utils.is_openSUSE_tumbleweed():
            print("Tumbleweed detected")

        print("Fetching data from openQA... \n")

        openqa_data = fetch_data_from_openqa()
        current_version = utils.get_installed_version()
        latest_version = utils.get_latest_released_version(openqa_data)
        final_table = utils.add_installed_flag_on_table(openqa_data, current_version) 

        print(tabulate(final_table, headers="keys", tablefmt="presto", disable_numparse=True), "\n")     

        if utils.is_openSUSE_tumbleweed():
            print("Current", current_version)
            print("Latest ", latest_version)       

        if utils.is_upgradable(current_version, latest_version):
            choice = input('%sDo you want update to latest version? [y/n] (n): %s' % (attr(1), attr(0)))
            
            if choice.upper() == 'Y':
                utils.launch_upgrade()

    except errors.FetchError:
        print("Fetch aborted")
        traceback.print_exc()
    except errors.SelectorError:
        print("Selector aborted")
        traceback.print_exc()
    except Exception:
        print("Error")
        traceback.print_exc()



if __name__ == "__main__":
    main()