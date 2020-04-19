import os, sys
from flask_login import UserMixin, login_user, logout_user, current_user
from main import login_manager
import hashlib
from db_mod import db_connect
from common import my_log


o_path = os.getcwd()
sys.path.append(o_path)
sys.path.append('..')
logger = my_log.LogUtil().getLogger()



class User(UserMixin):
    def __init__(self, user_id=None, account_number=None, password=None): 
   
        self.user_id = user_id 
        self.accountNumber = account_number 
        self.password = password 
        # self.name = name 
   
    def is_authenticated(self):
        return True 
   
    def is_active(self): 
        return True 
   
    def is_anonymous(self): 
        return False 
   
    def get_id(self): 
        return str((self.user_id)).encode('utf-8')
   
    def __repr__(self): 
        return '<User %r>' % (self.accountNumber) 










@login_manager.user_loader
class login_tools(object):
    def __init__(self):
        pass
    def user_load(self, username, password):
        # 查询该用户在数据库中的密码 
        sql_password = "SELECT c_password FROM db_apitesting.t_zx_user WHERE c_username = '%s';" % username
        try:
            res_password = db_connect.My_dbc().pg_select_operator(sql_password)
        except Exception as eee:
            logger.error('查询登录密码报错，错误信息：' +str(eee))
            return False
        try:
            password == res_password[0]['c_password']
        except Exception as eee:
            logger.error('查询登录密码报错，错误信息：' +str(eee))
            return False
        # MD5加密前台传过来的密码明文
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()
        if password == res_password[0]['c_password']:
            curr_user = User(user_id=username)
            curr_user.id = username
            login_user(curr_user)
            # logger.info('当前登录用户：' + str(curr_user.get_id()))
            return curr_user
        else:
            return False
    def logout(self):
        logout_user()
        return '登出成功！'
    def get_username(self):
        return current_user.id

    

def update_password(new_password, username):
    md5 = hashlib.md5()
    md5.update(new_password.encode('utf-8'))
    password = md5.hexdigest()
    sql_uppwd = "UPDATE db_apitesting.t_zx_user SET c_password = '%s' WHERE c_username = '%s';" % (password, username)
    try:
        db_connect.My_dbc().pg_update_operator(sql_uppwd)
    except Exception as eee:
        logger.error('更新用户密码报错')
        logger.exception(eee)
        return False
    return True




if __name__ == '__main__':
    aaa = login_tools('q', '111').login()
    print(aaa)