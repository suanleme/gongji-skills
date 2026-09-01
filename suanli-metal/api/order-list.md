# 订单列表

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/output/v2/device_order/get_order_list_v2:
    post:
      summary: 订单列表
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        获取订单列表及其相关信息。
      tags:
        - 共绩算力 Open API/裸金属/订单列表
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                page:
                  type: integer
                  title: 页码
                page_size:
                  type: integer
                  title: 每页数量
                conditional:
                  type: object
                  properties:
                    condition:
                      type: string
                  required:
                    - condition
                  x-apifox-orders:
                    - condition
                  title: 关键词
                  description: 设备型号/订单编号
              required:
                - page
                - page_size
                - conditional
              x-apifox-orders:
                - page
                - page_size
                - conditional
            example:
              page: 1
              page_size: 10
              conditional:
                condition: '123'
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: string
                  message:
                    type: string
                  data:
                    type: object
                    properties:
                      count:
                        type: integer
                      results:
                        type: array
                        items:
                          type: object
                          properties:
                            order_id:
                              type: integer
                              title: 订单ID
                            order_no:
                              type: string
                              title: 订单号
                            status:
                              type: string
                              title: 订单状态
                              enum:
                                - Default
                                - Waiting
                                - Serving
                                - Finished
                                - Canceled
                              x-apifox-enum:
                                - value: Default
                                  name: 默认
                                  description: ''
                                - value: Waiting
                                  name: 等待中
                                  description: ''
                                - value: Serving
                                  name: 服务中
                                  description: ''
                                - value: Finished
                                  name: 已结束
                                  description: ''
                                - value: Canceled
                                  name: 已取消
                                  description: ''
                            buy_count:
                              type: integer
                              title: 购买数量
                            total_price:
                              type: integer
                              title: 订单金额
                            create_time:
                              type: string
                              title: 创建时间
                            billing_type:
                              type: string
                              title: 计费方式
                              enum:
                                - Hour
                                - Day
                                - Week
                                - Month
                              x-apifox-enum:
                                - value: Hour
                                  name: 小时时长包
                                  description: ''
                                - value: Day
                                  name: 24小时时长包
                                  description: ''
                                - value: Week
                                  name: 7天时长包
                                  description: ''
                                - value: Month
                                  name: 30天时长包
                                  description: ''
                            gpu_models:
                              type: array
                              items:
                                type: object
                                properties:
                                  gpu_model:
                                    type: string
                                    title: 设备GPU型号
                                  gpu_count:
                                    type: integer
                                    title: 设备卡数
                                  order_details_id:
                                    type: integer
                                    title: 订单详情ID
                                  order_detail_status:
                                    type: string
                                    title: 订单详情状态
                                    enum:
                                      - Default
                                      - Waiting
                                      - Serving
                                      - Finished
                                      - Canceled
                                      - CanceledRefunded
                                    x-apifox-enum:
                                      - value: Default
                                        name: 默认
                                        description: ''
                                      - value: Waiting
                                        name: 等待中
                                        description: ''
                                      - value: Serving
                                        name: 服务中
                                        description: ''
                                      - value: Finished
                                        name: 已结束
                                        description: ''
                                      - value: Canceled
                                        name: 已取消
                                        description: ''
                                      - value: CanceledRefunded
                                        name: 已取消并退款
                                        description: ''
                                  total_price:
                                    type: integer
                                    title: 订单详情金额
                                  is_paid:
                                    type: boolean
                                    title: 是否支付
                                required:
                                  - gpu_model
                                  - gpu_count
                                  - order_details_id
                                  - order_detail_status
                                  - total_price
                                  - is_paid
                                x-apifox-orders:
                                  - gpu_model
                                  - gpu_count
                                  - order_details_id
                                  - order_detail_status
                                  - total_price
                                  - is_paid
                              title: 设备信息
                            discount_total_price:
                              type: integer
                              title: 订单算力券消费
                              description: 1000000=1元
                            actually_total_price:
                              type: integer
                              title: 订单余额消费
                              description: 1000000=1元
                            cancel_actually_total_price:
                              type: integer
                              title: 订单余额退款
                              description: 1000000=1元
                            cancel_discount_total_price:
                              type: integer
                              title: 订单算力券退款
                              description: 1000000=1元
                          required:
                            - order_id
                            - order_no
                            - status
                            - buy_count
                            - total_price
                            - create_time
                            - billing_type
                            - gpu_models
                            - discount_total_price
                            - actually_total_price
                            - cancel_actually_total_price
                            - cancel_discount_total_price
                          x-apifox-orders:
                            - order_id
                            - order_no
                            - status
                            - buy_count
                            - total_price
                            - create_time
                            - billing_type
                            - gpu_models
                            - discount_total_price
                            - actually_total_price
                            - cancel_actually_total_price
                            - cancel_discount_total_price
                    required:
                      - count
                      - results
                    x-apifox-orders:
                      - count
                      - results
                required:
                  - code
                  - message
                  - data
                x-apifox-orders:
                  - code
                  - message
                  - data
              example:
                code: '0000'
                message: success
                data:
                  count: 2
                  results:
                    - order_id: 1775
                      order_no: '1785826899729'
                      status: Waiting
                      buy_count: 1
                      device_count: 0
                      total_price: 28000000
                      create_time: '2026-08-04T15:01:39.729898+08:00'
                      billing_type: Hour
                      gpu_models:
                        - gpu_model: '5090'
                          gpu_count: 8
                          order_details_id: 1772
                          order_detail_status: Waiting
                          total_price: 28000000
                          is_paid: true
                      discount_total_price: 28000000
                      actually_total_price: 0
                      cancel_actually_total_price: 0
                      cancel_discount_total_price: 0
                    - order_id: 1703
                      order_no: '1784512431064'
                      status: Finished
                      buy_count: 1
                      device_count: 0
                      total_price: 28000000
                      create_time: '2026-07-20T09:53:51.064032+08:00'
                      billing_type: Hour
                      gpu_models:
                        - gpu_model: '5090'
                          gpu_count: 8
                          order_details_id: 1700
                          order_detail_status: Finished
                          total_price: 28000000
                          is_paid: true
                      discount_total_price: 28000000
                      actually_total_price: 0
                      cancel_actually_total_price: 0
                      cancel_discount_total_price: 0
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 共绩算力 Open API/裸金属/订单列表
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-496881804-run
components:
  schemas: {}
  securitySchemes:
    AdminAuth:
      type: jwt
      scheme: bearer
      bearerFormat: JWT
      description: 运营中台管理员登录态；需具备权限 `tenant:create_offline_metal_order`
servers:
  - url: https://openapi.suanli.cn
    description: 正式环境
security: []

```