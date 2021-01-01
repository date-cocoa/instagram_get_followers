# instagram_get_followers
ターゲットのインスタグラムのフォロー者とフォロー者のフォロワー人数を取得

## 実行方法
conf/配下にconfig.ymlというファイルを作成。中身は下記の通りに書く。
```
phone_number: 00012341234
password: writepasswordhere
target: https://www.instagram.com/aaabbbccc
```

src/配下で下記を実行するとtargetのフォロワーの情報を取得し、data/配下にdata.csvが生成される。
```
python3 get_instagram_info.py
```

上記で出力されたdata.csvに下記でフィルターをかけて、data_official.csvを生成。
```
Rscript get_official_data.R
```

フィルターを変更するときはget_official_data.Rの中身を変更すること。また、フィルターをかけない場合は下記を実行すること。
```
cp ../data/data.csv ../data/data_official.csv
```

上記で出力されたdata_official.csvのアカウントを下記で開く。
```
python3 get_official_page.py
```