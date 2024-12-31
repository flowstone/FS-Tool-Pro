# 说明
## 介绍
作者开发的小工具(完全由ChatGPT、豆包生成的代码)，目前有WIN/MacOS端，如果有问题，可以去项目中提issues，有时间会修复问题

### 项目地址
【[FS-Tool](https://github.com/flowstone/FS-Tool)】: https://github.com/flowstone/FS-Tool
### 作者
* 【[博客](http://blog.xueyao.tech/)】http://blog.xueyao.tech/, 文章基本不更新，但是域名注册了10年，到2034年结束
* 【[GitHub](https://github.com/flowstone)】https://github.com/flowstone
* 【flowstone】ipfs://flowstone.x

## 功能
### 透明时间
可以在桌面的左上角生成一个无背景的当前时间及计时器

### 快捷便签
用于日常使用中，随手记录的临时便签，不做保存处理

### 密码生成器
生成特写长度密码

### 文件夹老师
根据选择的文件夹，根据指定的分割字符，匹配目录下的文件名，以分割字符为界，前部分创建文件夹，把符合的文件移动到新创建的文件夹中，
#### 例如
[**初始**]文件夹下的文件如下：
```
abc_123.txt
abc_456.txt
abc_789.txt
cbd_123.pdf
cbd_456.pdf
cbd_789.pdf
```
[**结束**]文件夹下的结构如下
```
abc
  - abc_123.txt
  - abc_456.txt
  - abc_789.txt
cbd
  - cbd_123.pdf
  - cbd_456.pdf
  - cbd_789.pdf
```
### 重命名使者
根据选择的文件夹，可以修改文件夹下的文件和文件夹，序号、前缀、后缀、指定字符替换

### HEIC作家[递归]
根据选择的文件夹，把文件夹下的heic图片转成jpg格式的图片

### 图转大师
选择图片，转换成其它格式图片，不建议使用

### 自动答题
个人自用功能，需要输入密码才能使用，主要模仿用户答题，
如果网站改版，功能将失效，可使用JS脚本代替
#### 特殊说明
1. [Chrome指定版本131.0.6778.69](https://pan.quark.cn/s/e3e92f0b8882)
2. 当前页面下拉框加载失败后，将重复刷新页面(最多10次，间隔2s)
3. 有异常出现，只有本次答题失败，继续执行下一次
4. 存在程序闪崩情况
其它版本[GitHub](https://github.com/flowstone/Auto-Answers): Java、JS脚本


### 文件生成
可以在指定文件夹下生成指定数量的文件

### 文件比较
选择两个目录，根据相同的文件名，来比较两个目录下文件是否相同

### 文件加密
指定文件夹，把文件夹下的文件用AES加密，生成.enc加密文件

### RSA生成器
可以生成RSA密钥对