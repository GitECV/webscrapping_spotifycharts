from services.database_connection import DBConnection
from utils.string_utils import StringUtils
from logs.logs import Logs
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import yaml

with open('configuration_data.yaml') as f:
    config = yaml.safe_load(f)

# Connection
dbConnection = DBConnection.database_cursor()


class ChartsService:
    @staticmethod
    def spotify_scrap():
        global driver
        try:
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=options)
            driver.get("https://charts.spotify.com/home")
            time.sleep(1)

            log_in = driver.find_element(By.XPATH,
                                         "//div[@class='ButtonInner-sc-14ud5tc-0 iMWZgy encore-bright-accent-set']")
            log_in.click()
            time.sleep(1)
        except ValueError:
            Logs.critical("ChartsDAO - SpotifyCharts get into login: ", ValueError)

        try:
            username_input = driver.find_element(By.XPATH, "//input[@id='login-username']")
            password_input = driver.find_element(By.XPATH, "//input[@id='login-password']")
            button_log_in = driver.find_element(By.XPATH,
                                                "//span[@class='ButtonInner-sc-14ud5tc-0 cJdEzG encore-bright-accent-set']")

            username_input.send_keys(config["SpotifyUsername"])
            password_input.send_keys(config["SpotifyPassword"])
            button_log_in.click()

            time.sleep(2)
        except ValueError:
            Logs.critical("ChartsDAO - SpotifyCharts cannot load: ", ValueError)

        try:
            accept_cookies = driver.find_element("xpath", "//button[@id='onetrust-accept-btn-handler']")
            accept_cookies.click()

            time.sleep(1)

            all_countrys_list = ['global', 'ar', 'au', 'at', 'by', 'be', 'bo', 'br', 'bg', 'ca', 'cl', 'co', 'cr',
                                 'cy', 'cz', 'dk', 'do', 'ec', 'eg', 'sv', 'ee', 'fi', 'fr', 'de', 'gr', 'gt',
                                 'hn', 'hk', 'hu', 'is', 'in', 'id', 'ie', 'il', 'it', 'jp', 'kz', 'lv', 'lt',
                                 'lu', 'my', 'mx', 'ma', 'nl', 'nz', 'ni', 'ng', 'no', 'pk', 'pa', 'py', 'pe',
                                 'ph', 'pl', 'pt', 'ro', 'sa', 'sg', 'sk', 'za', 'kr', 'es', 'se', 'ch', 'tw',
                                 'th', 'tr', 'ae', 'ua', 'gb', 'uy', 'us', 've', 'vn']

            for country in all_countrys_list:
                first_url_part = "https://charts.spotify.com/charts/view/regional-"
                second_url_part = "-daily/latest"
                driver.get(first_url_part + country + second_url_part)
                time.sleep(1)

                getAllTr = driver.find_elements(By.XPATH, '//tr[@class="TableRow__TableRowElement-sc-1kuhzdh-0 bANOpw styled__StyledTableRow-sc-135veyd-3 lsudt"]')
                for row in getAllTr:
                    today = datetime.today()
                    dtDatetime = today
                    sPlaylist = country
                    sIdSong = row.find_element(By.XPATH, './/a[@target="_blank"][@rel="noopener noreferrer"]').get_attribute("href")
                    iChartPosition = StringUtils.string_to_insertion(row.find_element(By.XPATH, './/span[@aria-label="Current position"]'), 'int')
                    sSongName = StringUtils.string_to_insertion(row.find_element(By.XPATH, './/span[@class="styled__StyledTruncatedTitle-sc-135veyd-22 kKOJRc"]'), 'str')
                    sArtistName = StringUtils.string_to_insertion(row.find_element(By.XPATH, './/a[@class="styled__StyledHyperlink-sc-135veyd-25 bVVLJU"]'), 'str')
                    iPeak = StringUtils.string_to_insertion(row.find_elements(By.XPATH, './/td[@class="TableCell__TableCellElement-sc-1nn7cfv-0 dLdEGj styled__RightTableCell-sc-135veyd-4 kGfYTK"]')[0], 'int')
                    iPrevPosition = StringUtils.string_to_insertion(row.find_elements(By.XPATH, './/td[@class="TableCell__TableCellElement-sc-1nn7cfv-0 dLdEGj styled__RightTableCell-sc-135veyd-4 kGfYTK"]')[1].find_element(By.XPATH, './/span'), 'str')
                    iStreak = StringUtils.string_to_insertion(row.find_elements(By.XPATH, './/td[@class="TableCell__TableCellElement-sc-1nn7cfv-0 dLdEGj styled__RightTableCell-sc-135veyd-4 kGfYTK"]')[2], 'int')
                    iStreams = StringUtils.string_to_insertion(row.find_element(By.XPATH, './/td[@class="TableCell__TableCellElement-sc-1nn7cfv-0 kJgiFu styled__RightTableCell-sc-135veyd-4 kGfYTK"]'), 'streams')

                    hacer_click = row.find_element(By.XPATH, './/td[@class="TableCell__TableCellElement-sc-1nn7cfv-0 cltvtH"]')
                    hacer_click.click()
                    time.sleep(0.7)

                    dtReleaseDate = None
                    dtFirstEntryDate = None
                    iFirstEntryPosition = None
                    iTotalDaysOnChart = None


                    table_element = driver.find_element(By.XPATH,
                                                        '//table[@class="Table__TableElement-evwssh-0 jaKCLL ExpandedRowTable__StyledTable-aasrut-0 duqHvH"]')
                    tbody_element = table_element.find_element(By.TAG_NAME, 'tbody')
                    tr_elements = tbody_element.find_elements(By.TAG_NAME, 'tr')
                    for tr_element in tr_elements:
                        div_elements = tr_element.find_elements(By.TAG_NAME, 'div')
                        if div_elements[0].text == "Release Date":
                            dtReleaseDate = StringUtils.string_to_insertion(div_elements[1], 'date')
                        if div_elements[0].text == "First entry date":
                            dtFirstEntryDate = StringUtils.string_to_insertion(div_elements[1], 'date')
                        if div_elements[0].text == "First entry position":
                            iFirstEntryPosition = StringUtils.string_to_insertion(div_elements[1], 'int')
                        if div_elements[0].text == "Total days on chart":
                            iTotalDaysOnChart = StringUtils.string_to_insertion(div_elements[1], 'int')

                    new_chart = (
                    dtDatetime, sPlaylist, sIdSong, iChartPosition, sSongName, sArtistName, iPeak, iPrevPosition,
                    iStreak, iStreams, dtReleaseDate, dtFirstEntryDate, iFirstEntryPosition, iTotalDaysOnChart)
                    insertion_query = "INSERT INTO GlobalDailyChart(dtDatetime, sPlaylist, sIdSong, iChartPosition, sSongName, sArtistName, iPeak, sPrevPosition, iStreak, iStreams, dtReleaseDate, dtFirstEntryDate, iFirstEntryPosition,iTotalDaysOnChart) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    dbConnection.execute(insertion_query, new_chart)
                    dbConnection.commit()
        except ValueError:
            Logs.critical("ChartsDAO - SpotifyCharts add to database: ", ValueError)
        dbConnection.close()
