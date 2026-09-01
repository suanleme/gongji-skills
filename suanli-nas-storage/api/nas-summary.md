# 查询集群存储用量概览

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/storage/nas/v1/summary:
    get:
      summary: 查询集群存储用量概览
      deprecated: false
      description: >-
        ### **接口说明**


        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 否 | 是 |


        ### **描述**


        查询当前租户集群存储卷的数量、容量、已用量和预估费用。仅统计创建中、可用、扩容中的卷。

        加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)
      tags:
        - 共绩算力 Open API/存储/集群存储/存储卷
        - 共绩算力 Open API/存储/集群存储/存储卷
      parameters:
        - name: token
          in: header
          description: 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。
          required: true
          example: a69abd35-1df0-4c21-9c2b-82a20a72d3b2-20260417200925
          schema:
            type: string
        - name: timestamp
          in: header
          description: 时间戳
          required: true
          example: '{{$date.millisecondsTimestamp}}'
          schema:
            type: integer
        - name: version
          in: header
          description: 固定值
          required: true
          example: 1.0.0
          schema:
            type: string
        - name: sign_str
          in: header
          description: 如果token为简易模式则无需填写此字段
          required: false
          example: ''
          schema:
            type: string
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NasSummaryEnvelope'
              example:
                code: '0000'
                message: success
                data:
                  volume_count: 3
                  total_size: 3221225472
                  used_size: 1073741824
                  estimated_price: 120
                  coin_sum_slice: 360
          headers: {}
          x-apifox-name: ''
      security: []
      x-apifox-folder: 共绩算力 Open API/存储/集群存储/存储卷
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-502709055-run
components:
  schemas:
    NasSummaryEnvelope:
      type: object
      required:
        - data
        - code
        - message
      properties:
        data:
          type: object
          required:
            - volume_count
            - total_size
            - used_size
            - coin_sum_slice
          properties:
            volume_count:
              type: integer
              format: int64
              title: 卷数量
              description: 仅统计 Creating、Active、Expanding
            total_size:
              type: integer
              format: int64
              title: 总容量
              description: 单位为字节
            used_size:
              type: integer
              format: int64
              title: 已使用容量
              description: 单位为字节。值为 -1 时表示该存储暂不支持查询已用容量，不要按字节换算。
            estimated_price:
              type: integer
              format: int64
              title: 预估单价
              description: 有效卷单价的算术平均。无卷时为 null
              nullable: true
            coin_sum_slice:
              type: integer
              format: int64
              title: 预估消耗
              description: 每 10 分钟预估消耗，单位为分
          x-apifox-orders:
            - volume_count
            - total_size
            - used_size
            - estimated_price
            - coin_sum_slice
          x-apifox-ignore-properties: []
          nullable: true
        code:
          $ref: '#/components/schemas/ResponseCode'
        message:
          type: string
          title: 响应信息
          nullable: true
      x-apifox-orders:
        - data
        - code
        - message
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    ResponseCode:
      type: string
      title: 响应码
      description: 当 code 不为 0000 时，data 为 null。
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
      x-apifox-folder: ''
  securitySchemes:
    AdminAuth:
      type: jwt
      scheme: bearer
      bearerFormat: JWT
      description: 运营中台管理员登录态；需具备权限 `tenant:create_offline_metal_order`
servers:
  - url: https://openapi.suanleme.cn
    description: 生产环境
security: []

```
