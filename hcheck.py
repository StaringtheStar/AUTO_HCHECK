from selenium import webdriver
# Selenium WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# for WAIT function
import datetime as dt

# ========= CONSTANTS ========= #
yymmdd = dt.date.today().strftime('%y%m%d')
print(yymmdd)
# date
driverpath = 'chromedriver'
# Webdriver path
hcheckurl = 'https://eduro.cne.go.kr/stv_cvd_co00_002.do'
# hcheck initial url
hchecksur = 'https://eduro.cne.go.kr/stv_cvd_co00_000.do'
# hcheck survey url
hcheckend = 'https://eduro.cne.go.kr/stv_cvd_co02_000.do'
# hcheck result url
h_school = 'N100002870'
# school code, input schulCode

# ===== WEBDRIVER OPTIONS ===== #
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
# ChromeDriver, no-sandbox headless FHD


driver = webdriver.Chrome(driverpath, options=options)
# define driver


def el_by_id(id):
    # get element by id
    return driver.find_element_by_id(id)


def idclick(id):
    # click by id
    # return error or false
    try:
        driver.execute_script('arguments[0].click();', el_by_id(id))
    except Exception as err:
        print(err.args)
        print(err)
        return err
    else:
        return False


def idvalset(id, val):
    # set value of attr by id
    # return error or false
    try:
        driver.execute_script(f'arguments[0].setAttribute("value", "{val}");',
                              el_by_id(id))
    except Exception as err:
        print(err.args)
        print(err)
        return err
    else:
        return False


def errlog(name, error):
    # log error at YYMMDDNAME.log
    with open(yymmdd + name + '.log', 'a') as f:
        f.write(str(error) + '\n')


class hcheck():
    def __init__(self):
        self.yymmdd = yymmdd
        # print('HCHECK START')

    def check(self, name, date):
        # input: name, date(birth)

        driver.get(hcheckurl)
        # move to info input

        infos = [['schulCode', h_school],
                 ['pName', name],
                 ['frnoRidno', date]]
        # school code
        # student name
        # student birth

        for info in infos:
            err = idvalset(info[0], info[1])
            if err:
                errlog(name, err)
                return False

        err = idclick('btnConfirm')
        if err:
            errlog(name, err)
            return False

        # submit, move to survey site

        WebDriverWait(driver=driver, timeout=5).until(
            EC.presence_of_element_located((By.ID, 'rspns091')))
        # wait until webpage loads(check by last radiobutton)

        rspns = ['rspns011',
                 'rspns02',
                 'rspns070',
                 'rspns080',
                 'rspns090',
                 'btnConfirm']
        # fever, symptoms, oversea, familyoversea, familyquarantine + submit

        for rspn in rspns:
            err = idclick(rspn)
            if err:
                errlog(name, err)
                return False

        try:
            WebDriverWait(driver=driver, timeout=5).until(
                EC.url_to_be(hcheckend))
        except TimeoutException:
            return False
        # wait until webpage moves to result page

        # driver.get_screenshot_as_file(
        #     'sr_' + yymmdd + '/' + name + '.png')
        # save result as image: survey_result/YYMMDD/NAME.png
        return True
        # True if no error

    def checkend():
        # clear driver
        driver.close()
        driver.quit()
