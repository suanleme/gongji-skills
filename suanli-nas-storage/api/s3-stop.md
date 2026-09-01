# 停止对象存储互传任务

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/storage/nas/v1/s3/stop:
    post:
      summary: 停止对象存储互传任务
      deprecated: false
      description: >-
        ### **接口说明**


        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 否 | 是 |


        ### **描述**


        停止运行中的对象存储互传任务。仅 Running 状态可停止。成功后 status 为 Stopped。

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
              $ref: '#/components/schemas/S3IdReq'
            example:
              id: 501
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/S3WriteEnvelope'
              example:
                code: '0000'
                message: success
                data:
                  id: 501
                  status: Stopped
          headers: {}
          x-apifox-name: ''
      security: []
      x-apifox-folder: 共绩算力 Open API/存储/集群存储/S3互传
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-502709068-run
components:
  schemas:
    S3IdReq:
      type: object
      title: 任务 ID 请求
      required:
        - id
      properties:
        id:
          type: integer
          format: int64
          title: 任务 ID
          description: 必须大于 0
      x-apifox-orders:
        - id
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    S3WriteEnvelope:
      type: object
      required:
        - data
        - code
        - message
      properties:
        data:
          $ref: '#/components/schemas/S3WriteData'
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
    S3WriteData:
      type: object
      title: 互传写操作结果
      required:
        - id
        - status
      properties:
        id:
          type: integer
          format: int64
          title: 任务 ID
        status:
          $ref: '#/components/schemas/S3TaskStatus'
      x-apifox-orders:
        - id
        - status
      x-apifox-ignore-properties: []
      nullable: true
      x-apifox-folder: ''
    S3TaskStatus:
      type: string
      title: 互传任务状态
      description: >-
        Queuing 排队中；Pending 处理中；Running 运行中；Stopped 已停止；Completed 已完成；Error
        失败；Exception 异常；Deleted 已删除
      enum:
        - Queuing
        - Pending
        - Running
        - Stopped
        - Completed
        - Error
        - Exception
        - Deleted
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
