# 重试对象存储互传任务

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/storage/nas/v1/encrypt/s3/retry:
    post:
      summary: 重试对象存储互传任务
      deprecated: false
      description: >-
        ### **接口说明**


        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 是 | 是 |


        ### **描述**


        对 Exception 或 Error 状态的任务重新提交。请求体须加密后以 text/plain 提交。原任务将标记为
        Deleted，并创建新任务。应答中的 id 为新任务 ID，status 为 Queuing。

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
              $ref: '#/components/schemas/S3RetryReq'
            example:
              id: 488
              storage_id: 1001
              name: prod-backup-sync-retry
              direction: 1
              s3_supplier: tencent
              s3_endpoint: cos.ap-guangzhou.myqcloud.com
              s3_access_key: your-access-key
              s3_secret_key: your-secret-key
              s3_bucket: company-backups
              s3_prefix: nas-sync/
              nas_path: /data/incoming
              overwrite_policy: 2
              ignore_patterns: []
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
                  id: 502
                  status: Queuing
          headers: {}
          x-apifox-name: ''
      security: []
      x-apifox-folder: 共绩算力 Open API/存储/集群存储/S3互传
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-502709066-run
components:
  schemas:
    S3RetryReq:
      type: object
      title: 重试互传任务请求
      required:
        - id
        - storage_id
        - direction
        - s3_supplier
        - s3_endpoint
        - s3_access_key
        - s3_secret_key
        - s3_bucket
      properties:
        id:
          type: integer
          format: int64
          title: 原任务 ID
          description: 原任务状态必须为 Exception 或 Error
        storage_id:
          type: integer
          format: int64
          title: 卷 ID
          description: 可与原任务不同，必须为 Active
        name:
          type: string
          title: 任务名称
          description: 为空时由系统生成
        direction:
          $ref: '#/components/schemas/S3Direction'
        s3_supplier:
          type: string
          title: 对象存储厂商
        s3_endpoint:
          type: string
          title: 对象存储 Endpoint
        s3_access_key:
          type: string
          title: AccessKey
          description: 仅用于本次请求，不会保存
        s3_secret_key:
          type: string
          title: SecretKey
          description: 仅用于本次请求，不会保存
        s3_bucket:
          type: string
          title: Bucket 名称
        s3_prefix:
          type: string
          title: 对象前缀
          nullable: true
        nas_path:
          type: string
          title: 集群存储路径
          nullable: true
        overwrite_policy:
          $ref: '#/components/schemas/S3OverwritePolicy'
        ignore_patterns:
          type: array
          title: 忽略规则
          items:
            type: string
          nullable: true
      x-apifox-orders:
        - id
        - storage_id
        - name
        - direction
        - s3_supplier
        - s3_endpoint
        - s3_access_key
        - s3_secret_key
        - s3_bucket
        - s3_prefix
        - nas_path
        - overwrite_policy
        - ignore_patterns
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    S3OverwritePolicy:
      type: integer
      format: int32
      title: 同名文件策略
      description: 1 强制覆盖；2 跳过重名；3 按内容哈希比较。未传时默认为 2
      enum:
        - 1
        - 2
        - 3
      x-apifox-folder: ''
    S3Direction:
      type: integer
      format: int32
      title: 传输方向
      description: 1 从对象存储同步到集群存储；2 从集群存储同步到对象存储
      enum:
        - 1
        - 2
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
