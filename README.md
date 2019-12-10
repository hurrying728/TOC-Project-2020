# TOC Project 2020

[![Maintainability](https://api.codeclimate.com/v1/badges/dc7fa47fcd809b99d087/maintainability)](https://codeclimate.com/github/NCKU-CCS/TOC-Project-2020/maintainability)

[![Known Vulnerabilities](https://snyk.io/test/github/NCKU-CCS/TOC-Project-2020/badge.svg)](https://snyk.io/test/github/NCKU-CCS/TOC-Project-2020)


Template Code for TOC Project 2020

A Line bot based on a finite state machine

More details in the [Slides](https://hackmd.io/@TTW/ToC-2019-Project#) and [FAQ](https://hackmd.io/s/B1Xw7E8kN)

## Setup

### Prerequisite
* Python 3.6
* Pipenv
* Facebook Page and App
* HTTPS Server

#### Install Dependency
```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)
	* [Note: macOS Install error](https://github.com/pygraphviz/pygraphviz/issues/100)


#### Secret Data
You should generate a `.env` file to set Environment Variables refer to our `.env.sample`.
`LINE_CHANNEL_SECRET` and `LINE_CHANNEL_ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

#### Run Locally
You can either setup https server or using `ngrok` as a proxy.

#### a. Ngrok installation
* [ macOS, Windows, Linux](https://ngrok.com/download)

or you can use Homebrew (MAC)
```sh
brew cask install ngrok
```

**`ngrok` would be used in the following instruction**

```sh
ngrok http 8000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python3 app.py
```

#### b. Servo

Or You can use [servo](http://serveo.net/) to expose local servers to the internet.


## Finite State Machine
![fsm](./img/show-fsm.png)

## Usage
```sh
協助成功大學學生初步排解使用宿網可能遇到的問題(X) 降低每年開學計網中心工讀生(我)產生想辭職衝動的機率(O)
```
The initial state is set to `user`. When the state is set to `final`, goes back to `user`.

* user
	* Input: "開始使用"
		* State: start
		* Reply: "請選擇是否已開始註冊宿網" + 2 buttons["尚未開始註冊宿網", "已開始註冊宿網"]
		
* start
	* Input: "尚未開始註冊宿網"
		* State: before_register
		* Reply: "請選擇連接宿網之方式" + 2 buttons["使用分享器", "無使用分享器"]
	* Input: "已開始註冊宿網"
		* State: after_register
		* Reply: "選擇註冊情況" + 3 buttons["已註冊", "未註冊", "網孔已被註冊"]
* before_register
	* Input: "使用分享器"
		* State: use_router
		* Reply: "請確認分享器設定" + 2 buttons["連線成功", "仍無法連線"]
	* Input: "無使用分享器"
		* State: not_use_router
		* Reply: "確認右下角連線圖示" + 2 buttons["紅色叉叉", "黃色驚嘆號"]
* after_register
	* Input: "已註冊"
		* State: "already_register"
		* Reply: "確認右下角連線圖示" + 2 buttons["紅色叉叉", "黃色驚嘆號"]
	* Input: "未註冊"
		* State: "not_register"
		* Reply: "請至宿網管理系統註冊" + 2 buttons["連線成功", "仍無法連線"]
	* Input: "網孔已被註冊"
		* State: "occupied"
		* Reply: "請確認是否為室友註冊" + 2 buttons["是", "否"]
* use_router, check_dns
	* Input: "連線成功"
		* State: final
		* Reply: "感謝您的使用"
	* Input: "仍無法連線"
		* State: call
		* Reply: "轉由專人服務"
* not_use_router, already_register
	* Input: "紅色叉叉"
		* State: change
		* Reply: "更換轉接頭/網路線測試"
	* Input: "黃色驚嘆號"
		* State: call
		* Reply: "轉由專人服務"
* not_register
	* Input: "連線成功"
		* State: final 
		* Reply: "感謝您的使用"
	* Input: "仍無法連線"
		* State: check_wifi
		* Reply: "確認無連上無線網路" + 2 buttons["連線成功", "仍無法連線"]
* check_wifi
	* Input: "連線成功"
		* State: final 
		* Reply: "感謝您的使用"
	* Input: "仍無法連線"
		* State: check_dns
		* Reply: "確認其他設定" + 2 buttons["連線成功", "仍無法連線"]
* occupied
	* Input: "是"
		* State: find_another 
		* Reply: "請更換至其他網孔" + 2 buttons["已更換至未註冊網孔", "欲與室友交換網孔"]
	* Input: "否"
		* State: reply
		* Reply: "請依照下列格式回覆"
* find_another
	* Input: "已更換至未註冊網孔"
		* State: not_register 
		* Reply: "請至宿網管理系統註冊" + 2 buttons["連線成功", "仍無法連線"]
	* Input: "欲與室友交換網孔"
		* State: reply
		* Reply: "請依照下列格式回覆"
* reply
	* Input: "姓名：..."
		* State: final
		* Reply: "感謝您的使用"
* call
	* Input: "我知道了"
		* State: final
		* Reply: "感謝您的使用"
## Deploy
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

or you can use Homebrew (MAC)
```sh
brew tap heroku/brew && brew install heroku
```

or you can use Snap (Ubuntu 16+)
```sh
sudo snap install --classic heroku
```

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

	refference: https://hackmd.io/@ccw/B1Xw7E8kN?type=view#Q2-如何在-Heroku-使用-pygraphviz

## Reference
[Pipenv](https://medium.com/@chihsuan/pipenv-更簡單-更快速的-python-套件管理工具-135a47e504f4) ❤️ [@chihsuan](https://github.com/chihsuan)

[TOC-Project-2019](https://github.com/winonecheng/TOC-Project-2019) ❤️ [@winonecheng](https://github.com/winonecheng)

Flask Architecture ❤️ [@Sirius207](https://github.com/Sirius207)

[Line line-bot-sdk-python](https://github.com/line/line-bot-sdk-python/tree/master/examples/flask-echo)
