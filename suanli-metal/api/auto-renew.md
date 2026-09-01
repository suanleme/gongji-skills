# 已购设备自动续费

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/output/v2/auto_renew_device_config/set_auto_renew_config:
    post:
      summary: 已购设备自动续费
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        已购买设备开启自动续费。
        注意：扣费失败会自动取消自动续费
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
                device_id:
                  type: integer
                  title: 设备ID
                use_discount:
                  type: boolean
                  title: 是否使用算力券
              required:
                - billing_type
                - device_id
                - use_discount
              x-apifox-orders:
                - billing_type
                - device_id
                - use_discount
            example:
              billing_type: Hour
              device_id: 250
              use_discount: true
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
                    type: 'null'
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
                data: null
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 共绩算力 Open API/裸金属/创建订单
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-496853781-run
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