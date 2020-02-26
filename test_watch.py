import unittest
from app import app,db,Movie,User
class WatchlistTestCase(unittest.TestCase):
    def setup(self):
        #更新配置
        app.config.update(
            TESTING=True,#开启测试
            SQLALCHEMY_DATBASE_URI='sqlite:///:memory:'#sqlite内存型数据库，不会干扰数据库
        )
        db.create_all()
        user = User(name='test',username='test')
        user.set_password('200010')
        movie = Movie(title='测试电影名称',year='2016')
        db.session.add_all([user,movie])
        db.session.commit()

        self.client = app.test_client()
        self.runner = app.test_cli_runer()


    def tearDown(self):
        db.session.remove()#清除数据库会话1
        db.drop_all()#删除数据库表

    #测试程序是否存在
    def test_app_exist(self):
        self.assertIsNotNone(app)

    #测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])


    def test_404_page(self):
        response = self.client.get('/lalala')#传入一个不存在的路由
        data = response.get_data(as_text=True) #获取Unicode格式的响应主体
        self.assertIn('404 - 页面跑丢了',data)
        self.assertIn('返回首页',data)
        self.assertEqual(response.status_code,404) #判断响应状态码

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('雷洛\'博客',data)
        self.assertEqual(response.status_code,200)

    #登录（辅助功能）
    def login(self):
        self.client.post('/login',data=dict(
            username='mrliu200010',
            password='200010'
        ),follow_redirects=True)

    def test_delete_item(self):
        self.login()
        response = self.client.post('movie/delete/1',follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("删除数据成功",data)