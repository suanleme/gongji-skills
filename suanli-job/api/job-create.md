# Job任务创建接口

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/task/job/create:
    post:
      summary: Job任务创建接口
      deprecated: false
      description: >-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 否 | 是 |


        ### **描述**

        创建Job批处理任务。


        数据结构中的 `resources.item.mark(资源唯一标识)` 需要从
        [获取设备资源列表](https://s.apifox.cn/6aa360d3-d8f2-471e-b841-3a35c33a7b7c/api-296881020.md)
        接口获取
      tags:
        - 共绩算力 Open API/Job批处理任务
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
              x-apifox-refs: {}
              x-apifox-orders:
                - task_name
                - sub_type
                - resources
                - share_disk_volumes
                - share_mem_volumes
                - points
                - job_support
                - task_qos
                - services
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
                    type: object
                    properties:
                      resource:
                        title: 资源信息
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
                        x-apifox-refs: {}
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
                      region_name:
                        type: string
                        title: 区域名称
                      mark:
                        type: string
                        title: 资源唯一标识
                      weight:
                        type: integer
                        nullable: true
                    x-apifox-refs: {}
                    x-apifox-orders:
                      - resource
                      - region_name
                      - mark
                      - weight
                    required:
                      - mark
                    x-apifox-ignore-properties: []
                  title: 资源列表
                share_disk_volumes:
                  type: array
                  items:
                    type: object
                    properties:
                      name:
                        type: string
                        title: 卷名
                    x-apifox-refs: {}
                    x-apifox-orders:
                      - name
                    required:
                      - name
                    x-apifox-ignore-properties: []
                  title: 共享磁盘卷
                  description: 声明共享磁盘卷，需在services中配置对应的share_disk_config进行卷挂载。
                  nullable: true
                share_mem_volumes:
                  type: array
                  items:
                    type: object
                    properties:
                      name:
                        type: string
                        title: 卷名
                      size_limit:
                        type: integer
                        title: 共享内存大小
                        description: 单位为二进制兆字节(Mi)
                    x-apifox-refs: {}
                    x-apifox-orders:
                      - name
                      - size_limit
                    required:
                      - name
                      - size_limit
                    x-apifox-ignore-properties: []
                  title: 共享内存卷
                  description: 声明共享内存卷，需在services中配置对应的share_mem_config进行卷挂载。
                  nullable: true
                points:
                  type: integer
                  title: 完成节点数量
                  description: 任务需要成功完成的总次数。对应K8s参数：spec.completions
                  x-apifox-mock: '1'
                job_support:
                  title: Job支持
                  type: object
                  properties:
                    estimated_exec_sec:
                      type: integer
                      title: 单元运行时间(秒)
                      description: >-
                        任务运行完成的预估时间，系统将基于此时间寻找最稳定的资源窗口。该字段仅在 Job 批处理任务的 sub_type
                        为 Spot 时生效且必填；其他 sub_type
                        类型下不生效。该值应比任务真正运行完成时间略长，比任务超时时间略短。
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
                                      description: >-
                                        容器异常退出时，K8s 会在原 Pod
                                        内部自动重启容器进程，适用于需要尽力保证任务跑通的场景
                                    - value: Never
                                      name: 从不重启
                                      description: >-
                                        容器退出后 Pod
                                        直接被标记为失败，不进行原地重启，适用于需要保留第一案发现场日志供调试
                                  x-apifox-mock: OnFailure
                              x-apifox-refs: {}
                              x-apifox-orders:
                                - backoff_limit
                                - restart_policy
                              required:
                                - backoff_limit
                                - restart_policy
                              x-apifox-ignore-properties: []
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
                              x-apifox-refs: {}
                              x-apifox-orders:
                                - index_backoff_limit
                                - max_failed_index
                              required:
                                - index_backoff_limit
                              x-apifox-ignore-properties: []
                          x-apifox-orders:
                            - index
                          required:
                            - index
                          title: 索引模式
                          description: 系统将为每个并行节点分配固定的独立索引编号，并通过环境变量注入容器中。
                          x-apifox-ignore-properties: []
                      title: 完成模式参数
                      description: 对于多节点并行任务，建议使用索引模式
                  x-apifox-refs: {}
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
                task_qos:
                  title: CPU独占
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
                  x-apifox-refs: {}
                  x-apifox-orders:
                    - class
                  required:
                    - class
                  x-apifox-ignore-properties: []
                  nullable: true
                services:
                  type: array
                  items:
                    type: object
                    x-apifox-refs: {}
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
                    properties:
                      service_id:
                        type: integer
                        title: 服务id
                        nullable: true
                      service_name:
                        type: string
                        title: 服务名
                      service_image:
                        type: string
                        title: 服务镜像
                      resource_weight:
                        title: 资源权重
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
                            description: >-
                              GPU分配最小单位为卡数，为防止GPU分配有剩余，各容器GPU权重之和需大于0且整除所选资源GPU卡数的最大公约数
                        x-apifox-refs: {}
                        x-apifox-orders:
                          - cpu_weight
                          - mem_weight
                          - gpu_weight
                        required:
                          - cpu_weight
                          - mem_weight
                          - gpu_weight
                        x-apifox-ignore-properties: []
                      health_checks:
                        title: 健康检查
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
                        x-apifox-refs: {}
                        x-apifox-orders:
                          - liveness_probe
                          - startup_probe
                          - readiness_probe
                        required:
                          - liveness_probe
                          - startup_probe
                          - readiness_probe
                        x-apifox-ignore-properties: []
                        nullable: true
                      remote_ports:
                        type: array
                        items:
                          type: object
                          properties:
                            url:
                              type: string
                              title: 服务回传链接
                              nullable: true
                            service_port:
                              type: integer
                              title: 服务端口
                          x-apifox-refs: {}
                          x-apifox-orders:
                            - url
                            - service_port
                          required:
                            - service_port
                          x-apifox-ignore-properties: []
                        title: 服务七层暴露(服务回传)端口列表
                        nullable: true
                      storage_config:
                        type: array
                        items:
                          type: object
                          properties:
                            storage_id:
                              type: integer
                              title: 存储id
                            target_dir:
                              type: string
                              title: 挂载路径
                          x-apifox-refs: {}
                          x-apifox-orders:
                            - storage_id
                            - target_dir
                          required:
                            - storage_id
                            - target_dir
                          x-apifox-ignore-properties: []
                        title: 对象存储加速配置
                        nullable: true
                      share_storage_config:
                        type: array
                        items:
                          type: object
                          properties:
                            storage_id:
                              type: integer
                              title: 存储id
                            target_dir:
                              type: string
                              title: 挂载路径
                          x-apifox-refs: {}
                          x-apifox-orders:
                            - storage_id
                            - target_dir
                          required:
                            - storage_id
                            - target_dir
                          x-apifox-ignore-properties: []
                        title: 共享存储配置
                        nullable: true
                      nas_storage_config:
                        type: array
                        items:
                          type: object
                          properties:
                            storage_id:
                              type: integer
                              title: 存储id
                              description: 集群存储（NAS）卷 ID，来自 /storage/nas/v1/list 的 storage_id
                            target_dir:
                              type: string
                              title: 挂载路径
                          x-apifox-refs: {}
                          x-apifox-orders:
                            - storage_id
                            - target_dir
                          required:
                            - storage_id
                            - target_dir
                          x-apifox-ignore-properties: []
                        title: NAS存储配置
                        nullable: true
                      share_mem_config:
                        type: array
                        items:
                          type: object
                          properties:
                            target_dir:
                              type: string
                              title: 挂载路径
                            volume_name:
                              type: string
                              title: 卷名
                          x-apifox-refs: {}
                          x-apifox-orders:
                            - target_dir
                            - volume_name
                          required:
                            - target_dir
                            - volume_name
                          x-apifox-ignore-properties: []
                        title: 共享内存配置
                        description: 挂载共享内存卷，需在外层中声明对应的share_mem_volumes。
                        nullable: true
                      share_disk_config:
                        type: array
                        items:
                          type: object
                          properties:
                            target_dir:
                              type: string
                              title: 挂载路径
                            volume_name:
                              type: string
                              title: 卷名
                          x-apifox-refs: {}
                          x-apifox-orders:
                            - target_dir
                            - volume_name
                          required:
                            - target_dir
                            - volume_name
                          x-apifox-ignore-properties: []
                        title: 共享磁盘配置
                        description: 挂载共享磁盘卷，需在外层中声明对应的share_disk_volumes。
                        nullable: true
                      env:
                        type: array
                        items:
                          oneOf:
                            - type: object
                              properties:
                                name:
                                  type: string
                                value:
                                  type: string
                              x-apifox-orders:
                                - name
                                - value
                              required:
                                - name
                                - value
                              title: 键值对类型
                              x-apifox-ignore-properties: []
                            - type: object
                              properties:
                                name:
                                  type: string
                                value:
                                  type: 'null'
                                value_from:
                                  oneOf:
                                    - type: 'null'
                                    - type: object
                                      properties:
                                        field_ref:
                                          type: object
                                          properties:
                                            field_path:
                                              type: string
                                              title: 字段路径
                                              x-apifox-mock: metadata.name
                                          x-apifox-refs: {}
                                          x-apifox-orders:
                                            - field_path
                                          required:
                                            - field_path
                                          x-apifox-ignore-properties: []
                                      x-apifox-orders:
                                        - field_ref
                                      required:
                                        - field_ref
                                      title: 字段引用
                                      x-apifox-ignore-properties: []
                                    - type: object
                                      properties:
                                        resource_field_ref:
                                          type: object
                                          properties:
                                            service_name:
                                              type: string
                                              title: 服务名
                                            resource:
                                              type: string
                                              title: 资源字段
                                              x-apifox-mock: limits.cpu
                                          x-apifox-refs: {}
                                          x-apifox-orders:
                                            - service_name
                                            - resource
                                          required:
                                            - resource
                                          x-apifox-ignore-properties: []
                                      x-apifox-orders:
                                        - resource_field_ref
                                      required:
                                        - resource_field_ref
                                      title: 资源字段引用
                                      x-apifox-ignore-properties: []
                              x-apifox-orders:
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
                        title: 启动命令
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
                        x-apifox-refs: {}
                        x-apifox-orders:
                          - command
                          - args
                        required:
                          - command
                          - args
                        x-apifox-ignore-properties: []
                        nullable: true
                      repository_account:
                        title: 私有仓库账号
                        type: object
                        properties:
                          repository_username:
                            type: string
                            title: 私有仓库用户名
                          repository_password:
                            type: string
                            title: 私有仓库密码
                            nullable: true
                        x-apifox-refs: {}
                        x-apifox-orders:
                          - repository_username
                          - repository_password
                        required:
                          - repository_username
                        x-apifox-ignore-properties: []
                        nullable: true
                      is_update_repository:
                        type: string
                        title: 是否更新私有仓库账号
                        nullable: true
                    required:
                      - service_name
                      - service_image
                      - resource_weight
                    x-apifox-ignore-properties: []
                  title: 服务列表
              required:
                - task_name
                - resources
                - points
                - job_support
                - services
              x-apifox-ignore-properties: []
            example:
              task_name: job-202604210858
              sub_type: null
              schedule_status: null
              resources:
                - resource:
                    device_name: '4090'
                    region: chengde-p1
                    gpu_name: '4090'
                    gpu_count: 1
                    gpu_memory: 24560
                    memory: 64512
                    cpu_cores: 16
                  region_name: 河北六区
                  mark: >-
                    ha8GDGEAORN3a9Hhu7X+W/lveP9CW2eBkI+oB/QJLRcfvPTUMuUpxqfch7PdWik27Qx0BQX2cmaGoUHnIQ6pUPcLqpoLUCh5MaAR9kIet8llTG2oulHTzTRxAofshQoSFvtGpGD4Rh7V2V7xAj/0ysk+OmC4WeIxe+zHVBoYCehyTVGCyFygp1QeqGCp
                  weight: null
              status: Running
              points: 1
              services:
                - service_id: 1963001
                  service_name: container-01
                  service_image: harbor.suanleme.cn/trsnls6j/ubuntu:22.04
                  remote_ports:
                    - url: https://job-11391-olueehus-80.550w.link
                      service_port: 80
                  health_checks:
                    liveness_probe:
                      switch: false
                      probe_type: httpGet
                      path: /live
                      port: 80
                      initial_delay_seconds: 0
                      period_seconds: 10
                      timeout_seconds: 1
                      failure_threshold: 3
                    startup_probe:
                      switch: false
                      probe_type: httpGet
                      path: /health
                      port: 80
                      initial_delay_seconds: 0
                      period_seconds: 10
                      timeout_seconds: 1
                      failure_threshold: 3
                    readiness_probe:
                      switch: false
                      probe_type: httpGet
                      path: /ready
                      port: 80
                      initial_delay_seconds: 0
                      period_seconds: 10
                      timeout_seconds: 1
                      failure_threshold: 3
                  storage_config:
                    - storage_id: 2038
                      target_dir: /root/s3
                  share_storage_config:
                    - storage_id: 2037
                      target_dir: /root/share
                  nas_storage_config:
                    - storage_id: 1001
                      target_dir: /mnt/nas
                  share_mem_config:
                    - target_dir: /dev/shm
                      volume_name: mem-default
                  share_disk_config:
                    - target_dir: /dev/shd
                      volume_name: share-disk
                  env:
                    - name: key1
                      value: value1
                      value_from: null
                  start_script:
                    command:
                      - sleep
                    args:
                      - '300'
                  repository_account: null
                  is_update_repository: null
                  resource_weight:
                    cpu_weight: 1
                    mem_weight: 1
                    gpu_weight: 1
                  registered_ports: null
              task_tags: null
              share_disk_volumes:
                - name: share-disk
              share_mem_volumes:
                - name: mem-default
                  size_limit: 32768
              job_support:
                estimated_exec_sec: null
                timeout_sec: 1200
                parallelism: 1
                mod_param:
                  default:
                    backoff_limit: 3
                    restart_policy: OnFailure
                  index: null
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
                    type: object
                    properties:
                      task_id:
                        type: integer
                        title: 任务id
                    x-apifox-orders:
                      - task_id
                    required:
                      - task_id
                    x-apifox-ignore-properties: []
                    nullable: true
                required:
                  - code
                  - message
                  - data
                x-apifox-orders:
                  - 01KV0AC0MVVM6SVJK0Y8S1CFH4
                  - data
                x-apifox-refs:
                  01KV0AC0MVVM6SVJK0Y8S1CFH4:
                    $ref: '#/components/schemas/IResponse'
                x-apifox-ignore-properties:
                  - code
                  - message
              example:
                code: '0000'
                message: success
                data:
                  task_id: 6799
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 共绩算力 Open API/Job批处理任务
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-445572292-run
components:
  schemas:
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