# 弹性部署/云主机-时间维度计费查询接口

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/billing/get_billing_record:
    get:
      summary: 弹性部署/云主机-时间维度计费查询接口
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        查询弹性部署/云主机的计费信息。
      tags:
        - 共绩算力 Open API/费用
        - 共绩算力 Open API/计费管理
        - 共绩算力 Open API/计费管理
      parameters:
        - name: range
          in: query
          description: 时间粒度
          required: true
          example: day
          schema:
            type: string
            enum:
              - hour
              - day
              - week
              - month
            x-apifox-enum:
              - value: hour
                name: ''
                description: 小时
              - value: day
                name: ''
                description: 天
              - value: week
                name: ''
                description: 周
              - value: month
                name: ''
                description: 月
        - name: start_time
          in: query
          description: 开始时间(RFC3339格式)
          required: true
          example: '2026-01-01T00:00:00+08:00'
          schema:
            type: string
            format: date-time
        - name: end_time
          in: query
          description: 结束时间(RFC3339格式)
          required: true
          example: '2026-01-02T23:59:59+08:00'
          schema:
            type: string
        - name: task_ids
          in: query
          description: 任务ID列表(空字符串表示全部任务)
          required: false
          example: 1,2,3,4
          schema:
            type: string
        - name: page
          in: query
          description: 页码
          required: false
          schema:
            type: number
        - name: page_size
          in: query
          description: 每页条数
          required: false
          schema:
            type: number
        - name: token
          in: header
          description: 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。
          required: true
          example: ''
          schema:
            type: string
        - name: timestamp
          in: header
          description: 时间戳
          required: true
          example: 1770194570564
          schema:
            type: number
        - name: version
          in: header
          description: 固定值
          required: true
          example: 1.0.0
          schema:
            type: string
      responses:
        '200':
          x-apifox-name: 成功
          description: 查询成功
          content:
            application/json:
              schema:
                type: object
                x-apifox-refs:
                  01KFAGV8BC55SVC4GZ1MX2XW5P:
                    $ref: '#/components/schemas/IResponse'
                    x-apifox-overrides: {}
                properties:
                  data:
                    type: object
                    properties:
                      count:
                        type: number
                      results:
                        type: array
                        items:
                          type: object
                          properties:
                            billing_coin:
                              type: number
                              description: 总账
                            discount_coin:
                              type: number
                              description: 优惠抵扣
                            start_time:
                              type: string
                              description: 开始时间
                            end_time:
                              type: string
                              description: 结束时间
                          x-apifox-orders:
                            - billing_coin
                            - discount_coin
                            - start_time
                            - end_time
                          required:
                            - billing_coin
                            - discount_coin
                            - start_time
                            - end_time
                          x--orders:
                            - billing_coin
                            - discount_coin
                            - start_time
                            - end_time
                          x--ignore-properties: []
                    x-apifox-orders:
                      - count
                      - results
                    required:
                      - count
                      - results
                    x--orders:
                      - count
                      - results
                    x--ignore-properties: []
                    nullable: true
                required:
                  - data
                x-apifox-orders:
                  - 01KFAGV8BC55SVC4GZ1MX2XW5P
                  - data
                x--orders:
                  - data
                x--ignore-properties: []
          headers: {}
      security: []
      x-apifox-folder: 共绩算力 Open API/费用
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-310631391-run
components:
  schemas:
    IResponse:
      type: object
      properties:
        code:
          type: string
          enum:
            - '0000'
            - C999
            - C001
            - C002
            - C004
            - C005
            - C006
            - C007
            - C008
            - C009
            - C010
            - Z001
          description: 当code≠0000时，data必为null。
          title: 响应码
        message:
          type: string
          title: 响应信息
          nullable: true
      required:
        - code
        - message
      x-apifox-orders:
        - code
        - message
      x--orders:
        - code
        - message
      x--ignore-properties: []
      x-apifox-folder: ''
  securitySchemes: {}
servers:
  - url: https://openapi.suanli.cn
    description: 正式环境
security: []

```