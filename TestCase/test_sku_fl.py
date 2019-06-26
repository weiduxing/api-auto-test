import allure
import pytest
from Common import Request, Assert, read_excel,conf

request = Request.Request()
url = conf.url
assertions = Assert.Assertions()

fl_id = 0
excel_list = read_excel.read_excel_list('./document/商品分类.xlsx')
ids_list = []
for i in range(len(excel_list)):
    # 删除excel_list中每个小list的最后一个元素,并赋值给ids_pop
    ids_pop = excel_list[i].pop()
    # 将ids_pop添加到 ids_list 里面
    ids_list.append(ids_pop)


@allure.feature("商品分类模块")
class Test_info:

    @allure.story("获取分类列表")
    def test_sel(self,head):
        login_resp = request.get_request(url=url+'/productCategory/list/0',
                                         params={'pageNum': 1, 'pageSize': 5}, headers=head)
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], '成功')

        resp_data = login_resp_json['data']
        data_list = resp_data['list']
        fl_dict = data_list[0]
        global fl_id
        fl_id = fl_dict['id']

    @allure.story("删除商品分类")
    def test_del(self,head):
        login_resp = request.post_request(url=url+'/productCategory/delete/' + str(fl_id),
                                          headers=head)
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], '成功')

    @allure.story("添加商品分类")
    def test_add(self,head):
        login_resp = request.post_request(url=url+'/productCategory/create',
                                            json={"description": "", "icon": "", "keywords": "", "name": "家电",
                                                  "navStatus": 0, "parentId": 0, "productUnit": "", "showStatus": 0,
                                                  "sort": 0, "productAttributeIdList": []}, headers=head)
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], '成功')

    @allure.story("添加商品分类_参数化")
    @pytest.mark.parametrize('name,keywords,msg',excel_list,ids=ids_list)
    def test_add(self,name,keywords,msg,head):
        login_resp = request.post_request(url=url+'/productCategory/create',
                                          json={"description": "", "icon": "", "keywords": keywords, "name": name,
                                                "navStatus": 0, "parentId": 0, "productUnit": "", "showStatus": 0,
                                                "sort": 0, "productAttributeIdList": []}, headers=head)
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], msg)