
## 專案簡介
以Flutter作為前端技術，搭配flask建立本地伺服器
基礎模型為Meta 所開源且在規範下可商用的 Llama 3 模型，實際用來訓練的是Hugging Face上的[taide/Llama3-TAIDE-LX-8B-Chat-Alpha1](https://huggingface.co/taide/Llama3-TAIDE-LX-8B-Chat-Alpha1)

功能：
1. 自動抓取有提及"地層下陷"的新聞
2. 可以上傳新聞讓模型分類並儲存結果
3. 直接在網頁查看原始新聞、被分類好的新聞
4. 把想回應的新聞群打勾並下載
5. 直接和Chat Bot進行單則訊息對話(分類模型)
6. 回應稿機器人幫忙回復新聞稿

## 程式使用說明

### 運行版本：
- python : 3.12.1
- flutter : 3.24.3
  - 安裝環境說明  [官網](https://docs.flutter.dev/get-started/install?_gl=1*6a7j8s*_gcl_aw*R0NMLjE3MjcwODMwNzkuQ2owS0NRandvOFMzQmhEZUFSSXNBRlJta09QYjZOOFdQb3haUnpQOC1yakJySE55SFVSSTZBWXlvWWFQN1N2bVljVkh3alJQY3FWYk1CZ2FBcjZTRUFMd193Y0I.*_gcl_dc*R0NMLjE3MjcwODMwNzkuQ2owS0NRandvOFMzQmhEZUFSSXNBRlJta09QYjZOOFdQb3haUnpQOC1yakJySE55SFVSSTZBWXlvWWFQN1N2bVljVkh3alJQY3FWYk1CZ2FBcjZTRUFMd193Y0I.*_up*MQ..*_ga*MTA0NTUwODgwLjE3MDg2ODkwNDU.*_ga_04YGWK0175*MTcyNzA4Mjk0OS4zMS4xLjE3MjcwODMwODMuMC4wLjA.&gclid=Cj0KCQjwo8S3BhDeARIsAFRmkOPb6N8WPoxZRzP8-rjBrHNyHURI6AYyoYaP7SvmYcVHwjRPcqVbMBgaAr6SEALw_wcB&gclsrc=aw.ds)
 
- [其他環境安裝說明（虛擬環境、Pytorch+cuda）](https://hackmd.io/@gonjo9/BkgszG10A)

### 運行方式
執行 :
1. `lib\main.dart`  -- 前端網頁
2. `app.py`       -- 本地伺服器

網頁成功被叫出且 "  Debugger is active! " 出現在 terminal 即代表程式開始運作
## 專案架構
後續說明以功能導向作為主架構
### 資料儲存
* `lib\back_end\repo`
  * 裡面的資料可以從網站看到 
  * 這裡存放爬蟲下來的歷史新聞、完整新聞檔案
  * 欄位：['Title', 'Content', 'Link', 'Time', 'Resource']
* `lib\back_end\repo\categorized_news`
  * 裡面的資料可以從網站看到 
  * 在這裏面的文章是被分類完才存到這裡
  * 欄位：['Title', 'Content', 'Link', 'Time', 'Resource', 'Categorize']

![image](https://hackmd.io/_uploads/Sy-o2-1CR.png)
* `lib\back_end\repo\files`
  * 這裡放的文件主要是跟後端邏輯有關，不太會需要動到
  * `country.txt`：供app.py中的upload_excel()使用
  * `record.txt`：用來記錄最後一次更新的日期
  * `count.txt`：紀錄訓練的model編號
  * `tune_parameter.xlsx`：紀錄model編號、所有參數資料、模型表現
### 1.更新新聞
![image](https://hackmd.io/_uploads/Hy1HybJCA.png)
#### 相關檔案
* app.py內路徑 ： 
@app.route('/fetch_news', methods=['GET'])
fetch_news()
* 後端：`lib\back_end\get_news`
* 前後端接口：`lib\view_model\homePageViewModel.dart` - updateNews(BuildContext context)
* 前端：`lib\view\homeView.dart` - Widget _buildSidebarFooter(viewModel, context)
* 爬取新聞的期限是依據`repo\files\record.txt`內紀錄的"上次更新"的日期~現在，
點擊這個按鈕後就會開始自動更新，爬完之後的檔案會進到兩個檔案
  - `repo\original_news\All_News.xlsx`
    * `All_News.xlsx`  : 記錄從20220101開始到最後一次更新的"所有"新聞
  - `repo\original_news\News_from_{前次日期}_to_{今天日期}.xlsx`
    * `News_from_{前次日期}_to_{今天日期}.xlsx`  : 紀錄上次更新到這次之間新增的新聞


### 2.上傳並讓模型分類新聞
![image](https://hackmd.io/_uploads/SyjgxGyRR.png)
- 從`repo\original_news\`選一個檔案進行分類，分類完之後的結果會被存到`repo\categorized_news\`

***如果沒有成功分類，可從Debug Console看到錯誤原因***
#### 相關檔案
* app.py內路徑(含後端邏輯) ： 
@app.route('/upload_excel', methods=['POST'])
def upload_excel()
* 前後端接口：`lib\view_model\homePageViewModel.dart` - uploadFile(BuildContext context)
* 前端：`lib\view\homeView.dart` - Widget _buildSidebarFooter(viewModel, context)

### 3.查看新聞
![image](https://hackmd.io/_uploads/HymhRWtzkl.png)
#### 相關檔案
* app.py內路徑(含後端邏輯) ： 
![image](https://hackmd.io/_uploads/H1KR0ZFM1l.png)
* 前端：`lib\front_end\view\fileView.dart` 
### 4.打勾新聞並下載
![image](https://hackmd.io/_uploads/H1nL1MKzJe.png)
打勾之後才會跳出確認送出的按鈕
#### 相關檔案
* app.py內路徑(含後端邏輯) ： 
@app.route('/save_excel', methods=['POST'])
def save_excel()
* 前後端接口：`lib\front_end\view_model\fileViewModel.dart` - downloadFile(BuildContext context)
* 前端：`lib\front_end\view\fileView.dart` 


### 5.和Chat Bot聊天
#### 相關檔案
* app.py內路徑 ： 
@app.route('/get_response', methods=['POST'])
def get_response()

* 前後端接口：`lib\view_model\trainViewModel.dart` - trainNewModel(BuildContext context)
* 前端：`lib\view\trainModelView.dart` 
### 6.回應稿機器人
![image](https://hackmd.io/_uploads/SJnGgMYz1l.png)

## 爬蟲相關除錯
### AttributeError: 'NoneType' object has no attribute...
ex:
`AttributeError: 'NoneType' object has no attribute 'findAll'`

通常是新聞網站更改了排版，導致 find/findAll 沒找到東西，要重新從 html 找那個物件的位置。
>例如找不到某家新聞的標題，就去該家新聞的網頁對標題按右鍵選檢查元件，然後修改尋找標題的那段程式碼

### UnicodeEncodeError
後續使用若有改變搜尋關鍵字，可能會更改爬蟲程式碼中的網址。

```python
url = "https://news.pts.org.tw/search/地層下陷"
```

而用 `urllib.request` 裡的 urlopen 開包含中文的網址可能會報這個錯誤。

```
UnicodeEncodeError: 'ascii' codec can't encode characters
in position 12-15: ordinal not in range(128)
```

若是這個問題，用 `import urllib.parse as parse` 裡的 parse.quote() 把中文的部分分開就沒問題了。

```python
url = "https://news.pts.org.tw/search/" + parse.quote("地層下陷")
```
