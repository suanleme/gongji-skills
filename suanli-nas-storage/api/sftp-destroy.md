# 关闭 SFTP 连接

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/storage/nas/v1/sftp/destroy:
    post:
      summary: 关闭 SFTP 连接
      deprecated: false
      description: >-
        ### **接口说明**


        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 否 | 是 |


        ### **描述**


        关闭指定卷的 SFTP 会话并清除凭证。关闭后再次获取将生成新凭证。

        加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)
      tags:
        - 共绩算力 Open API/存储/集群存储/SFTP
        - 共绩算力 Open API/存储/集群存储/SFTP
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
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SftpReq'
            example:
              storage_id: 1001
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SftpDestroyEnvelope'
              example:
                code: '0000'
                message: success
                data: null
          headers: {}
          x-apifox-name: ''
      security: []
      x-apifox-folder: 共绩算力 Open API/存储/集群存储/SFTP
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-502709071-run
components:
  schemas:
    SftpReq:
      type: object
      title: SFTP 请求
      required:
        - storage_id
      properties:
        storage_id:
          type: integer
          format: int64
          title: 卷 ID
          description: 必须大于 0
      x-apifox-orders:
        - storage_id
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    SftpDestroyEnvelope:
      type: object
      required:
        - data
        - code
        - message
      properties:
        data:
          type: 'null'
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
  - url: https://openapi.suanli.cn
    description: 正式环境
security: []

```
