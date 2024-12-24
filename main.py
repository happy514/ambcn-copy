from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=chrome_options)

#目标网站接口
BASE_URL = "https://exp.com/archives_data.php?project_id="

#id范围（整数不超过999）
PROJECT_ID_START = 0
PROJECT_ID_END = 10

#内容存储位置
SAVE_DIRECTORY = "C:\\example\\example"

if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)

substantial_content_count = 0
no_substantial_content_count = 0

def scrape_data(project_id):
    global substantial_content_count
    global no_substantial_content_count
    project_id_with_prefix = f"AMB-{project_id:03d}"
    url = BASE_URL + project_id_with_prefix
    try:
        driver.get(url)
        time.sleep(2) 
        page_source = driver.page_source
        
        #过滤被删除的内容
        if "该档案已被覆盖" in page_source:
            no_substantial_content_count += 1
            print(f"Project ID {project_id_with_prefix} has no substantial content. Skipping...")
        else:
            substantial_content_count += 1
            file_path = os.path.join(SAVE_DIRECTORY, f"page_{project_id}.html")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(page_source)
            print(f"Successfully saved Project ID {project_id_with_prefix} to {file_path}")
    except Exception as e:
        print(f"Failed to retrieve Project ID {project_id_with_prefix}: {e}")

def main():
    for project_id in range(PROJECT_ID_START, PROJECT_ID_END + 1):
        scrape_data(project_id)
    print(f"Total pages with substantial content: {substantial_content_count}")
    print(f"Total pages with no substantial content: {no_substantial_content_count}")

if __name__ == "__main__":
    main()

driver.quit()
