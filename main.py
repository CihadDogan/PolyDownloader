import poly_scrapper as ps
import file_manager as fm
import time
import datetime
import re
import os

def replace_non_ascii(unicode_string):

    real = re.sub('[\W_]+', '', unicode_string)
    real = real.replace(" ", "")

    return real

def main():
    """ Start point of app """

    # Driver path
    driverPath = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver_win32/chromedriver.exe'

    # Objects
    objFileManager = fm.FileManager()
    objScrapper = ps.PolyScrapper(driverPath)

    # Get words to search from file (words.txt)
    searchTexts = objFileManager.read_all_words()
    for i in range(len(searchTexts)):
        searchTexts[i] = searchTexts[i].rstrip()

    # Count of max download per searched text.
    maxDownloadCountPerItem = 50

    for searchText in searchTexts:
        print("--------------------> Searching:" + searchText)

        # Create sub folder in destinationPath
        objFileManager.create_folder(searchText)

        # Search
        objScrapper.search(searchText)
        time.sleep(4)

        # Filter founded items
        objScrapper.filter()
        time.sleep(2)

        # Get founded total item count
        itemCount = int(objScrapper.get_item_count())
        maxItemCount = maxDownloadCountPerItem
        if itemCount < maxDownloadCountPerItem:
            maxItemCount = itemCount
        print("--------------------> ItemCount:" + str(itemCount))
        
        # Scroll a couple times to load enough item to screen.
        objScrapper.scroll_down()
        time.sleep(1)
        objScrapper.scroll_down()
        time.sleep(1)
        objScrapper.scroll_down()
        time.sleep(1)
        objScrapper.scroll_down()
        time.sleep(1)

        # Download all founded items one by one
        for index in range(maxItemCount):
            realIndex = index + 1
            print("Index:" + str(realIndex) + " at " + str(datetime.datetime.now()))

            # Click Item
            isClickSuccess = objScrapper.click_element(realIndex)
            if isClickSuccess:
                time.sleep(2)

                isPageExist = objScrapper.is_page_exist()

                if isPageExist:
                    
                    # Remove non-ascii characters from name
                    name = objScrapper.get_name()
                    name = replace_non_ascii(name)

                    # Is item already downloaded?
                    isFileExist = objFileManager.has_file(name, searchText)

                    #
                    if isFileExist == False:
                        isSuccess = objScrapper.download()
                        if isSuccess:
                            # Wait until download finish
                            while True:
                                if objFileManager.is_download_finished() == True:
                                    break
                                time.sleep(0.25)

                            # Move downloaded file to correct folder
                            objFileManager.create_folder(searchText)
                            objFileManager.cut_and_paste_last_file(searchText, name)
                        else:
                            print("Download failed")
                            objScrapper.return_to_first_tab()
                    else:
                        print("File already exist")
                        objScrapper.return_to_first_tab()
                else:
                    print("File already exist")
                    objScrapper.return_to_first_tab()
            #
            time.sleep(0.5)

    objScrapper.quit()
    print("ALL DONE!")

if __name__ == "__main__":
    main()