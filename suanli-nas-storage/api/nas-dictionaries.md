# 查询集群存储字典

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/storage/nas/v1/dictionaries:
    get:
      summary: 查询集群存储字典
      deprecated: false
      description: >-
        ### **接口说明**


        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 否 | 是 |


        ### **描述**


        查询当前租户可选的地域和存储规格。

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
                $ref: '#/components/schemas/NasDictionariesEnvelope'
              example:
                code: '0000'
                message: success
                data:
                  regions:
                    - tag: bj-001
                      name: 北京一区
                    - tag: sh-001
                      name: 上海一区
                  storage_classes:
                    - storage_class: nfs-standard
                      storage_class_name: 标准型
                    - storage_class: nfs-premium
                      storage_class_name: 高性能型
          headers: {}
          x-apifox-name: ''
      security: []
      x-apifox-folder: 共绩算力 Open API/存储/集群存储/存储卷
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-502709056-run
components:
  schemas:
    NasDictionariesEnvelope:
      type: object
      required:
        - data
        - code
        - message
      properties:
        data:
          type: object
          required:
            - regions
            - storage_classes
          properties:
            regions:
              type: array
              title: 地域列表
              items:
                $ref: '#/components/schemas/RegionDto'
            storage_classes:
              type: array
              title: 存储规格列表
              items:
                $ref: '#/components/schemas/StorageClassDto'
          x-apifox-orders:
            - regions
            - storage_classes
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
    StorageClassDto:
      type: object
      title: 存储规格
      required:
        - storage_class
        - storage_class_name
      properties:
        storage_class:
          type: string
          title: 规格标识
        storage_class_name:
          type: string
          title: 规格名称
      x-apifox-orders:
        - storage_class
        - storage_class_name
      x-apifox-ignore-properties: []
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
