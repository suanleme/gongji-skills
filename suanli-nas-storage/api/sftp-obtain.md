# 获取 SFTP 连接

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/storage/nas/v1/sftp/obtain:
    post:
      summary: 获取 SFTP 连接
      deprecated: false
      description: >-
        ### **接口说明**


        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 否 | 是 |


        ### **描述**


        获取指定卷的 SFTP 会话，可重复调用。status 为 Running 时返回连接信息；为 Pending 时表示开通中，请稍后再次查询。

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
                $ref: '#/components/schemas/SftpObtainEnvelope'
              example:
                code: '0000'
                message: success
                data:
                  id: 1
                  status: Running
                  username: sftp_user
                  password: example-password
                  sftp_url: sftp.example.com:22
                  web_url: sftp.example.com:80
                  webdav_url: sftp.example.com:81
                  expire_at: '2026-07-09 12:00:00'
                  error_code: null
                  error_message: null
          headers: {}
          x-apifox-name: ''
      security: []
      x-apifox-folder: 共绩算力 Open API/存储/集群存储/SFTP
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-502709070-run
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
    SftpObtainEnvelope:
      type: object
      required:
        - data
        - code
        - message
      properties:
        data:
          $ref: '#/components/schemas/SftpObtainData'
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
    SftpObtainData:
      type: object
      title: SFTP 会话
      required:
        - id
        - status
      properties:
        id:
          type: integer
          format: int64
          title: 会话 ID
        status:
          $ref: '#/components/schemas/SftpStatus'
        username:
          type: string
          title: 用户名
          description: 仅 status 为 Running 时返回
          nullable: true
        password:
          type: string
          title: 密码
          description: 仅 status 为 Running 时返回
          nullable: true
        sftp_url:
          type: string
          title: SFTP 地址
          description: 格式为 host:port。仅 status 为 Running 时返回
          nullable: true
        web_url:
          type: string
          title: Web 入口
          description: 仅 status 为 Running 时返回
          nullable: true
        webdav_url:
          type: string
          title: WebDAV 入口
          description: 仅 status 为 Running 时返回
          nullable: true
        expire_at:
          type: string
          title: 过期时间
          description: 格式 yyyy-MM-dd HH:mm:ss。非 Running 时为 null
          nullable: true
        error_code:
          type: string
          title: 错误码
          nullable: true
        error_message:
          type: string
          title: 错误信息
          nullable: true
      x-apifox-orders:
        - id
        - status
        - username
        - password
        - sftp_url
        - web_url
        - webdav_url
        - expire_at
        - error_code
        - error_message
      x-apifox-ignore-properties: []
      nullable: true
      x-apifox-folder: ''
    SftpStatus:
      type: string
      title: SFTP 状态
      description: Pending 开通中；Running 可连接；Exception 异常
      enum:
        - Pending
        - Running
        - Exception
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
