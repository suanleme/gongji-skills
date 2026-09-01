# 查询可创建的存储配置

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/storage/nas/v1/pre-create:
    get:
      summary: 查询可创建的存储配置
      deprecated: false
      description: >-
        ### **接口说明**


        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 否 | 是 |


        ### **描述**


        查询当前租户可用于创建卷的存储配置。Unavailable 表示暂不可选，不会返回已下线配置。

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
                $ref: '#/components/schemas/NasPreCreateEnvelope'
              example:
                code: '0000'
                message: success
                data:
                  configs:
                    - id: 10
                      name: 北京标准型
                      description: null
                      region:
                        tag: bj-001
                        name: 北京一区
                      storage_class: nfs-standard
                      storage_class_name: 标准型
                      total_capacity: 1099511627776
                      allocated_capacity: 107374182400
                      used_capacity: 53687091200
                      unit_price: 120
                      display_unit_price: '0.36'
                      status: Available
          headers: {}
          x-apifox-name: ''
      security: []
      x-apifox-folder: 共绩算力 Open API/存储/集群存储/存储卷
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-502709057-run
components:
  schemas:
    NasPreCreateEnvelope:
      type: object
      required:
        - data
        - code
        - message
      properties:
        data:
          type: object
          required:
            - configs
          properties:
            configs:
              type: array
              title: 存储配置列表
              items:
                $ref: '#/components/schemas/StorageNasConfigDto'
          x-apifox-orders:
            - configs
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
    StorageNasConfigDto:
      type: object
      title: 存储配置
      required:
        - id
        - name
        - region
        - storage_class
        - storage_class_name
        - total_capacity
        - allocated_capacity
        - used_capacity
        - unit_price
        - display_unit_price
        - status
      properties:
        id:
          type: integer
          format: int64
          title: 配置 ID
        name:
          type: string
          title: 配置名称
        description:
          type: string
          title: 配置说明
          nullable: true
        region:
          $ref: '#/components/schemas/RegionDto'
        storage_class:
          type: string
          title: 规格标识
        storage_class_name:
          type: string
          title: 规格名称
        total_capacity:
          type: integer
          format: int64
          title: 集群总容量
          description: 单位为字节
        allocated_capacity:
          type: integer
          format: int64
          title: 已分配容量
          description: 单位为字节
        used_capacity:
          type: integer
          format: int64
          title: 已使用容量
          description: 单位为字节
        unit_price:
          type: integer
          format: int64
          title: 单价
          description: 单位为积分每 GB 每 10 分钟
        display_unit_price:
          type: string
          title: 展示单价
          description: 单位为元每 GB 每月
        status:
          $ref: '#/components/schemas/NasConfigStatus'
      x-apifox-orders:
        - id
        - name
        - description
        - region
        - storage_class
        - storage_class_name
        - total_capacity
        - allocated_capacity
        - used_capacity
        - unit_price
        - display_unit_price
        - status
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    NasConfigStatus:
      type: string
      title: 配置状态
      description: Available 可选；Unavailable 暂不可选
      enum:
        - Available
        - Unavailable
      x-apifox-folder: ''
    RegionDto:
      type: object
      title: 地域
      required:
        - tag
        - name
      properties:
        tag:
          type: string
          title: 地域标识
        name:
          type: string
          title: 地域名称
      x-apifox-orders:
        - tag
        - name
      x-apifox-ignore-properties: []
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
