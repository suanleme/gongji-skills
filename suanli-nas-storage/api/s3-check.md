# 校验对象存储连接

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/storage/nas/v1/encrypt/s3/check:
    post:
      summary: 校验对象存储连接
      deprecated: false
      description: >-
        ### **接口说明**


        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 是 | 是 |


        ### **描述**


        校验对象存储连接是否可用。请求体须加密后以 text/plain 提交。AccessKey 和 SecretKey
        仅用于本次请求，不会保存。接口成功时请以 data.pass 判断连接是否通过。

        加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)
      tags:
        - 共绩算力 Open API/存储/集群存储/S3互传
        - 共绩算力 Open API/存储/集群存储/S3互传
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
              $ref: '#/components/schemas/S3CheckReq'
            example:
              supplier: tencent
              endpoint: cos.ap-guangzhou.myqcloud.com
              ak: your-access-key
              sk: your-secret-key
              bucket: my-bucket
              prefix: /data/
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/S3CheckEnvelope'
              example:
                code: '0000'
                message: success
                data:
                  pass: true
                  message: null
          headers: {}
          x-apifox-name: ''
      security: []
      x-apifox-folder: 共绩算力 Open API/存储/集群存储/S3互传
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-502709069-run
components:
  schemas:
    S3CheckReq:
      type: object
      title: 连接校验请求
      required:
        - supplier
        - endpoint
        - ak
        - sk
        - bucket
        - prefix
      properties:
        supplier:
          type: string
          title: 对象存储厂商
          description: 如 tencent、aws、aliyun、minio
        endpoint:
          type: string
          title: 对象存储 Endpoint
        ak:
          type: string
          title: AccessKey
          description: 仅用于本次请求，不会保存
        sk:
          type: string
          title: SecretKey
          description: 仅用于本次请求，不会保存
        bucket:
          type: string
          title: Bucket 名称
        prefix:
          type: string
          title: 对象前缀
      x-apifox-orders:
        - supplier
        - endpoint
        - ak
        - sk
        - bucket
        - prefix
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    S3CheckEnvelope:
      type: object
      required:
        - data
        - code
        - message
      properties:
        data:
          $ref: '#/components/schemas/S3CheckData'
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
    S3CheckData:
      type: object
      title: 连接校验结果
      required:
        - pass
      properties:
        pass:
          type: boolean
          title: 是否通过
        message:
          type: string
          title: 说明
          nullable: true
      x-apifox-orders:
        - pass
        - message
      x-apifox-ignore-properties: []
      nullable: true
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
