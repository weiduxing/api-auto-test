import allure
import pytest
from Common import Request, Assert, conf

url = conf.url
request = Request.Request()

assertions = Assert.Assertions()


@allure.feature("获取用户信息")
class Test_Info:

    @allure.story("用户信息接口")
    @pytest.mark.login
    def test_info(self, head):
        info_resp = request.get_request(url=url + '/admin/info', headers=head)
        assertions.assert_code(info_resp.status_code, 200)
        info_resp_json = info_resp.json()
        assertions.assert_in_text(info_resp_json['message'], '成功')

    @allure.story("获取商品列表")
    @pytest.mark.login
    def test_sku(self, head):
        sku_resp = request.get_request(url=url + '/product/list',
                                       params={'pageNum': 1, 'pageSize': 5}, headers=head)

        assertions.assert_code(sku_resp.status_code, 200)
        sku_resp_json = sku_resp.json()
        assertions.assert_in_text(sku_resp_json['message'], '成功')
