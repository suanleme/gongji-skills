# 查询集群存储卷列表

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/storage/nas/v1/list:
    get:
      summary: 查询集群存储卷列表
      deprecated: false
      description: >-
        ### **接口说明**


        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 否 | 是 |


        ### **描述**


        分页查询当前租户的集群存储卷。statuses 中的 Deleted 会被忽略。

        加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)
      tags:
        - 共绩算力 Open API/存储/集群存储/存储卷
        - 共绩算力 Open API/存储/集群存储/存储卷
      parameters:
        - name: regions
          in: query
          description: 地域标识，多个值用英文逗号分隔
          required: false
          example: bj-001,sh-001
          schema:
            type: string
        - name: storage_class
          in: query
          description: 存储规格标识，多个值用英文逗号分隔
          required: false
          example: nfs-standard
          schema:
            type: string
        - name: statuses
          in: query
          description: >-
            卷状态，多个值用英文逗号分隔。可选值
            Creating（创建中）、Active（可用）、Expanding（扩容中）、Deleting（删除中）、Exception（异常）。Deleted
            会被忽略。
          required: false
          example: Creating,Active
          schema:
            type: string
        - name: storage_ids
          in: query
          description: 卷 ID，多个值用英文逗号分隔
          required: false
          example: 1001,1002
          schema:
            type: string
        - name: page
          in: query
          description: 页码，从 1 开始。小于等于 0 时按 1 处理
          required: false
          example: 1
          schema:
            type: integer
            format: int64
        - name: page_size
          in: query
          description: 每页条数。小于等于 0 时按 10 处理，最大 100
          required: false
          example: 10
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
                $ref: '#/components/schemas/NasListEnvelope'
              example:
                code: '0000'
                message: success
                data:
                  count: 1
                  results:
                    - storage_id: 1001
                      name: my-volume
                      region:
                        tag: bj-001
                        name: 北京一区
                      storage_class: nfs-standard
                      storage_class_name: 标准型
                      unit_price: 120
                      display_unit_price: '0.36'
                      total_size: 1073741824
                      used_size: 268435456
                      status: Active
                      namespace: tenant-ns
                      claim_name: pvc-1001
                      instance_count: 1
                      instances:
                        - instance_id: 2001
                          instance_name: training-job-1
                          instance_type: deployment
                          mount_path: /data/nas
                      create_time: '2026-06-12 10:00:00'
                      last_update_time: '2026-06-12 12:30:00'
                      error_code: null
                      error_message: null
          headers: {}
          x-apifox-name: ''
      security: []
      x-apifox-folder: 共绩算力 Open API/存储/集群存储/存储卷
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-502709058-run
components:
  schemas:
    NasListEnvelope:
      type: object
      required:
        - data
        - code
        - message
      properties:
        data:
          type: object
          required:
            - count
            - results
          properties:
            count:
              type: integer
              format: int64
              title: 总条数
            results:
              type: array
              title: 当前页数据
              items:
                $ref: '#/components/schemas/StorageNasRecordItem'
          x-apifox-orders:
            - count
            - results
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
    StorageNasRecordItem:
      type: object
      title: 存储卷
      required:
        - storage_id
        - name
        - region
        - storage_class
        - storage_class_name
        - unit_price
        - display_unit_price
        - total_size
        - used_size
        - status
        - namespace
        - claim_name
        - instance_count
        - instances
        - create_time
        - last_update_time
      properties:
        storage_id:
          type: integer
          format: int64
          title: 卷 ID
        name:
          type: string
          title: 卷名称
        region:
          $ref: '#/components/schemas/RegionDto'
        storage_class:
          type: string
          title: 规格标识
        storage_class_name:
          type: string
          title: 规格名称
        unit_price:
          type: integer
          format: int64
          title: 单价
          description: 单位为积分每 GB 每 10 分钟
        display_unit_price:
          type: string
          title: 展示单价
          description: 单位为元每 GB 每月
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
        status:
          $ref: '#/components/schemas/NasVolumeStatus'
        namespace:
          type: string
          title: 命名空间
        claim_name:
          type: string
          title: 存储声明名称
        instance_count:
          type: integer
          format: int64
          title: 挂载实例数
        instances:
          type: array
          title: 挂载实例列表
          items:
            $ref: '#/components/schemas/MountedInstanceDto'
        create_time:
          type: string
          title: 创建时间
          description: 格式 yyyy-MM-dd HH:mm:ss
        last_update_time:
          type: string
          title: 更新时间
          description: 格式 yyyy-MM-dd HH:mm:ss
        error_code:
          type: string
          title: 错误码
          nullable: true
        error_message:
          type: string
          title: 错误信息
          nullable: true
      x-apifox-orders:
        - storage_id
        - name
        - region
        - storage_class
        - storage_class_name
        - unit_price
        - display_unit_price
        - total_size
        - used_size
        - status
        - namespace
        - claim_name
        - instance_count
        - instances
        - create_time
        - last_update_time
        - error_code
        - error_message
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    MountedInstanceDto:
      type: object
      title: 挂载实例
      properties:
        instance_id:
          type: integer
          format: int64
          title: 实例 ID
        instance_name:
          type: string
          title: 实例名称
        instance_type:
          type: string
          title: 实例类型
        mount_path:
          type: string
          title: 挂载路径
      x-apifox-orders:
        - instance_id
        - instance_name
        - instance_type
        - mount_path
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    NasVolumeStatus:
      type: string
      title: 卷状态
      description: >-
        Creating 创建中；Active 可用；Expanding 扩容中；Deleting 删除中；Deleted 已删除；Exception
        异常
      enum:
        - Creating
        - Active
        - Expanding
        - Deleting
        - Deleted
        - Exception
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
