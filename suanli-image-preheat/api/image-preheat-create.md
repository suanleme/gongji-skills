# 镜像预热任务创建接口

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  version: 1.0.0
paths:
  /api/task/image_preheat/create:
    post:
      summary: 镜像预热任务创建接口
      deprecated: false
      description: >-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 否 | 是 |


        ### **描述**

        # 镜像预热任务


        ## 功能描述


        镜像预热任务用于提前将服务镜像缓存到指定的集群区域或资源节点，以减少后续任务启动时拉取镜像所需的时间。


        创建镜像预热任务时支持以下两种预热类型：


        - **仅集群预热**：将镜像预热到所选区域的集群级镜像缓存中。该模式按区域执行，不指定具体资源规格、节点数量和调度策略。

        - **节点预热**：根据指定的资源规格和节点数量创建预热任务，将镜像预热到对应的资源节点。该模式支持配置跨区调度策略。


        接口没有单独的预热类型字段，而是根据 `regions` 和 `resources`
        判断预热类型。两个字段必须二选一，不能同时传入，也不能同时为空。


        ## 创建接口


        ```text

        POST /api/task/image_preheat/create

        ```


        加密创建接口：


        ```text

        POST /api/task/image_preheat/encrypt/create

        ```


        加密接口解密后的业务字段及校验规则与普通创建接口一致。


        ## 字段要求


        | 字段 | 类型 | 仅集群预热 | 节点预热 | 说明 |

        | --- | --- | --- | --- | --- |

        | `task_name` | `string` | 必填 | 必填 | 任务名称，不能为空。 |

        | `resources` | `ResourceMark[] \| null` | 必须为 `null` 或不传 | 必填 |
        节点预热资源列表，至少包含一项。 |

        | `regions` | `ImagePreheatRegionDto[] \| null` | 必填 | 必须为 `null` 或不传 |
        集群预热区域列表，至少包含一个有效区域。 |

        | `scheduler_strategy` | `TaskSchedulerStrategy \| null` | 必须为 `null`
        或不传 | 可选 | 节点预热的调度策略。 |

        | `points` | `integer \| null` | 必须为 `null` 或不传 | 必填 | 节点数量，必须大于等于 `1`。
        |

        | `services` | `ImagePreheatServiceDto[]` | 必填 | 必填 | 待预热的服务镜像列表，至少包含一项。
        |


        节点预热：resources[].mark 需通过资源列表接口 GET
        /api/deployment/resource/search?task_type=ImagePreHeat 获取，不能自行构造；同时必须传
        points。


        仅集群预热：regions 需通过区域列表接口 GET /api/task/image_preheat/get_regions 获取；无需传
        resources、scheduler_strategy 和 points。

        加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)
      tags:
        - 共绩算力 Open API/镜像预热任务
        - 共绩算力 Open API/任务
      parameters:
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
              type: object
              x-apifox-refs:
                01KTGHX3QHK6QHDFTNM9BFRQWD:
                  $ref: '#/components/schemas/ImagePreheatTaskDetailDto'
                  x-apifox-overrides:
                    task_id: null
                    task_type: null
                    scheduler_resources: null
                    status: null
                    used_points: null
                    available_points: null
                    scheduling_template: null
                    dependent_tasks: null
                    user_info: null
                    region_cache_info: null
                    services:
                      type: array
                      items:
                        type: object
                        x-apifox-refs:
                          01KTGJ3KFY4FFNPWAZZTS9WR4Y:
                            $ref: '#/components/schemas/ImagePreheatServiceDto'
                            x-apifox-overrides:
                              service_id: null
                        x-apifox-orders:
                          - 01KTGJ3KFY4FFNPWAZZTS9WR4Y
                        properties: {}
                  required:
                    - services
              x-apifox-orders:
                - 01KTGHX3QHK6QHDFTNM9BFRQWD
              properties: {}
            example:
              task_name: 镜像预热任务
              scheduler_strategy:
                mode: Unrestricted
              points: 2
              services:
                - service_name: d1779468791353-35628
                  service_image: harbor.sxxxe.cn/public-hub/dailyhot:1.0
                  repository_account: null
                  is_update_repository: null
              create_time: null
              resources:
                - mark: >-
                    J19Cg02JMM7pVim3XPCik/U6sbaBl/dYKodWFvzjPWWGJInsPwDdSxdy9/JlWA4GfzNWzeJB/tuGhCNTWLu4QY8g8FizMIgdNVGZh8Tp8XOEbxyOnOH7pHbI7WIUdbCUx1Wo8rderOCHwBwAq/QkIQAAU7hOXN4TgAK1tggieTos7TE9on7i2i
                - mark: >-
                    J19Cg02JMM7pVim3XPCik/U6vLaBl/dYKodWFvzjPWWGJInsPwDdSxdy9/JlWA4GfzNWzeJB/tuGiSNTWLu4QY8g8FizMIg3a51r+dNVGZh8Tp8XOEbxyOrKGLhZHlg4Esc7duvMDmQPgRm6aH4cHRIt1f3G6zhb1SUj+0tzZr/5UPLBduBg
        required: true
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: object
                    properties:
                      task_id:
                        type: integer
                        title: 任务id
                    x-apifox-orders:
                      - task_id
                    required:
                      - task_id
                    nullable: true
                required:
                  - data
                x-apifox-orders:
                  - 01KV0A6VPFPRP9AHZB9SW63151
                  - data
                x-apifox-refs:
                  01KV0A6VPFPRP9AHZB9SW63151:
                    $ref: '#/components/schemas/IResponse'
              example:
                code: '0000'
                message: success
                data:
                  task_id: 38116
          headers: {}
          x-apifox-name: 成功
          x-apifox-ordering: 0
      security: []
      x-apifox-folder: 共绩算力 Open API/镜像预热任务
      x-apifox-status: developing
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-469645046-run
components:
  schemas:
    ImagePreheatTaskDetailDto:
      type: object
      properties:
        task_id:
          type: integer
          title: 任务id
          nullable: true
        task_type:
          type: string
          enum:
            - ImagePreHeat
          x-apifox-enum:
            - value: ImagePreHeat
              name: 镜像预热
              description: ''
          title: 任务类型
          nullable: true
        task_name:
          type: string
          title: 任务名
        resources:
          type: array
          items:
            $ref: '#/components/schemas/ResourceMark'
          title: 资源列表
          nullable: true
        regions:
          type: array
          items:
            type: object
            properties:
              region:
                type: string
              region_name:
                type: string
                nullable: true
            x-apifox-orders:
              - region
              - region_name
            required:
              - region
            x-apifox-ignore-properties: []
          nullable: true
        scheduler_strategy:
          $ref: '#/components/schemas/TaskSchedulerStrategy'
          nullable: true
          title: 跨区调度
        scheduler_resources:
          type: array
          items:
            $ref: '#/components/schemas/ResourceMark'
          title: 跨区调度资源列表
          nullable: true
        status:
          type: string
          enum:
            - Pending
            - Running
            - Paused
            - End
          x-apifox-enum:
            - value: Pending
              name: 等待中
              description: ''
            - value: Running
              name: 运行中
              description: ''
            - value: Paused
              name: 已暂停
              description: ''
            - value: End
              name: 已停止
              description: ''
          title: 任务状态
          nullable: true
        points:
          type: integer
          title: 节点数量
          nullable: true
        used_points:
          type: integer
          title: 使用中节点数
          nullable: true
        available_points:
          type: integer
          title: 可用节点数
          nullable: true
        scheduling_template:
          $ref: '#/components/schemas/SchedulingTemplateDto'
          nullable: true
          title: 调度模板
        dependent_tasks:
          type: array
          items:
            $ref: '#/components/schemas/DependentTaskDto'
          title: 关联任务
          nullable: true
        create_time:
          type: string
          title: 创建时间
          nullable: true
        user_info:
          $ref: '#/components/schemas/UserInfoDto'
          nullable: true
          title: 用户信息
        region_cache_info:
          type: array
          items:
            $ref: '#/components/schemas/RegionCacheState'
          title: 集群预热信息
          nullable: true
        services:
          type: array
          items:
            $ref: '#/components/schemas/ImagePreheatServiceDto'
          title: 服务列表
        region_point_usage:
          type: object
          properties:
            北京酒仙桥t1(备注：该字段为预热节点所在集群的region_name):
              type: object
              properties:
                used_points:
                  type: integer
                  title: 已用节点数
                available_points:
                  type: integer
                  title: 可用节点数
              required:
                - used_points
                - available_points
              x-apifox-orders:
                - used_points
                - available_points
              x-apifox-ignore-properties: []
            北京酒仙桥t2(备注：该字段为预热节点所在集群的region_name):
              type: object
              properties:
                used_points:
                  type: integer
                  title: 已用节点数
                available_points:
                  type: integer
                  title: 可用节点数
              required:
                - used_points
                - available_points
              x-apifox-orders:
                - used_points
                - available_points
              x-apifox-ignore-properties: []
          x-apifox-orders:
            - 北京酒仙桥t1(备注：该字段为预热节点所在集群的region_name)
            - 北京酒仙桥t2(备注：该字段为预热节点所在集群的region_name)
          title: 集群使用节点数
          required:
            - 北京酒仙桥t1(备注：该字段为预热节点所在集群的region_name)
            - 北京酒仙桥t2(备注：该字段为预热节点所在集群的region_name)
          x-apifox-ignore-properties: []
          nullable: true
      x-apifox-orders:
        - task_id
        - task_type
        - task_name
        - resources
        - regions
        - scheduler_strategy
        - scheduler_resources
        - status
        - points
        - used_points
        - available_points
        - scheduling_template
        - dependent_tasks
        - create_time
        - user_info
        - region_cache_info
        - services
        - 01KY9X8302E2SH0MM99DEVCYWC
      required:
        - task_name
        - services
      x-apifox-refs:
        01KY9X8302E2SH0MM99DEVCYWC:
          $ref: '#/components/schemas/RegionPointUsage'
      x-apifox-ignore-properties:
        - region_point_usage
      x-apifox-folder: ''
    ImagePreheatServiceDto:
      type: object
      properties:
        service_id:
          type: string
          title: 服务id
          nullable: true
        service_name:
          type: string
          title: 服务名称
        service_image:
          type: string
          title: 服务镜像
        repository_account:
          $ref: '#/components/schemas/RepositoryAccountDto'
          nullable: true
          title: 私有仓库账号
        is_update_repository:
          type: boolean
          title: 是否更新私有仓库账号
          nullable: true
      x-apifox-orders:
        - service_id
        - service_name
        - service_image
        - repository_account
        - is_update_repository
      required:
        - service_name
        - service_image
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    ResourceMark:
      type: object
      properties:
        resource:
          $ref: '#/components/schemas/ResourceMarkDto'
          title: 资源信息
        region_name:
          type: string
          title: 区域名称
        mark:
          type: string
          title: 资源唯一标识
        weight:
          type: integer
          nullable: true
      x-apifox-orders:
        - resource
        - region_name
        - mark
        - weight
      x-apifox-refs: {}
      required:
        - mark
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    TaskSchedulerStrategy:
      type: object
      properties:
        mode:
          type: string
          enum:
            - Unrestricted
          x-apifox-enum:
            - value: Unrestricted
              name: ''
              description: ''
          x-apifox-mock: Unrestricted
      x-apifox-orders:
        - mode
      required:
        - mode
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    SchedulingTemplateDto:
      type: object
      properties:
        template:
          type: string
          title: 调度模板唯一标识
      x-apifox-orders:
        - template
      required:
        - template
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    DependentTaskDto:
      type: object
      properties:
        task_id:
          type: string
          title: 任务id
        task_type:
          type: string
          title: 任务类型
        task_name:
          type: string
          title: 任务名称
        points:
          type: string
          title: 期望节点数
        max_workers:
          type: string
          title: 最大节点数
          nullable: true
      x-apifox-orders:
        - task_id
        - task_type
        - task_name
        - points
        - max_workers
      required:
        - task_id
        - task_type
        - task_name
        - points
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    UserInfoDto:
      type: object
      properties:
        nickname:
          type: string
          title: 用户昵称
        tenant_nickname:
          type: string
          nullable: true
      x-apifox-orders:
        - nickname
        - tenant_nickname
      required:
        - nickname
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    RegionCacheState:
      type: object
      properties:
        region:
          type: string
          title: 区域
        status:
          type: string
          title: 状态
          enum:
            - Syncing
            - Completed
            - Begin
          x-apifox-enum:
            - value: Syncing
              name: 预热中
              description: ''
            - value: Completed
              name: 已预热
              description: ''
            - value: Begin
              name: 等待中
              description: ''
      x-apifox-orders:
        - region
        - status
      required:
        - region
        - status
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    RegionPointUsage:
      type: object
      properties:
        region_point_usage:
          type: object
          properties:
            北京酒仙桥t1(备注：该字段为预热节点所在集群的region_name):
              type: object
              properties:
                used_points:
                  type: integer
                  title: 已用节点数
                available_points:
                  type: integer
                  title: 可用节点数
              required:
                - used_points
                - available_points
              x-apifox-orders:
                - used_points
                - available_points
              x-apifox-ignore-properties: []
            北京酒仙桥t2(备注：该字段为预热节点所在集群的region_name):
              type: object
              properties:
                used_points:
                  type: integer
                  title: 已用节点数
                available_points:
                  type: integer
                  title: 可用节点数
              required:
                - used_points
                - available_points
              x-apifox-orders:
                - used_points
                - available_points
              x-apifox-ignore-properties: []
          x-apifox-orders:
            - 北京酒仙桥t1(备注：该字段为预热节点所在集群的region_name)
            - 北京酒仙桥t2(备注：该字段为预热节点所在集群的region_name)
          title: 集群使用节点数
          required:
            - 北京酒仙桥t1(备注：该字段为预热节点所在集群的region_name)
            - 北京酒仙桥t2(备注：该字段为预热节点所在集群的region_name)
          x-apifox-ignore-properties: []
          nullable: true
      x-apifox-orders:
        - region_point_usage
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    RepositoryAccountDto:
      type: object
      properties:
        repository_username:
          type: string
          title: 私有仓库用户名
        repository_password:
          type: string
          title: 私有仓库密码
          nullable: true
      x-apifox-orders:
        - repository_username
        - repository_password
      required:
        - repository_username
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    ResourceMarkDto:
      type: object
      properties:
        device_name:
          type: string
          title: 设备信息
        region:
          type: string
          title: 区域唯一标识
        gpu_name:
          type: string
          title: GPU名称
          nullable: true
        gpu_count:
          type: integer
          title: GPU卡数
        gpu_memory:
          type: integer
          title: GPU显存
          description: 单位为二进制兆字节(Mi)
        memory:
          type: integer
          title: 内存
          description: 单位为二进制兆字节(Mi)
        cpu_cores:
          type: integer
          title: CPU核数
          description: 单位为核(CPU)
      x-apifox-orders:
        - device_name
        - region
        - gpu_name
        - gpu_count
        - gpu_memory
        - memory
        - cpu_cores
      required:
        - device_name
        - region
        - gpu_count
        - gpu_memory
        - memory
        - cpu_cores
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
  responses: {}
  securitySchemes: {}
servers: []
security: []

```