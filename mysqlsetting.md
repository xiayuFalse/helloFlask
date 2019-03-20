###mysql初次登录配置
    1、自从mysql5.7开始，密码列不在为password，为authentication_string。
    2、mysqld_safe与mysqld区别，直接运行mysqld程序来启动MySQL服务的方法很少见，mysqld_safe脚本会在启动MySQL服务器后继续监控其运行情况，并在其死机时重新启动它。
    2、其中 --skip-grant-tables 的意思是跳过授权表，通过此参数来跳过输入密码。通常为忘记管理员密码时进行使用，也可以在/etc/mysql/my.conf配置文件中的[mysqld]段中加入此命令。
    3、修改默认密码命令:alter user user() identified by 'new_password';,update user set authentication_string=password('new_password
       ') where user='root';
    4、查看数据库中的字符编码:SHOW VARIABLES LIKE 'character%';
