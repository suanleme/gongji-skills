# Job任务队列任务组详情查询接口

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/job/queue/group/detail:
    get:
      summary: Job任务队列任务组详情查询接口
      deprecated: false
      description: >-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 否 | 是 |


        ### **描述**

        获取指定Job任务组详情。

        加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)
      tags:
        - 共绩算力 Open API/Job批处理任务队列
        - 共绩算力 Open API/任务
      parameters:
        - name: group_id
          in: query
          description: 组id
          required: true
          schema:
            type: integer
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
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
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
                  data:
                    anyOf:
                      - $ref: '#/components/schemas/GroupDto'
                      - type: 'null'
                required:
                  - code
                  - message
                  - data
                x-apifox-orders:
                  - 01KV0ASEZEB7GTT6WJER3Z86YY
                  - data
                x-apifox-refs:
                  01KV0ASEZEB7GTT6WJER3Z86YY:
                    $ref: '#/components/schemas/IResponse'
                x-apifox-ignore-properties:
                  - code
                  - message
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 共绩算力 Open API/Job批处理任务队列
      x-apifox-status: developing
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-481939016-run
components:
  schemas:
    GroupDto:
      type: object
      properties:
        queue_id:
          type: integer
          title: 队列id
        queue_name:
          type: string
          title: 队列名称
        group_id:
          type: integer
          title: 组id
        group_name:
          type: string
          title: 组名称
        group_count:
          type: integer
          title: 组内任务总数
          description: 该任务组将包含的子任务总数，定义该任务组内一共需要执行多少个子任务
        task_parallel_limit:
          type: integer
          title: 组内并发任务上限
          description: 允许同时运行的最大子任务数目，控制该任务组在执行阶段的任务并发上限
        status:
          type: string
          title: 组状态
          enum:
            - Running
            - Waiting
            - End
          x-apifox-enum:
            - value: Running
              name: 运行中
              description: ''
            - value: Waiting
              name: 等待中
              description: ''
            - value: End
              name: 已停止
              description: ''
        billing_value:
          type: integer
          title: 累计费用(积分)
        task_status_capacity:
          type: object
          properties:
            Pending:
              type: integer
              title: 等待中任务数量
            Running:
              type: integer
              title: 运行中任务数量
            Paused:
              type: integer
              title: 已暂停任务数量
            End:
              type: integer
              title: 已停止任务数量
          x-apifox-orders:
            - Pending
            - Running
            - Paused
            - End
          title: 任务状态队列
          x-apifox-ignore-properties: []
        create_time:
          type: string
          title: 创建时间
        task_dto:
          $ref: '#/components/schemas/TaskJobCreateDto'
          title: job任务资源
      x-apifox-orders:
        - queue_id
        - queue_name
        - group_id
        - group_name
        - group_count
        - task_parallel_limit
        - status
        - billing_value
        - task_status_capacity
        - create_time
        - task_dto
      required:
        - queue_id
        - queue_name
        - group_id
        - group_name
        - group_count
        - task_parallel_limit
        - status
        - billing_value
        - task_status_capacity
        - create_time
        - task_dto
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    TaskJobCreateDto:
      type: object
      properties:
        task_name:
          type: string
          title: 任务名
          x-apifox-mock: Job-test
        sub_type:
          type: string
          title: 子类型
          enum:
            - Spot
          x-apifox-enum:
            - value: Spot
              name: ''
              description: ''
          description: 传null或不传表示OnDemand任务，传Spot表示Spot任务。
          nullable: true
        resources:
          type: array
          items:
            $ref: '#/components/schemas/ResourceMark'
          title: 资源列表
        share_disk_volumes:
          type: array
          items:
            $ref: '#/components/schemas/EmptyDirDiskDto'
          title: 共享磁盘卷
          description: 声明共享磁盘卷，需在services中配置对应的share_disk_config进行卷挂载。
          nullable: true
        share_mem_volumes:
          type: array
          items:
            $ref: '#/components/schemas/EmptyDirMemoryDto'
          title: 共享内存卷
          description: 声明共享内存卷，需在services中配置对应的share_mem_config进行卷挂载。
          nullable: true
        task_qos:
          anyOf:
            - $ref: '#/components/schemas/TaskQosDto'
            - type: 'null'
          title: CPU独占
        points:
          type: integer
          title: 完成节点数量
          description: 任务需要成功完成的总次数。对应K8s参数：spec.completions
          x-apifox-mock: '1'
        task_tags:
          type: array
          items:
            type: string
          title: 任务标识
          description: 目前仅限标识是否为自带SSH的公有镜像
          nullable: true
        job_support:
          $ref: '#/components/schemas/JobSupport'
          title: Job支持
        termination_grace_period_seconds:
          type: integer
          title: 优雅退出时间
          nullable: true
        services:
          type: array
          items:
            type: object
            x-apifox-refs:
              01KPMG69RHP95M14B0MB2HEW93: &ref_2
                $ref: '#/components/schemas/ServiceDtoV2'
                x-apifox-overrides:
                  restart_policy: null
                required:
                  - health_checks
                  - restart_policy
            x-apifox-orders:
              - 01KPMG69RHP95M14B0MB2HEW93
            properties:
              service_id: &ref_3
                type: integer
                title: 服务id
                nullable: true
              service_name: &ref_4
                type: string
                title: 服务名
              service_image: &ref_5
                type: string
                title: 服务镜像
              resource_weight: &ref_6
                $ref: '#/components/schemas/ResourceWeightDto'
                title: 资源权重
              health_checks:
                anyOf:
                  - &ref_7
                    $ref: '#/components/schemas/HealthChecks'
                  - &ref_8
                    type: 'null'
                title: 健康检查
              remote_ports: &ref_9
                type: array
                items:
                  $ref: '#/components/schemas/RemotePort'
                title: 服务七层暴露(服务回传)端口列表
                nullable: true
              storage_config: &ref_10
                type: array
                items: &ref_0
                  $ref: '#/components/schemas/ServiceStorageDto'
                title: 对象存储加速配置
                nullable: true
              share_storage_config: &ref_11
                type: array
                items: *ref_0
                title: 共享存储配置
                nullable: true
              nas_storage_config: &ref_12
                type: array
                items: *ref_0
                title: NAS存储配置
                nullable: true
              share_mem_config: &ref_13
                type: array
                items: &ref_1
                  $ref: '#/components/schemas/ServiceVolumeMountDto'
                title: 共享内存配置
                description: 挂载共享内存卷，需在外层中声明对应的share_mem_volumes。
                nullable: true
              share_disk_config: &ref_14
                type: array
                items: *ref_1
                title: 共享磁盘配置
                description: 挂载共享磁盘卷，需在外层中声明对应的share_disk_volumes。
                nullable: true
              env:
                type: array
                items:
                  oneOf:
                    - type: object
                      properties:
                        name: &ref_15
                          type: string
                        value: &ref_16
                          type: string
                      x-apifox-orders: &ref_17
                        - name
                        - value
                      required:
                        - name
                        - value
                      title: 键值对类型
                      x-apifox-ignore-properties: []
                    - type: object
                      properties:
                        name: &ref_18
                          type: string
                        value: &ref_19
                          type: 'null'
                        value_from:
                          oneOf:
                            - &ref_20
                              type: 'null'
                            - type: object
                              properties:
                                field_ref: &ref_21
                                  $ref: '#/components/schemas/FieldRefDto'
                              x-apifox-orders: &ref_22
                                - field_ref
                              required:
                                - field_ref
                              title: 字段引用
                              x-apifox-ignore-properties: []
                            - type: object
                              properties:
                                resource_field_ref: &ref_23
                                  $ref: >-
                                    #/components/schemas/ServiceResourceFieldRefDto
                              x-apifox-orders: &ref_24
                                - resource_field_ref
                              required:
                                - resource_field_ref
                              title: 资源字段引用
                              x-apifox-ignore-properties: []
                      x-apifox-orders: &ref_25
                        - name
                        - value
                        - value_from
                      required:
                        - name
                        - value_from
                      title: 引用类型
                      x-apifox-ignore-properties: []
                title: 环境变量
                nullable: true
              start_script:
                anyOf:
                  - &ref_26
                    $ref: '#/components/schemas/StartScriptDtoV2'
                  - &ref_27
                    type: 'null'
                title: 启动命令
              repository_account:
                anyOf:
                  - &ref_28
                    $ref: '#/components/schemas/RepositoryAccountDto'
                  - &ref_29
                    type: 'null'
                title: 私有仓库账号
              is_update_repository: &ref_30
                type: string
                title: 是否更新私有仓库账号
                nullable: true
              registered_ports: &ref_31
                type: array
                items:
                  $ref: '#/components/schemas/ServicePortDto'
                title: 服务四层暴露(SSH)端口列表
                description: 目前仅限云主机
                nullable: true
            required:
              - service_name
              - service_image
              - resource_weight
            x-apifox-ignore-properties:
              - service_id
              - service_name
              - service_image
              - resource_weight
              - health_checks
              - remote_ports
              - storage_config
              - share_storage_config
              - nas_storage_config
              - share_mem_config
              - share_disk_config
              - env
              - start_script
              - repository_account
              - is_update_repository
              - registered_ports
          title: 服务列表
        init_services:
          type: array
          items: *ref_2
          nullable: true
      x-apifox-orders:
        - task_name
        - sub_type
        - resources
        - share_disk_volumes
        - share_mem_volumes
        - task_qos
        - points
        - task_tags
        - job_support
        - termination_grace_period_seconds
        - services
        - init_services
      required:
        - task_name
        - resources
        - points
        - job_support
        - services
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    ServicePortDto:
      type: object
      properties:
        service_port:
          type: integer
          title: 服务端口
      x-apifox-orders:
        - service_port
      required:
        - service_port
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
    StartScriptDtoV2:
      type: object
      properties:
        command:
          type: array
          items:
            type: string
          title: 命令
        args:
          type: array
          items:
            type: string
          title: 参数
      x-apifox-orders:
        - command
        - args
      required:
        - command
        - args
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    ServiceResourceFieldRefDto:
      type: object
      properties:
        service_name:
          type: string
          title: 服务名
        resource:
          type: string
          title: 资源字段
          x-apifox-mock: limits.cpu
      x-apifox-orders:
        - service_name
        - resource
      required:
        - resource
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    FieldRefDto:
      type: object
      properties:
        field_path:
          type: string
          title: 字段路径
          x-apifox-mock: metadata.name
      x-apifox-orders:
        - field_path
      required:
        - field_path
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    ServiceVolumeMountDto:
      type: object
      properties:
        target_dir:
          type: string
          title: 挂载路径
        volume_name:
          type: string
          title: 卷名
      x-apifox-orders:
        - target_dir
        - volume_name
      required:
        - target_dir
        - volume_name
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    ServiceStorageDto:
      type: object
      properties:
        storage_id:
          type: integer
          title: 存储id
        target_dir:
          type: string
          title: 挂载路径
      x-apifox-orders:
        - storage_id
        - target_dir
      required:
        - storage_id
        - target_dir
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    RemotePort:
      type: object
      properties:
        url:
          type: string
          title: 服务回传链接
          nullable: true
        service_port:
          type: integer
          title: 服务端口
      x-apifox-orders:
        - url
        - service_port
      required:
        - service_port
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    HealthChecks:
      type: object
      properties:
        liveness_probe:
          type: object
          properties:
            switch:
              type: boolean
              x-apifox-mock: 'false'
              title: 开关
            probe_type:
              type: string
              x-apifox-mock: httpGet
              enum:
                - httpGet
                - tcpSocket
              x-apifox-enum:
                - value: httpGet
                  name: ''
                  description: ''
                - value: tcpSocket
                  name: ''
                  description: ''
              title: 检查类型
            path:
              type: string
              x-apifox-mock: /live
              title: 路径
            port:
              type: integer
              x-apifox-mock: '80'
              title: 服务端口
            initial_delay_seconds:
              type: integer
              x-apifox-mock: '0'
              title: 初始延迟
              description: 单位为秒
            period_seconds:
              type: integer
              x-apifox-mock: '10'
              title: 检查周期
              description: 单位为秒
            timeout_seconds:
              type: integer
              x-apifox-mock: '1'
              title: 超时时间
              description: 单位为秒
            failure_threshold:
              type: integer
              x-apifox-mock: '3'
              title: 失败阈值
          x-apifox-refs: {}
          x-apifox-orders:
            - switch
            - probe_type
            - path
            - port
            - initial_delay_seconds
            - period_seconds
            - timeout_seconds
            - failure_threshold
          required:
            - switch
            - probe_type
            - port
            - initial_delay_seconds
            - period_seconds
            - timeout_seconds
            - failure_threshold
          title: 存活探针
          x-apifox-ignore-properties: []
        startup_probe:
          type: object
          properties:
            switch:
              type: boolean
              x-apifox-mock: 'false'
              title: 开关
            probe_type:
              type: string
              x-apifox-mock: httpGet
              enum:
                - httpGet
                - tcpSocket
              x-apifox-enum:
                - value: httpGet
                  name: ''
                  description: ''
                - value: tcpSocket
                  name: ''
                  description: ''
              title: 检查类型
            path:
              type: string
              x-apifox-mock: /health
              title: 路径
            port:
              type: integer
              x-apifox-mock: '80'
              title: 服务端口
            initial_delay_seconds:
              type: integer
              x-apifox-mock: '0'
              title: 初始延迟
              description: 单位为秒
            period_seconds:
              type: integer
              x-apifox-mock: '10'
              title: 检查周期
              description: 单位为秒
            timeout_seconds:
              type: integer
              x-apifox-mock: '1'
              title: 超时时间
              description: 单位为秒
            failure_threshold:
              type: integer
              x-apifox-mock: '3'
              title: 失败阈值
          x-apifox-refs: {}
          x-apifox-orders:
            - switch
            - probe_type
            - path
            - port
            - initial_delay_seconds
            - period_seconds
            - timeout_seconds
            - failure_threshold
          required:
            - switch
            - probe_type
            - port
            - initial_delay_seconds
            - period_seconds
            - timeout_seconds
            - failure_threshold
          title: 启动探针
          x-apifox-ignore-properties: []
        readiness_probe:
          type: object
          properties:
            switch:
              type: boolean
              x-apifox-mock: 'false'
              title: 开关
            probe_type:
              type: string
              x-apifox-mock: httpGet
              enum:
                - httpGet
                - tcpSocket
              x-apifox-enum:
                - value: httpGet
                  name: ''
                  description: ''
                - value: tcpSocket
                  name: ''
                  description: ''
              title: 检查类型
            path:
              type: string
              x-apifox-mock: /ready
              title: 路径
            port:
              type: integer
              x-apifox-mock: '80'
              title: 服务端口
            initial_delay_seconds:
              type: integer
              x-apifox-mock: '0'
              title: 初始延迟
              description: 单位为秒
            period_seconds:
              type: integer
              x-apifox-mock: '10'
              title: 检查周期
              description: 单位为秒
            timeout_seconds:
              type: integer
              x-apifox-mock: '1'
              title: 超时时间
              description: 单位为秒
            failure_threshold:
              type: integer
              x-apifox-mock: '3'
              title: 失败阈值
          x-apifox-refs: {}
          x-apifox-orders:
            - switch
            - probe_type
            - path
            - port
            - initial_delay_seconds
            - period_seconds
            - timeout_seconds
            - failure_threshold
          required:
            - switch
            - probe_type
            - port
            - initial_delay_seconds
            - period_seconds
            - timeout_seconds
            - failure_threshold
          title: 就绪探针
          x-apifox-ignore-properties: []
      x-apifox-orders:
        - liveness_probe
        - startup_probe
        - readiness_probe
      required:
        - liveness_probe
        - startup_probe
        - readiness_probe
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    ResourceWeightDto:
      type: object
      properties:
        cpu_weight:
          type: integer
          x-apifox-mock: '1'
          title: CPU权重
          description: CPU分配最小单位为豪核(m)，CPU权重需大于0
        mem_weight:
          type: integer
          x-apifox-mock: '1'
          title: 内存权重
          description: 内存分配最小单位为二进制兆字节(Mi)，内存权重需大于0
        gpu_weight:
          type: integer
          x-apifox-mock: '1'
          title: GPU权重
          description: GPU分配最小单位为卡数，为防止GPU分配有剩余，各容器GPU权重之和需大于0且整除所选资源GPU卡数的最大公约数
      x-apifox-orders:
        - cpu_weight
        - mem_weight
        - gpu_weight
      required:
        - cpu_weight
        - mem_weight
        - gpu_weight
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    ServiceDtoV2:
      type: object
      properties:
        service_id: *ref_3
        service_name: *ref_4
        service_image: *ref_5
        resource_weight: *ref_6
        health_checks:
          anyOf:
            - *ref_7
            - *ref_8
          title: 健康检查
        remote_ports: *ref_9
        storage_config: *ref_10
        share_storage_config: *ref_11
        nas_storage_config: *ref_12
        share_mem_config: *ref_13
        share_disk_config: *ref_14
        env:
          type: array
          items:
            oneOf:
              - type: object
                properties:
                  name: *ref_15
                  value: *ref_16
                x-apifox-orders: *ref_17
                required:
                  - name
                  - value
                title: 键值对类型
                x-apifox-ignore-properties: []
              - type: object
                properties:
                  name: *ref_18
                  value: *ref_19
                  value_from:
                    oneOf:
                      - *ref_20
                      - type: object
                        properties:
                          field_ref: *ref_21
                        x-apifox-orders: *ref_22
                        required:
                          - field_ref
                        title: 字段引用
                        x-apifox-ignore-properties: []
                      - type: object
                        properties:
                          resource_field_ref: *ref_23
                        x-apifox-orders: *ref_24
                        required:
                          - resource_field_ref
                        title: 资源字段引用
                        x-apifox-ignore-properties: []
                x-apifox-orders: *ref_25
                required:
                  - name
                  - value_from
                title: 引用类型
                x-apifox-ignore-properties: []
          title: 环境变量
          nullable: true
        start_script:
          anyOf:
            - *ref_26
            - *ref_27
          title: 启动命令
        repository_account:
          anyOf:
            - *ref_28
            - *ref_29
          title: 私有仓库账号
        is_update_repository: *ref_30
        registered_ports: *ref_31
        restart_policy:
          type: string
          title: 重启策略
          enum:
            - Always
          x-apifox-enum:
            - value: Always
              name: ''
              description: ''
          nullable: true
      x-apifox-orders:
        - service_id
        - service_name
        - service_image
        - resource_weight
        - health_checks
        - remote_ports
        - storage_config
        - share_storage_config
        - nas_storage_config
        - share_mem_config
        - share_disk_config
        - env
        - start_script
        - repository_account
        - is_update_repository
        - registered_ports
        - restart_policy
      required:
        - service_name
        - service_image
        - resource_weight
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    JobSupport:
      type: object
      properties:
        estimated_exec_sec:
          type: integer
          title: 单元运行时间(秒)
          description: >-
            任务运行完成的预估时间，系统将基于此时间寻找最稳定的资源窗口。该字段仅在 Job 批处理任务的 sub_type 为 Spot
            时生效且必填；其他 sub_type 类型下不生效。该值应比任务真正运行完成时间略长，比任务超时时间略短。
          maximum: 86400
          minimum: 1
          x-apifox-mock: '3600'
          nullable: true
        timeout_sec:
          type: integer
          title: 任务超时时间(秒)
          description: 任务从开始运行到结束的最长物理时间，超时系统将强制终止任务。
          x-apifox-mock: '86400'
        parallelism:
          type: integer
          title: 并行节点数
          x-apifox-mock: '1'
        mod_param:
          oneOf:
            - type: object
              properties:
                default:
                  $ref: '#/components/schemas/DefaultModeParam'
              x-apifox-orders:
                - default
              required:
                - default
              title: 默认模式
              description: 非索引模式
              x-apifox-ignore-properties: []
            - type: object
              properties:
                index:
                  $ref: '#/components/schemas/IndexModeParam'
              x-apifox-orders:
                - index
              required:
                - index
              title: 索引模式
              description: 系统将为每个并行节点分配固定的独立索引编号，并通过环境变量注入容器中。
              x-apifox-ignore-properties: []
          title: 完成模式参数
          description: 对于多节点并行任务，建议使用索引模式
      x-apifox-orders:
        - estimated_exec_sec
        - timeout_sec
        - parallelism
        - mod_param
      required:
        - timeout_sec
        - parallelism
        - mod_param
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    IndexModeParam:
      type: object
      properties:
        index_backoff_limit:
          type: integer
          title: 单索引重试次数
          description: 定义每个独立索引节点各自允许失败重试的最大次数
          x-apifox-mock: '3'
        max_failed_index:
          type: integer
          title: 最大允许失败节点数
          description: 当失败的节点数量达到此设定值时，系统将直接终止整个任务下所有的运行节点
          nullable: true
      x-apifox-orders:
        - index_backoff_limit
        - max_failed_index
      required:
        - index_backoff_limit
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    DefaultModeParam:
      type: object
      properties:
        backoff_limit:
          type: integer
          title: 任务重试次数
          description: 定义整个任务在彻底宣告失败前，系统自动重新调度创建新 Pod 的累计最大次数
          x-apifox-mock: '3'
        restart_policy:
          type: string
          title: 重启策略
          description: 定义当任务容器由于内部错误或异常退出（非 0 状态码）时，系统的重启行为
          enum:
            - OnFailure
            - Never
          x-apifox-enum:
            - value: OnFailure
              name: ' 失败时重启'
              description: 容器异常退出时，K8s 会在原 Pod 内部自动重启容器进程，适用于需要尽力保证任务跑通的场景
            - value: Never
              name: 从不重启
              description: 容器退出后 Pod 直接被标记为失败，不进行原地重启，适用于需要保留第一案发现场日志供调试
          x-apifox-mock: OnFailure
      x-apifox-orders:
        - backoff_limit
        - restart_policy
      required:
        - backoff_limit
        - restart_policy
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    TaskQosDto:
      type: object
      properties:
        class:
          type: string
          enum:
            - Guaranteed
          x-apifox-enum:
            - value: Guaranteed
              name: ''
              description: ''
          x-apifox-mock: Guaranteed
      x-apifox-orders:
        - class
      required:
        - class
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    EmptyDirMemoryDto:
      type: object
      properties:
        name:
          type: string
          title: 卷名
        size_limit:
          type: integer
          title: 共享内存大小
          description: 单位为二进制兆字节(Mi)
      x-apifox-orders:
        - name
        - size_limit
      required:
        - name
        - size_limit
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    EmptyDirDiskDto:
      type: object
      properties:
        name:
          type: string
          title: 卷名
      x-apifox-orders:
        - name
      required:
        - name
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
