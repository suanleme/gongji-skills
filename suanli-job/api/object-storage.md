# 获取对象存储加速资源列表

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/storage/get_storage:
    get:
      summary: 获取对象存储加速资源列表
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        获取存储资源列表及其相关信息。
      tags:
        - 共绩算力 Open API/资源
        - 共绩算力 Open API/存储
      parameters:
        - name: storage_type
          in: query
          description: 存储类型
          required: true
          example: Juicefs
          schema:
            type: string
            enum:
              - Juicefs
            x-apifox-enum:
              - value: Juicefs
                name: ''
                description: 对象存储加速
        - name: status
          in: query
          description: 状态
          required: true
          example: Activate,Unactivated
          schema:
            type: string
            enum:
              - Activate
              - Unactivated
            x-apifox-enum:
              - value: Activate
                name: ''
                description: ''
              - value: Unactivated
                name: ''
                description: ''
        - name: page
          in: query
          description: 页码
          required: false
          example: 1
          schema:
            type: number
        - name: page_size
          in: query
          description: |
            每页条数
          required: false
          example: 10
          schema:
            type: number
        - name: token
          in: header
          description: 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。
          required: true
          example: ''
          schema:
            type: string
        - name: timestamp
          in: header
          description: 时间戳
          required: true
          example: 1770194570564
          schema:
            type: number
        - name: version
          in: header
          description: 固定值
          required: true
          example: 1.0.0
          schema:
            type: string
      responses:
        '200':
          x-apifox-name: 成功
          description: ''
          content:
            application/json:
              schema:
                type: object
                x-apifox-refs:
                  01KFAEJ984MTVK3394K95062QJ:
                    $ref: '#/components/schemas/IResponse'
                    x-apifox-overrides: {}
                properties:
                  code:
                    type: string
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
                    description: 当code≠0000时，data必为null。
                    title: 响应码
                  message:
                    type: string
                    title: 响应信息
                    nullable: true
                  data:
                    type: object
                    properties:
                      count:
                        type: number
                      results:
                        type: array
                        items:
                          type: object
                          x-apifox-refs:
                            01KFAEM4Q4C2KBK4MJB3AKQ4NK:
                              $ref: '#/components/schemas/IStorage'
                              x-apifox-overrides:
                                share_storage_type: null
                                syncing_regions: null
                          x-apifox-orders:
                            - 01KFAEM4Q4C2KBK4MJB3AKQ4NK
                          properties:
                            storage_id:
                              type: number
                              description: 存储桶id
                            storage_type:
                              type: string
                              enum:
                                - ShareStorage
                                - Juicefs
                              x-apifox-enum:
                                - value: ShareStorage
                                  name: ''
                                  description: 共享存储卷
                                - value: Juicefs
                                  name: ''
                                  description: 对象存储加速
                              description: 存储桶类型
                              nullable: true
                            juicefs_region_id:
                              type: number
                              description: 对象存储加速-区域id
                            storage_name:
                              type: string
                              description: 存储桶名称
                            k3s_cloud_name:
                              type: string
                              description: 对象存储加速-云服务商名称
                            k3s_region_name:
                              type: string
                              description: 对象存储加速-云服务商区域
                            regions:
                              type: array
                              items:
                                type: object
                                properties:
                                  tag:
                                    type: string
                                    description: 区域tag
                                  name:
                                    type: string
                                    description: 区域名称
                                x-apifox-orders:
                                  - tag
                                  - name
                                required:
                                  - tag
                                  - name
                                x-apifox-ignore-properties: []
                              description: 区域列表
                              nullable: true
                            activate_regions:
                              type: array
                              items:
                                type: object
                                properties:
                                  tag:
                                    type: string
                                    description: 区域tag
                                  name:
                                    type: string
                                    description: 区域名称
                                x-apifox-orders:
                                  - tag
                                  - name
                                required:
                                  - tag
                                  - name
                                x-apifox-ignore-properties: []
                              description: 对象存储加速-已回源区域列表（可被正常使用）
                              nullable: true
                            bucket:
                              type: string
                              description: 对象存储加速-存储桶名称
                            size:
                              type: number
                              description: 共享存储卷-存储桶总容量
                              nullable: true
                            dir:
                              type: string
                              description: 对象存储加速-存储桶内被加速的目录
                            endpoint:
                              type: string
                              description: 对象存储加速-endpoint
                            status:
                              type: string
                              enum:
                                - Unactivated
                                - Activate
                              x-apifox-enum:
                                - value: Unactivated
                                  name: ''
                                  description: 未加速
                                - value: Activate
                                  name: ''
                                  description: 加速中
                              description: 是否加速
                            last_sync_time:
                              type: string
                              description: 对象存储加速-最后同步回源时间
                              nullable: true
                            deployments:
                              type: array
                              items:
                                type: object
                                properties:
                                  deployment_id:
                                    type: string
                                    description: 任务id
                                  deployment_name:
                                    type: string
                                    description: 任务名
                                  target_dir:
                                    type: string
                                    description: 任务挂载目录
                                  task_type:
                                    type: string
                                    description: 任务类型
                                    enum:
                                      - Deployment
                                      - Development
                                    x-apifox-enum:
                                      - value: Deployment
                                        name: ''
                                        description: 弹性服务部署
                                      - value: Development
                                        name: ''
                                        description: 云主机
                                  regions:
                                    type: array
                                    items:
                                      type: object
                                      properties:
                                        tag:
                                          type: string
                                          description: 区域tag
                                        name:
                                          type: string
                                          description: 区域名称
                                      x-apifox-orders:
                                        - tag
                                        - name
                                      required:
                                        - tag
                                        - name
                                      x-apifox-ignore-properties: []
                                x-apifox-orders:
                                  - deployment_id
                                  - deployment_name
                                  - target_dir
                                  - task_type
                                  - regions
                                required:
                                  - deployment_id
                                  - deployment_name
                                  - target_dir
                                  - task_type
                                  - regions
                                x-apifox-ignore-properties: []
                              description: 所关联的任务
                              nullable: true
                            remark:
                              type: string
                              description: 备注
                              nullable: true
                            use_size:
                              type: number
                              description: "对象存储加速-\t加速用量\n共享存储卷-存储用量"
                              nullable: true
                            create_time:
                              type: string
                              description: 创建时间（RFC3339）格式
                          required:
                            - storage_id
                            - storage_type
                            - juicefs_region_id
                            - storage_name
                            - k3s_cloud_name
                            - k3s_region_name
                            - regions
                            - activate_regions
                            - bucket
                            - size
                            - dir
                            - endpoint
                            - status
                            - last_sync_time
                            - deployments
                            - remark
                            - use_size
                            - create_time
                          x-apifox-ignore-properties:
                            - storage_id
                            - storage_type
                            - juicefs_region_id
                            - storage_name
                            - k3s_cloud_name
                            - k3s_region_name
                            - regions
                            - activate_regions
                            - bucket
                            - size
                            - dir
                            - endpoint
                            - status
                            - last_sync_time
                            - deployments
                            - remark
                            - use_size
                            - create_time
                    x-apifox-orders:
                      - count
                      - results
                    required:
                      - count
                      - results
                    x-apifox-ignore-properties: []
                    nullable: true
                required:
                  - code
                  - message
                  - data
                x-apifox-orders:
                  - 01KFAEJ984MTVK3394K95062QJ
                  - data
                x-apifox-ignore-properties:
                  - code
                  - message
              example:
                code: '0000'
                message: success
                data:
                  count: 1
                  results:
                    - storage_id: 36
                      storage_type: Juicefs
                      juicefs_region_id: 531
                      storage_name: 火山引擎
                      k3s_cloud_name: 火山引擎
                      k3s_region_name: 华北2 - 北京
                      regions:
                        - tag: guangdong-t-01
                          name: 广东-T1
                      activate_regions:
                        - tag: guangdong-t-01
                          name: 广东-T1
                      bucket: test
                      size: 18506235904
                      dir: /test
                      endpoint: https://test.com
                      status: Activate
                      last_sync_time: '2026-01-19T11:52:18.110268+08:00'
                      deployments:
                        - deployment_id: 1
                          deployment_name: test
                          target_dir: /data
                          task_type: Deployment
                          regions:
                            - tag: guangdong-t-01
                              name: 广东-T1
                      remark: null
                      use_size: 18506235904
                      create_time: '2025-12-29T16:15:47.736468+08:00'
                      share_storage_type: null
                      syncing_regions: null
          headers: {}
      security: []
      x-apifox-folder: 共绩算力 Open API/资源
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-314646799-run
components:
  schemas:
    IStorage:
      type: object
      properties:
        storage_id:
          type: number
          description: 存储桶id
        storage_type:
          type: string
          enum:
            - ShareStorage
            - Juicefs
          x-apifox-enum:
            - value: ShareStorage
              name: ''
              description: 共享存储卷
            - value: Juicefs
              name: ''
              description: 对象存储加速
          description: 存储桶类型
          nullable: true
        juicefs_region_id:
          type: number
          description: 对象存储加速-区域id
        storage_name:
          type: string
          description: 存储桶名称
        k3s_cloud_name:
          type: string
          description: 对象存储加速-云服务商名称
        k3s_region_name:
          type: string
          description: 对象存储加速-云服务商区域
        regions:
          type: array
          items:
            type: object
            properties:
              tag:
                type: string
                description: 区域tag
              name:
                type: string
                description: 区域名称
            x-apifox-orders:
              - tag
              - name
            required:
              - tag
              - name
            x-apifox-ignore-properties: []
          description: 区域列表
          nullable: true
        activate_regions:
          type: array
          items:
            type: object
            properties:
              tag:
                type: string
                description: 区域tag
              name:
                type: string
                description: 区域名称
            x-apifox-orders:
              - tag
              - name
            required:
              - tag
              - name
            x-apifox-ignore-properties: []
          description: 对象存储加速-已回源区域列表（可被正常使用）
          nullable: true
        bucket:
          type: string
          description: 对象存储加速-存储桶名称
        size:
          type: number
          description: 共享存储卷-存储桶总容量
          nullable: true
        dir:
          type: string
          description: 对象存储加速-存储桶内被加速的目录
        endpoint:
          type: string
          description: 对象存储加速-endpoint
        status:
          type: string
          enum:
            - Unactivated
            - Activate
          x-apifox-enum:
            - value: Unactivated
              name: ''
              description: 未加速
            - value: Activate
              name: ''
              description: 加速中
          description: 是否加速
        last_sync_time:
          type: string
          description: 对象存储加速-最后同步回源时间
          nullable: true
        deployments:
          type: array
          items:
            type: object
            properties:
              deployment_id:
                type: string
                description: 任务id
              deployment_name:
                type: string
                description: 任务名
              target_dir:
                type: string
                description: 任务挂载目录
              task_type:
                type: string
                description: 任务类型
                enum:
                  - Deployment
                  - Development
                x-apifox-enum:
                  - value: Deployment
                    name: ''
                    description: 弹性服务部署
                  - value: Development
                    name: ''
                    description: 云主机
              regions:
                type: array
                items:
                  type: object
                  properties:
                    tag:
                      type: string
                      description: 区域tag
                    name:
                      type: string
                      description: 区域名称
                  x-apifox-orders:
                    - tag
                    - name
                  required:
                    - tag
                    - name
                  x-apifox-ignore-properties: []
            x-apifox-orders:
              - deployment_id
              - deployment_name
              - target_dir
              - task_type
              - regions
            required:
              - deployment_id
              - deployment_name
              - target_dir
              - task_type
              - regions
            x-apifox-ignore-properties: []
          description: 所关联的任务
          nullable: true
        remark:
          type: string
          description: 备注
          nullable: true
        use_size:
          type: number
          description: "对象存储加速-\t加速用量\n共享存储卷-存储用量"
          nullable: true
        create_time:
          type: string
          description: 创建时间（RFC3339）格式
        share_storage_type:
          type: string
          enum:
            - Single
            - Multiple
          x-apifox-enum:
            - value: Single
              name: ''
              description: 单区域
            - value: Multiple
              name: ''
              description: 多区域
          description: 共享存储卷-类型
          nullable: true
        syncing_regions:
          type: array
          items:
            type: object
            properties:
              tag:
                type: string
                description: 区域tag
              name:
                type: string
                description: 区域名称
            x-apifox-orders:
              - tag
              - name
            required:
              - tag
              - name
            x-apifox-ignore-properties: []
          description: 共享存储卷-正在回源中的区域
          nullable: true
      x-apifox-orders:
        - storage_id
        - storage_type
        - juicefs_region_id
        - storage_name
        - k3s_cloud_name
        - k3s_region_name
        - regions
        - activate_regions
        - bucket
        - size
        - dir
        - endpoint
        - status
        - last_sync_time
        - deployments
        - remark
        - use_size
        - create_time
        - share_storage_type
        - syncing_regions
      required:
        - storage_id
        - storage_type
        - juicefs_region_id
        - storage_name
        - k3s_cloud_name
        - k3s_region_name
        - regions
        - activate_regions
        - bucket
        - size
        - dir
        - endpoint
        - status
        - last_sync_time
        - deployments
        - remark
        - use_size
        - create_time
        - share_storage_type
        - syncing_regions
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    IResponse:
      type: object
      properties:
        code:
          type: string
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
          description: 当code≠0000时，data必为null。
          title: 响应码
        message:
          type: string
          title: 响应信息
          nullable: true
      required:
        - code
        - message
      x-apifox-orders:
        - code
        - message
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
  securitySchemes: {}
servers:
  - url: https://openapi.suanli.cn
    description: 正式环境
security: []

```