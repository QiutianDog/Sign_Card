'''
###########################################
#   Auto Sign Card V2.0                   #
#       * Support many people Sign        #
#       * User save at Mysql.Table.user   #
#           * id=*                        #
#           * username=*                  #
#           * password=*                  #
#           * email=*                     #
###########################################
'''
from lxml import etree
import requests
import MySQLdb
import time
import json
import os

class SignCardRobot:
    def __init__(self):
        # 用来储存用户的列表
        self.user_list = []
        # 用来存储当前所选择的用户
        self.user = None
        # 用来存储当前所选择用户的打卡数据包
        self.user_data = None
        # 用来存储打卡的结果信息
        self.email_message = None

        # 用来打卡的一些url
        # 默认头部
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        # 登录url
        self.login_url = "http://ids2.just.edu.cn/cas/login?service=http%3A%2F%2Fmy.just.edu.cn%2F"
        # 打卡url
        self.sign_url = "http://ehall.just.edu.cn/default/work/jkd/jkxxtb/com.sudytech.portalone.base.db.saveOrUpdate.biz.ext"
        # 近期打卡信息url
        self.near_url = "http://ehall.just.edu.cn/default/work/jkd/jkxxtb/com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext"

        # 打卡所用的会话
        self.sess = None

    def select_user(self, indexOf):
        self.user = self.user_list[indexOf]
        self.user_data = None

    def add_user(self, username, password, email):
        user = {"username": username,
                "password": password,
                "email": email
        }
        self.user_list.append(user)

    def user_count(self):
        return len(self.user_list)

    def create_sess(self):
        self.sess = requests.session()

    def close_sess(self):
        self.sess.close()

    def login(self):
        '''
        登录当前所选择的用户
        '''
        # 打开登录界面
        login_html = self.sess.get(url=self.login_url, headers=self.header)

        # 获取随机的execution
        selector = etree.HTML(login_html.text)
        execution = selector.xpath('/html/body/div[2]/div[1]/div[2]/div/div[1]/div/div/form[1]/div[5]/input[1]/@value')[0]

        # 构建数据包
        data = {'username': self.user['username'],
                'password': self.user['password'],
                'execution': execution,
                '_eventId': 'submit',
                'loginType': '1',
                'submit': '登 录'
        }

        # 登录
        self.sess.post(url=self.login_url, data=data, headers=self.header)

    def check_sign(self):
        '''
        检查今天是否打过卡
        :return: 是否打卡 是为 True 否为 False
        '''
        # 打开打卡界面
        self.sess.get(url=self.sign_url, headers=self.header)

        # 准备查询数据
        today = time.strftime("%Y-%m-%d", time.localtime())
        data = {'params': {'empcode': self.user['username']},
                'querySqlId': 'com.sudytech.work.suda.jkxxtb.jkxxtb.queryNear'
                }
        # 查询近期打卡情况
        rsp = self.sess.post(url=self.near_url, json=data, headers=self.header)
        near_data = json.loads(rsp.text)['list'][0]

        # 根据最近的打卡结果判断
        if near_data['TBRQ'] == today:
            return True
        else:
            # 如果今天没有打卡，记录下上次的打卡信息
            self.user_data = self.near_json_to_sgin(near_data)
            return False

    def near_json_to_sgin(self, near_json):
        '''
        将最近的打卡数据包，转化为最新的打卡数据包
        :param near_json: 最近打卡的 json 数据
        :return: 最新的打卡数据包
        '''
        # 获取今天的时间
        tbrq = time.strftime("%Y-%m-%d", time.localtime())
        tjsj = time.strftime("%Y-%m-%d %H:%M", time.localtime())

        # 调整参数
        def null_or_value(value):
            if value == "null":
                return ""
            return value

        bz = null_or_value(near_json['BZ'])
        fhzjbc = null_or_value(near_json['FHZJBC'])
        fhzjgj = null_or_value(near_json['FHZJGJ'])
        fhzjsj = null_or_value(near_json['FHZJSJ'])
        fztztkdd = null_or_value(near_json['FZTZTKDD'])
        gh = null_or_value(near_json['GH'])
        id = null_or_value(near_json['ID'])
        jgshen = null_or_value(near_json['JGSHEN'])
        jgshi = null_or_value(near_json['JGSHI'])
        jgzgfxdq = null_or_value(near_json['JGZGFXDQ'])
        jrjzdxxdz = null_or_value(near_json['JRJZDXXDZ'])
        jrsfjgzgfxdq = null_or_value(near_json['JRSFJGZGFXDQ'])
        jrstzk = null_or_value(near_json['JRSTZK'])
        jrszd = null_or_value(near_json['JRSZD'])
        lxdh = null_or_value(near_json['LXDH'])
        lzbc = null_or_value(near_json['LZBC'])
        lzjtgj = null_or_value(near_json['LZJTGJ'])
        lzsj = null_or_value(near_json['LZSJ'])
        rysf = null_or_value(near_json['RYSF'])
        sffr = null_or_value(near_json['SFFR'])
        sffz = null_or_value(near_json['SFFZ'])
        sfjchwry = null_or_value(near_json['SFJCHWRY'])
        sfjcysqzrq = null_or_value(near_json['SFJCYSQZRQ'])
        sflz = null_or_value(near_json['SFLZ'])
        sfyqgzdyqryjc = null_or_value(near_json['SFYQGZDYQRYJC'])
        sfyyqryjc = null_or_value(near_json['SFYYQRYJC'])
        sfzh = null_or_value(near_json['SFZH'])
        sqbmid = null_or_value(near_json['SQBMID'])
        sqbmmc = null_or_value(near_json['SQBMMC'])
        sqrid = null_or_value(near_json['SQRID'])
        sqrmc = null_or_value(near_json['SQRMC'])
        tw = null_or_value(near_json['TW'])
        xb = null_or_value(near_json['XB'])
        zwtw = null_or_value(near_json['ZWTW'])

        data = {"entity": {
                'bz': bz,
                'fhzjbc': fhzjbc,
                'fhzjgj': fhzjgj,
                'fhzjsj': fhzjsj,
                'fztztkdd': fztztkdd,
                'gh': gh,
                'glqsrq': "[" + tbrq + "," + tbrq + "]",
                'id': id,
                'jgshen': jgshen,
                'jgshi': jgshi,
                'jgzgfxdq': jgzgfxdq,
                'jrjzdxxdz': jrjzdxxdz,
                'jrsfjgzgfxdq': jrsfjgzgfxdq,
                'jrstzk': jrstzk,
                'jrszd': jrszd,
                'lxdh': lxdh,
                'lzbc': lzbc,
                'lzjtgj': lzjtgj,
                'lzsj': lzsj,
                'rysf': rysf,
                'sffr': sffr,
                'sffz': sffz,
                'sfjchwry': sfjchwry,
                'sfjcysqzrq': sfjcysqzrq,
                'sflz': sflz,
                'sfyqgzdyqryjc': sfyqgzdyqryjc,
                'sfyyqryjc': sfyyqryjc,
                'sfzh': sfzh,
                'sqbmid': sqbmid,
                'sqbmmc': sqbmmc,
                'sqrid': sqrid,
                'sqrmc': sqrmc,
                'tbrq': tbrq,
                'tjsj': tjsj,
                'tw': tw,
                'xb': xb,
                'zwtw': zwtw,
                '__type': "sdo:com.sudytech.work.suda.jkxxtb.jkxxtb.TSudaJkxxtb",
                '_ext': "{}"
            }
        }
        return data

    def sign(self):
        # 发送数据包 进行打卡
        rsp = self.sess.post(url=self.sign_url, json=self.user_data, headers=self.header)

        # 分析打卡结果
        results = json.loads(rsp.text)
        tjsj = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        if results['result'] == '1':
            self.email_message = "User [" + self.user['username'] + "] Sign Card succeed at " + tjsj + " !"
            return True
        return False

    def sent_eamil(self):
        # 发送邮件
        msg = self.email_message
        cmd = "echo \"" + msg +  "\" | mailx -s \"Sign Note\" " + self.user['email']
        os.system(cmd)

        # 记录
        note_time = "[" + time.asctime(time.localtime(time.time())) + "]"
        today = time.strftime("%Y-%m-%d", time.localtime())
        file_path = "logs/" + today + ".log"
        os.chdir("/home/admin/PythonPro/request") # 这里填的是项目文件存放的文件夹(linux)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as log:
                log.write(note_time + msg + '\n')
        else:
            with open(file_path, 'a') as log:
                log.write(note_time + msg + '\n')

if __name__ == '__main__':
    # 创建打卡对象
    robot = SignCardRobot()

    # 从数据库中读取用户信息(url, user, password, database)
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "sign_card")
    cursor = conn.cursor()
    sql = "SELECT * FROM user"
    cursor.execute(sql)

    tables = cursor.fetchall()
    for rows in tables:
        username = rows[1]
        password = rows[2]
        email = rows[3]
        # 添加到列表中
        robot.add_user(username=username, password=password, email=email)
    # 关闭数据库
    conn.close()

    # 开始依次打卡
    for i in range(robot.user_count()):
        robot.select_user(i)
        robot.create_sess()
        robot.login()
        if robot.check_sign() is False:
            b = robot.sign()
            if b is True:
                robot.sent_eamil()
        robot.close_sess()
