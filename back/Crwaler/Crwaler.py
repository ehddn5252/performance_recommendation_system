import copy
import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm


class Crwaler:
    driver = webdriver.Chrome()
    new_df = pd.DataFrame(columns=["1"])
    #musical_name = "캣츠"
    crwaling_num= 5
    def __init__(self):
        print("Crwaler class is generated")

    '''
    @property
    def musical_name(self):
        return self.musical_name
    '''

    '''
    @musical_name.setter
    def musical_name(self,input_musical_name):
        self.musical_name = input_musical_name
    '''

    # naver
    @classmethod
    def nav(cls,musical_name):
        text = "뮤지컬 " + str(musical_name)
        # new_df = copy.deepcopy(pd.DataFrame(columns=["1"]))
        url = 'https://section.blog.naver.com/Search/Post.nhn?pageNo='+ str(1) + '&rangeType=ALL&orderBy=sim&keyword=' + text
        cls.driver.get(url)
        time.sleep(0.5)

        url_list = []
        for j in range(1, cls.crwaling_num+1): # 각 블로그 주소 저장
            titles = cls.driver.find_element_by_xpath('/html/body/ui-view/div/main/div/div/section/div[2]/div['+str(j)+']/div/div[1]/div[1]/a[1]')
            title = titles.get_attribute('href')
            #print(title)
            url_list.append(title)

        print("url 수집 완료,\n 해당 url의 본문  데이터 크롤링")

        for url in url_list: # 수집한 url 만큼 반복
            cls.driver.get(url) # 해당 url로 이동

            cls.driver.switch_to.frame('mainFrame')
            overlays = ".se-component.se-text.se-l-default" # 내용 크롤링
            contents = cls.driver.find_elements_by_css_selector(overlays)
            content_list = ""
            for content in contents:
                content_list = content_list + content.text
            new_data = {}
            new_data = {"1":content_list}
            cls.new_df = cls.new_df.append(new_data, ignore_index=True)
        return cls.new_df

    # tistory
    @classmethod
    def tis(cls,musical_name):
        text = "뮤지컬 " + str(musical_name)
        #self.new_df = pd.DataFrame(columns=["1"])

        url = f'https://www.google.com/search?q={text}+tistory.com'
        cls.driver.get(url)
        time.sleep(1)
        # /html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[3]/div/div/div[1]/a

        try:
            url_list=[]
            for j in range(1, cls.crwaling_num+1): # 각 블로그 주소 저장
                titles = cls.driver.find_element_by_xpath(f'/html/body/div[7]/div/div[8]/div[1]/div/div[2]/div[2]/div/div/div[{str(j)}]/div/div/div[1]/a')

                title = titles.get_attribute('href')
                url_list.append(title)
        except:
            pass

        print("url 수집 완료,\n 해당 url의 본문  데이터 크롤링")
        time.sleep(1)

        for url in url_list: # 수집한 url 만큼 반복
            cls.driver.get(url) # 해당 url로 이동

            # driver.switch_to.frame('mainFrame')
            # overlays = ".se-component.se-text.se-l-default" # 내용 크롤링
            overlays = "#content > div.inner > div.entry-content > div"
            contents = cls.driver.find_elements_by_tag_name('p')
            content_list=""

            for content in contents:
                content_list = content_list + content.text
            #new_data={}
            new_data = {"1":content_list}
            cls.new_df = cls.new_df.append(new_data, ignore_index=True)
            time.sleep(5)
        return cls.new_df

    # here to use youtube

    @classmethod
    def move_url(cls,URL):
        ''' 입력한 URL로 이동한다.
            안써도 될듯

        Parameters:
            URL(str) : 이동할URL
        Returns:
        X
        '''
        # url로 이동
        cls.driver.get(URL)
        #웹 페이지가 넘어올 때까지 3초 기다린다.
        cls.driver.implicitly_wait(3)
        time.sleep(3)

    @staticmethod
    def youtube_search(keyword)->None:
        '''youtube에서 search할 항목을 찾는다.
            안써도 될듯

        Paramters:
            keyword(str) : 검색할 keyword
        Returns:
            X
        '''
        # youtube search
        search_keyword_encode = requests.utils.quote(keyword)
        url = "https://www.youtube.com/results?search_query=" + search_keyword_encode


    @classmethod
    def get_videos_url(cls,keyword,vidoe_count=3)->None:
        ''' 검색한 keyword의 모든 video의 title과 url을 가져온다.

        Paramters:
            keyword(str): 검색할 keyword
        Returns:
            X
        '''
        titles = []
        urls = []

        search_keyword_encode = requests.utils.quote(keyword)

        url = "https://www.youtube.com/results?search_query=" + search_keyword_encode
        #driver = wd.Chrome(executable_path="chromedriver.exe")
        cls.driver.get(url)

        html_source = cls.driver.page_source
        count=0
        soup = BeautifulSoup(html_source, 'lxml')
        datas = soup.select("a#video-title")

        for data in datas:
            if count == vidoe_count:
                break
            title = data.text.replace('\n', '')
            url = "https://www.youtube.com/" + data.get('href')
            count += 1
            titles.append(title)
            urls.append(url)
        return titles, urls

    @classmethod
    def scroll(cls,direction = "down")->None:
        """
        :desc:
        스크롤을 아래로 내린다.
        :param direction: down으로 할 시 아래로 스크롤 한다.

        """
        # 300사이즈가 댓글 보일 수 있는 정도의 scroll 크기
        if direction=="down":
            cls.driver.execute_script("window.scrollTo(0, 300);")
        else:
            cls.driver.execute_script("window.scrollTo(0, 0);")

        time.sleep(3)

    @classmethod
    def scroll_end_page(cls)->None:
        """
        :desc:
        스크롤을 페이지 끝까지 내린다.

        """
        last_height = cls.driver.execute_script("return document.documentElement.scrollHeight")

        while True:
            cls.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(1.5)

            new_height = cls.driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(1)

    @classmethod
    def close_pop_up(cls,pop_up_selector="#dismiss-button > a")-> None:
        '''
        :desc:
        팝업을 닫는다.

        :param pop_up_selector: 닫을 pop up의 selector이다.

        '''
        # 팝업 닫기
        try:
            cls.driver.find_element_by_css_selector(pop_up_selector).click()
        except:
            pass

    @classmethod
    def open_coments_coment(cls)->None:
        ''' youtube 영상이 있는 위치에서 대댓글을 모두 연다.
        '''
        # 대댓글 모두 열기
        buttons = cls.driver.find_elements_by_css_selector("#more-replies > a")
        time.sleep(1.5)

        for button in buttons:
            try:
                button.send_keys(Keys.ENTER)
                time.sleep(1.5)
                button.click()
            except:
                print('open_coments_coment except')
        time.sleep(1.5)

    @classmethod
    def extract_id_comment(cls, id_selector="div#header-author > h3 > #author-text > span", comment_selector = "yt-formatted-string#content-text")->list:
        ''' 유튜브 id와 comment selector에 매칭되는 text를 가져와서 list에 저장후 return한다. 직접 사용할 때 이와 같이 사용할 것이므로 일단 일반화는 pass
            이렇게 쓸꺼면 사실 Parameter도 필요없는데 나중에 일반화 할때 생각나라고 일단 써줬다.

        Paramters:
            id_selector(str) : 댓글 id selector
            comment_selecotr(str) : 댓글의 comment selector

        Returns:
            id_list(list) : 가져온 댓글 id들이 들어있는 list
            comment_list(list) : 가져온 댓글 comment 들이 들어있는 list

        '''
        # 정보 추출하기
        html_source = cls.driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        id_list = soup.select(id_selector)
        comment_list = soup.select(comment_selector)
        return id_list,  comment_list

    @classmethod
    def extract_object(cls,selector = "#count > ytd-video-view-count-renderer > span.view-count.style-scope.ytd-video-view-count-renderer")->list:
        '''selector에 맞는 객체 가져온다. (default 값은 조회수를 가져오는 것이다.)
            bs4의 selcet를 사용해서 list를 반환한다.

        Parameters:
            selector : 가져올 것의 selector
        Returns:
            object : selector에 맞는 object를 가져온 list
        '''
        html_source = cls.driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        object = soup.select(selector)
        return object


    @staticmethod
    def data_preprocessing(id_list:list,comment_list:list)->tuple:
        '''
        :desc:
        댓글에 \n이나 \t '    ' 와 같은 필요없는 데이터를 제거해준다. in youtube crwaler

        Paramters:
            id_list : 앞의 extract_id_comment()함수에서 return한 댓글 id list이다.
            comment_list : 앞의 extract_id_comment()함수에서 return한 댓글 이다.
        Returns:
            id_final(list) : 필요없는 데이터 제거된 id list
            comment_final(list) : 필요없는 데이터 제거된 comment
        '''

        id_final = []
        comment_final = []

        for i in range(len(comment_list)):

            temp_id = id_list[i].text
            temp_id = temp_id.replace('\n', '')
            temp_id = temp_id.replace('\t', '')
            temp_id = temp_id.replace('    ', '')
            id_final.append(temp_id)

            temp_comment = comment_list[i].text
            temp_comment = temp_comment.replace('\n', '')
            temp_comment = temp_comment.replace('\t', '')
            temp_comment = temp_comment.replace('    ', '')
            comment_final.append(temp_comment)
        return id_final,comment_final

    @classmethod
    def youtube_comment_crwaler(cls,musical_name):

        # 시작과 끝번호 정하기
        try:
            # 공연명 가져오고 분할하고 싶을 때는 iloc[start:end] 를 사용하면 된다.
            musical_name = "뮤지컬 " + str(musical_name)
            titles, urls = cls.get_videos_url(musical_name, vidoe_count=cls.crwaling_num)

            for title, url in zip(titles, urls):
                # new_df = pd.DataFrame(columns=["1"])
                cls.move_url(url)
                # 제목에 맞는 column 생성
                cls.scroll("down")
                cls.scroll_end_page()

                id_list, comment_list = cls.extract_id_comment()

                # comment 전처리
                _, comment_final = cls.data_preprocessing(id_list, comment_list)
                coment_num = 0
                for comment in comment_final:
                    if coment_num>5:
                        break
                    coment_num+=1

                    new_data = {"1" : comment}
                    cls.new_df = cls.new_df.append(new_data,ignore_index=True)

            return cls.new_df
        except:
            pass
        return pd.DataFrame()
