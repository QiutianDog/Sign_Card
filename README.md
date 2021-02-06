# 自动健康打卡

------

## 运行需求
* Linux 系统（我的是 CentOS 7.3）
* Python 3.6
* Linux 下所使用的 mail 功能 （可以使用网易邮箱，需要配置参数）
* Mysql 5.1 以上 （账号密码和数据库名字可以改成自己的，但是必须有user表，表结构也要严格按要求来）

------

## 数据库安装
1. 下载数据库安装包
```shell
rpm -ivh http://dev.mysql.com/get/mysql-community-release-el7-8.noarch.rpm
```
2. 安装数据库
```
yum install mysql-community-server
```
3. 设置开机启动
```shell
systemctl enable mysqld.service
```
4. 查看服务器默认密码
```
grep 'temporary password' /var/log/mysqld.log
```
5. 登录mysql
```
mysql -uroot -p

然后输入刚刚得到的密码
```
6. 设置密码的验证强度等级
```mysql
set global validate_password_policy = LOW;
```
7. 设置密码最短长度
```mysql
set global validate_password_length = 4;
```
8. 设置密码
```mysql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
```
9. 设置root远程登录
```mysql
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'a123456!' WITH GRANT OPTION;
```
10. 命令立即执行生效
```mysql
flush privileges;
```
11. 建立数据库，建立user表
```mysql
create database sign_card;

USE sign_card;

CREATE TABLE user (
  id int NOT NULL AUTO_INCREMENT COMMENT '用户 ID',
  username varchar(12) NOT NULL COMMENT '学号',
  password varchar(6) NOT NULL COMMENT '身份证后六位',
  email varchar(32) DEFAULT NULL COMMENT '邮箱',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
```
12. 添加一条数据（举例）
```mysql
INSERT INTO user (username, password, email) VALUES ('学号', '密码', '邮箱');
```

------

## 网易邮箱配置
教程地址：[点击此处](https://www.cnblogs.com/mython/p/12180299.html)

------

## 设置服务器自动运行
使用Linux自带的定时任务系统 crond
```
编辑定时任务
crontab -e

跳入了vim界面，按一下insert切换到编辑模式，输入（一个任务占一行）
1,4,7 0,1,10,11 * * * /opt/anaconda3/envs/DemoPython36/bin/python3.6 /home/admin/PythonPro/request/sign_plus.py
python运行地址 换成自己python3.6所在地址
sign_plus.py文件地址 换成自己存放的地址

再按一下insert切换到只读模式，按下ESC 输入:wq! 回车即可保存

查看定时任务列表
crontab -l
```

------

## 运行
* sign_plus.py 的 228 行记得修改成自己的项目文件所在地址
* log 文件夹不要删，如果不需要记录日志 224~234行 注释掉即可
* 241行 可以就改成自己的数据库