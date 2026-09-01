# 创建订单

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/output/v2/device_order/buy_v2:
    post:
      summary: 创建订单
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        创建裸金属订单，需要传入相应的设备ID。
        注意：unit_price仅用于页面显示价格与下单那一刻价格不一致的提示。
      tags:
        - 共绩算力 Open API/裸金属/创建订单
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
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
                buy_count:
                  type: integer
                  title: 购买数量
                inner:
                  type: array
                  items:
                    type: object
                    properties:
                      device_id:
                        type: integer
                        title: 设备ID
                      unit_price:
                        type: integer
                        title: 购买单价
                        description: 1000000=1元，仅用于页面显示价格与下单那一刻价格不一致的提示
                    required:
                      - device_id
                      - unit_price
                    x-apifox-orders:
                      - device_id
                      - unit_price
                  title: 购买设备
                  description: 组网设备购买buy_count > 1时传入多个，单机设备购买buy_count > 1时也只传入1个
                software_init:
                  type: boolean
                  title: 是否需要安装部分软件
                discount_relation_id:
                  type: integer
                  title: 使用算力券的ID
                  nullable: true
              required:
                - billing_type
                - buy_count
                - inner
                - software_init
                - discount_relation_id
              x-apifox-orders:
                - billing_type
                - buy_count
                - inner
                - software_init
                - discount_relation_id
            example: |-
              // 组网，inner传入object数量根据实际设备数（多个）
              // {
              //     "billing_type": "Hour",
              //     "buy_count": 2,
              //     "inner": [
              //         {
              //             "device_id": 1,
              //             "unit_price": 15000000
              //         },
              //         {
              //             "device_id": 2,
              //             "unit_price": 15000000
              //         }
              //     ],
              //     "software_init": true,
              //     "discount_relation_id": null
              // }
              // 单机，buy_count为多个时，inner也只传入1个object
              {
                  "billing_type": "Hour",
                  "buy_count": 3,
                  "inner": [
                      {
                          "device_id": 690,
                          "unit_price": 15000000
                      }
                  ],
                  "software_init": false,
                  "discount_relation_id": null
              }
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
                      order_id:
                        type: integer
                        title: 订单ID
                    required:
                      - order_id
                    x-apifox-orders:
                      - order_id
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
                  order_id: 1
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 共绩算力 Open API/裸金属/创建订单
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-496722319-run
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