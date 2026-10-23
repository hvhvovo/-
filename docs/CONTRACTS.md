# 预期结果的依据

被测服务：Restful Booker 单体演示API，不是 Restful Booker Platform。

官方API文档：https://restful-booker.herokuapp.com/apidoc/index.html
机器可读文档：https://restful-booker.herokuapp.com/apidoc/api_data.js
官方源码：https://github.com/mwinteringham/restful-booker

| 场景 | 预期 | 依据与限制 |
|---|---|---|
| 创建与读取 | 200，字段与提交值一致 | 官方 CreateBooking/GetBooking 定义 |
| PUT/PATCH | 200，并可重新读取 | 官方 UpdateBooking/PartialUpdateBooking |
| DELETE | 201；随后GET为404 | 删除成功状态来自官方示例；不存在资源响应由实跑核对 |
| 无认证或无效令牌写入 | 403，原记录保持 | 官方写接口的认证参数要求；具体403由实跑核对 |
| firstname/lastname筛选 | 创建记录包含在结果中 | GetBookingIds 文档列出查询参数 |
| 金额0、布尔false、空附加需求 | 按原值保存 | 接口字段类型允许这些输入，文档未规定更严格范围；属于演示API契约的特征测试，不表示真实酒店业务应允许零价 |
| 负数、缺失必填字段、反向日期 | 本期不预设返回400 | 文档未充分规定错误契约，不能靠通用习惯判缺陷 |

筛选用例只验证本测试创建的记录可被找到，未穷尽所有返回项的过滤正确性。当前不声称完整业务覆盖。
