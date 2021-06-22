# 重產 klf 檔測資上傳工具

## 設定

* `.env` 設定資料庫帳密
    ![](https://i.imgur.com/husWsv1.png)


## 使用步驟
1. 終端機打開重產 klf 檔測資上傳工具資料夾，輸入`pipenv shell` 進入虛擬環境
    ![](https://i.imgur.com/aWeRyX3.png)
2. 終端機輸入 `pipenv install` 安裝依賴項(範例圖已經安裝過依賴了，所以進度顯示0)
    ![](https://i.imgur.com/257QnFt.png)
3. 終端機輸入 `python copy_folders_to_home.py`，將所需檔案複製到 /home 底下
    ![](https://i.imgur.com/DerI8gZ.png)
    ![](https://i.imgur.com/yp8v1fb.png)

4. 終端機輸入`python upload_klf_data_to_db.py ` 將 input_klf_backup 裡的資料上傳到資料庫
    ![](https://i.imgur.com/sHghdQS.png)
    c_img_data 表
    ![](https://i.imgur.com/ZN2Wh1k.png)
    klf_info 表
    ![](https://i.imgur.com/L9B0fIO.png)
    wafer_info 表
    ![](https://i.imgur.com/6hWZjil.png)
