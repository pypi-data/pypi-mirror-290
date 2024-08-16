import LibHanger.Library.uwLogger as Logger
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
from LibHanger.Library.uwGlobals import *
from Scrapinger.Library.baseWebBrowserController import baseWebBrowserController
from Scrapinger.Library.scrapingConfig import scrapingConfig

class browserContainer:
    
    """
    ブラウザコンテナクラス
    """

    class beautifulSoup(baseWebBrowserController):
    
        """
        beautifulSoup用コンテナ
        """
    
        def __init__(self, _config: scrapingConfig):
            
            """
            コンストラクタ
            
            Parameters 
            ----------
            _config : scrapingConfig
                共通設定クラス

            """
            
            # 基底側コンストラクタ呼び出し
            super().__init__(_config)
    
    class chrome(baseWebBrowserController):
        
        """
        GoogleCheromブラウザコンテナ
        """
        
        def __init__(self, _config:scrapingConfig):
            
            """
            コンストラクタ
            
            Parameters 
            ----------
            _config : scrapingConfig
                共通設定クラス

            """
            
            # 基底側コンストラクタ呼び出し
            super().__init__(_config)

        def __del__(self):
            
            """
            デストラクタ
            """
            
            if self.wDriver != None:
                # webdriver - quit
                self.wDriver.quit()
                # ログ出力
                Logger.logging.info('chrome webdriver is quit.')
            
        def getWebDriver(self):
            
            """ 
            Webドライバーを取得する
            
            Parameters
            ----------
            None
                
            """
            
            # オプションクラスインスタンス
            options = chromeOptions()
            # ヘッドレスモード設定
            self.setOptions(options)
            # WebDriverパスを取得
            webDriverPath = self.getWebDriverPath(self.config.chrome)
            # WebDriverを返す
            Logger.logging.info('get webdriver - start')
            Logger.logging.info('WebDriverPath:' + webDriverPath)
            Logger.logging.info('WebDriverLogPath:' + self.config.chrome.WebDriverLogPath)
            Logger.logging.info('PageLoadStrategy:' + self.config.PageLoadStrategy)
            try:
                # ページ読み込み待ち処理の無効/有効を設定する
                desired = DesiredCapabilities().CHROME
                desired['pageLoadStrategy'] = self.config.PageLoadStrategy

                Logger.logging.info('Create WebDriver Instance - start')
                
                # WebDriver生成
                if self.config.chrome.WebDriverLogPath == '':
                    self.wDriver = webdriver.Chrome(executable_path=webDriverPath, 
                                                    options=options, 
                                                    desired_capabilities=desired)
                else:
                    self.wDriver = webdriver.Chrome(executable_path=webDriverPath, 
                                                    service_log_path=self.config.chrome.WebDriverLogPath, 
                                                    options=options,
                                                    desired_capabilities=desired)
                    
                Logger.logging.info('Create WebDriver Instance - end')

            except TimeoutException as e:
                Logger.logging.error("Selenium Exception: {0} Message: {1}".format("TimeoutException", str(e)))
            except WebDriverException as e:
                Logger.logging.error("Selenium Exception: {0} Message: {1}".format("WebDriverException", str(e)))
            except Exception as e:
                Logger.logging.error("Selenium Exception: {0} Message: {1}".format("Exception", str(e)))
            finally:
                Logger.logging.info('get webdriver - end')
            return self.wDriver 
        
    class firefox(baseWebBrowserController):
        
        """
        FireFoxブラウザコンテナ
        """
        
        def __init__(self, _config:scrapingConfig):
            
            """
            コンストラクタ
            
            Parameters 
            ----------
            _config : scrapingConfig
                共通設定クラス

            """
            
            # 基底側コンストラクタ呼び出し
            super().__init__(_config)
        
        def __del__(self):
            
            """
            デストラクタ
            """
            
            # webdriver - quit
            self.wDriver.close()
            self.wDriver.quit()
            # ログ出力
            Logger.logging.info('firefox webdriver is quit.')

        def getWebDriver(self):
            
            """ 
            Webドライバーを取得する
            
            Parameters
            ----------
            None
                
            """
            
            # オプションクラスインスタンス
            options = firefoxOptions()
            # オプション設定
            self.setOptions(options)
            # WebDriverパスを取得
            webDriverPath = self.getWebDriverPath(self.config.firefox)
            # WebDriverを返す
            Logger.logging.info('get webdriver - start')
            Logger.logging.info(self.config.firefox.WebDriverLogPath)
            try:
                if self.config.firefox.WebDriverLogPath == '':
                    self.wDriver = webdriver.Firefox(executable_path=webDriverPath, options=options)
                else:
                    self.wDriver = webdriver.Firefox(executable_path=webDriverPath, log_path=self.config.firefox.WebDriverLogPath, options=options)            
            except TimeoutException as e:
                Logger.logging.error("Selenium Exception: {0} Message: {1}".format("TimeoutException", str(e)))
            except WebDriverException as e:
                Logger.logging.error("Selenium Exception: {0} Message: {1}".format("WebDriverException", str(e)))
            finally:
                Logger.logging.info('get webdriver - end') 
            return self.wDriver 
        