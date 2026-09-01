# 查询对象存储互传任务详情

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/storage/nas/v1/s3/detail:
    get:
      summary: 查询对象存储互传任务详情
      deprecated: false
      description: >-
        ### **接口说明**


        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 否 | 是 |


        ### **描述**


        按任务 ID 查询对象存储互传详情。应答字段与列表项一致，不含 AccessKey 和 SecretKey。

        加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)
      tags:
        - 共绩算力 Open API/存储/集群存储/S3互传
        - 共绩算力 Open API/存储/集群存储/S3互传
      parameters:
        - name: id
          in: query
          description: 任务 ID，必须大于 0
          required: true
          example: 501
          schema:
            type: integer
            format: int64
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
                $ref: '#/components/schemas/S3DetailEnvelope'
              example:
                code: '0000'
                message: success
                data:
                  id: 501
                  name: s3-sync-demo
                  ready_files: 15
                  total_files: 100
                  transferred_bytes: 5242880
                  total_bytes: 104857600
                  create_time: '2026-07-05 10:00:00'
                  end_time: null
                  status: Exception
                  direction: 1
                  remaining_seconds: 0
                  speed: 5MB/s
                  bps: 5242880
                  last_update_time: '2026-07-05 10:30:00'
                  storage_id: 1001
                  s3_supplier: tencent
                  s3_endpoint: cos.ap-guangzhou.myqcloud.com
                  s3_bucket: my-backup-bucket
                  s3_prefix: project/data/
                  nas_path: /data/backup
                  overwrite_policy: 2
                  ignore_patterns:
                    - .tmp
                    - .log
                  error_code: S410
                  error_message: S3 任务创建失败
                  storage_name: my-volume
          headers: {}
          x-apifox-name: ''
      security: []
      x-apifox-folder: 共绩算力 Open API/存储/集群存储/S3互传
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-502709064-run
components:
  schemas:
    S3DetailEnvelope:
      type: object
      required:
        - data
        - code
        - message
      properties:
        data:
          allOf:
            - $ref: '#/components/schemas/StorageNasS3Item'
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
    StorageNasS3Item:
      type: object
      title: 互传任务
      required:
        - id
        - name
        - ready_files
        - total_files
        - transferred_bytes
        - total_bytes
        - create_time
        - status
        - direction
        - remaining_seconds
        - speed
        - bps
        - last_update_time
        - storage_id
        - s3_supplier
        - s3_endpoint
        - s3_bucket
        - s3_prefix
        - nas_path
        - overwrite_policy
        - ignore_patterns
        - storage_name
      properties:
        id:
          type: integer
          format: int64
          title: 任务 ID
        name:
          type: string
          title: 任务名称
        ready_files:
          type: integer
          format: int64
          title: 已传输文件数
        total_files:
          type: integer
          format: int64
          title: 总文件数
          description: 尚未统计完成时可能为 0
        transferred_bytes:
          type: integer
          format: int64
          title: 已传输字节数
        total_bytes:
          type: integer
          format: int64
          title: 总字节数
          description: 尚未统计完成时可能为 0
        create_time:
          type: string
          title: 创建时间
          description: 格式 yyyy-MM-dd HH:mm:ss
        end_time:
          type: string
          title: 结束时间
          description: 进行中为 null。格式 yyyy-MM-dd HH:mm:ss
          nullable: true
        status:
          $ref: '#/components/schemas/S3TaskStatus'
        direction:
          $ref: '#/components/schemas/S3Direction'
        remaining_seconds:
          type: integer
          format: int64
          title: 预估剩余秒数
          description: 无法估算或已结束时为 0
        speed:
          type: string
          title: 传输速率展示
          deprecated: true
          description: 已废弃，请使用 bps
        bps:
          type: integer
          format: int64
          title: 传输速率
          description: 单位为字节每秒。无法计算或已结束时为 0
        last_update_time:
          type: string
          title: 更新时间
          description: 格式 yyyy-MM-dd HH:mm:ss
        storage_id:
          type: integer
          format: int64
          title: 卷 ID
        s3_supplier:
          type: string
          title: 对象存储厂商
        s3_endpoint:
          type: string
          title: 对象存储 Endpoint
        s3_bucket:
          type: string
          title: Bucket 名称
        s3_prefix:
          type: string
          title: 对象前缀
        nas_path:
          type: string
          title: 集群存储路径
        overwrite_policy:
          $ref: '#/components/schemas/S3OverwritePolicy'
        error_code:
          type: string
          title: 错误码
          nullable: true
        error_message:
          type: string
          title: 错误信息
          nullable: true
        ignore_patterns:
          type: array
          title: 忽略规则
          items:
            type: string
        storage_name:
          type: string
          title: 卷名称
      x-apifox-orders:
        - id
        - name
        - ready_files
        - total_files
        - transferred_bytes
        - total_bytes
        - create_time
        - end_time
        - status
        - direction
        - remaining_seconds
        - speed
        - bps
        - last_update_time
        - storage_id
        - s3_supplier
        - s3_endpoint
        - s3_bucket
        - s3_prefix
        - nas_path
        - overwrite_policy
        - error_code
        - error_message
        - ignore_patterns
        - storage_name
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
