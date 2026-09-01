# 新版任务详情查询接口

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/task/deployment/detail:
    get:
      summary: 新版任务详情查询接口
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        获取弹性部署任务详情。
      tags:
        - 共绩算力 Open API/弹性部署服务任务
      parameters:
        - name: task_id
          in: query
          description: 任务id
          required: true
          example: 1
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
          description: ''
          content:
            application/json:
              schema:
                type: object
                x-apifox-refs:
                  01KEDP6HH3E811E750HBT9DQMW:
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
                    anyOf:
                      - $ref: '#/components/schemas/IDeployTask'
                      - type: 'null'
                required:
                  - code
                  - message
                  - data
                x-apifox-orders:
                  - 01KEDP6HH3E811E750HBT9DQMW
                  - data
                x-apifox-ignore-properties:
                  - code
                  - message
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 共绩算力 Open API/弹性部署服务任务
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-402249411-run
components:
  schemas:
    IDeployTask:
      type: object
      properties:
        task_id:
          type: number
          title: 任务id
          nullable: true
        task_type:
          type: string
          title: 任务类型
          const: Deployment
          nullable: true
        task_name:
          type: string
          title: 任务名称
        namespace:
          type: string
          title: 命名空间
          nullable: true
        repository_username:
          type: string
          title: 私有仓库用户名
          description: |-
            为仅写字段（write-only），仅在提交请求时生效，查询接口不返回。
            暂不支持创建后更新。
          nullable: true
        repository_password:
          type: string
          title: 私有仓库密码
          description: |-
            为仅写字段（write-only），仅在提交请求时生效，查询接口不返回。
            暂不支持创建后更新。
          nullable: true
        status:
          type: string
          title: 任务状态
          enum:
            - Pending
            - Running
            - Paused
            - End
            - Other
          x-apifox-enum:
            - value: Pending
              name: ''
              description: 等待中
            - value: Running
              name: ''
              description: 运行中
            - value: Paused
              name: ''
              description: 已停止
            - value: End
              name: ''
              description: 已删除
            - value: Other
              name: ''
              description: 其它
          nullable: true
        points:
          type: number
          title: 节点数量
          nullable: true
        runing_points:
          type: number
          title: 运行中节点数
          nullable: true
        billing_points:
          type: number
          title: 计费中节点数
          nullable: true
        billing_value:
          type: number
          title: 累计花费金额
          nullable: true
        forecast_value:
          type: number
          title: 实时花费金额
          nullable: true
        scheduler_strategy:
          type: object
          properties:
            mode:
              type: string
              const: Unrestricted
          x-apifox-orders:
            - mode
          title: 跨区调度
          required:
            - mode
          x-apifox-ignore-properties: []
          nullable: true
        task_qos:
          type: object
          properties:
            class:
              type: string
              const: Guaranteed
          x-apifox-orders:
            - class
          title: CPU独占
          required:
            - class
          x-apifox-ignore-properties: []
          nullable: true
        load_balance:
          type: object
          properties:
            type:
              type: string
              title: 负载均衡策略
              enum:
                - LeastConnection
                - RoundRobin
                - Random
                - IpHash
                - HeaderHash
                - CookieHash
              x-apifox-enum:
                - value: LeastConnection
                  name: ''
                  description: 最少连接（加权）
                - value: RoundRobin
                  name: ''
                  description: 轮询
                - value: Random
                  name: ''
                  description: 随机
                - value: IpHash
                  name: ''
                  description: IP 哈希
                - value: HeaderHash
                  name: ''
                  description: HTTP Header 哈希
                - value: CookieHash
                  name: ''
                  description: Cookie 哈希
            params:
              type: object
              properties:
                header:
                  type: string
                  title: HTTP Header 名称
                  description: 仅当 type 为 HeaderHash
                  nullable: true
                cookie:
                  type: string
                  title: Cookie 名称
                  description: 仅当 type 为 CookieHash
                  nullable: true
              x-apifox-orders:
                - header
                - cookie
              required:
                - header
                - cookie
              title: 负载均衡策略参数
              x-apifox-ignore-properties: []
              nullable: true
          x-apifox-orders:
            - type
            - params
          title: 负载均衡
          required:
            - type
            - params
          x-apifox-ignore-properties: []
          nullable: true
        dynamic_pod_strategy:
          type: object
          properties:
            min_workers:
              type: number
              title: 最小节点数
            max_workers:
              type: number
              title: 最大节点数
            idle_timeout:
              type: number
              title: 空闲超时时间
            execution_timeout:
              type: number
              title: 执行超时时间
            switch:
              type: boolean
              title: 开关
            benchmark:
              type: array
              items:
                anyOf:
                  - type: object
                    properties:
                      scaling_strategy:
                        type: string
                        title: 扩缩容子策略
                        const: queue_delay
                      indicators:
                        type: object
                        properties:
                          port:
                            type: number
                            title: 端口
                          queue_delay_threshold:
                            type: number
                            title: 队列延迟阈值
                            description: 单位 秒
                          max_concurrency_per_instance:
                            type: number
                            title: 单节点最大并发
                        x-apifox-orders:
                          - port
                          - queue_delay_threshold
                          - max_concurrency_per_instance
                        required:
                          - port
                          - queue_delay_threshold
                          - max_concurrency_per_instance
                        title: 指标
                        x-apifox-ignore-properties: []
                    x-apifox-orders:
                      - scaling_strategy
                      - indicators
                    required:
                      - scaling_strategy
                      - indicators
                    title: 延迟策略
                    x-apifox-ignore-properties: []
                  - type: object
                    properties:
                      scaling_strategy:
                        type: string
                        title: 扩缩容子策略
                        const: queue_length
                      indicators:
                        type: object
                        properties:
                          port:
                            type: number
                            title: 端口
                          request_count_threshold:
                            type: number
                            title: 请求计数阈值
                          max_concurrency_per_instance:
                            type: number
                            title: 单节点最大并发
                        x-apifox-orders:
                          - port
                          - request_count_threshold
                          - max_concurrency_per_instance
                        required:
                          - port
                          - request_count_threshold
                          - max_concurrency_per_instance
                        title: 指标
                        x-apifox-ignore-properties: []
                    x-apifox-orders:
                      - scaling_strategy
                      - indicators
                    required:
                      - scaling_strategy
                      - indicators
                    title: 计数策略
                    x-apifox-ignore-properties: []
                title: 策略配置
              title: 策略配置
          x-apifox-orders:
            - min_workers
            - max_workers
            - idle_timeout
            - execution_timeout
            - switch
            - benchmark
          required:
            - min_workers
            - max_workers
            - idle_timeout
            - execution_timeout
            - switch
            - benchmark
          title: 弹性扩缩容
          x-apifox-ignore-properties: []
          nullable: true
        resources:
          type: array
          items:
            properties:
              resource:
                type: object
                properties:
                  device_name:
                    type: string
                    title: 设备名称
                  region:
                    type: string
                    title: 区域唯一标识
                  gpu_name:
                    type: string
                    title: GPU名称
                  gpu_count:
                    type: integer
                    title: GPU数量
                  gpu_memory:
                    type: integer
                    title: GPU显存
                  memory:
                    type: integer
                    title: 内存
                  cpu_cores:
                    type: integer
                    title: CPU核数
                required:
                  - device_name
                  - region
                  - gpu_name
                  - gpu_count
                  - gpu_memory
                  - memory
                  - cpu_cores
                x-apifox-orders:
                  - device_name
                  - region
                  - gpu_name
                  - gpu_count
                  - gpu_memory
                  - memory
                  - cpu_cores
                title: 资源信息
              region_name:
                type: string
                title: 地区名称
              mark:
                type: string
                title: 资源唯一标识
            required:
              - resource
              - region_name
              - mark
            x-apifox-orders:
              - resource
              - region_name
              - mark
            $ref: '#/components/schemas/IDeployResource'
          title: 资源列表
        services:
          type: array
          items:
            $ref: '#/components/schemas/IDeployService'
      x-apifox-refs: {}
      x-apifox-orders:
        - task_id
        - task_type
        - task_name
        - namespace
        - repository_username
        - repository_password
        - status
        - points
        - runing_points
        - billing_points
        - billing_value
        - forecast_value
        - scheduler_strategy
        - task_qos
        - load_balance
        - dynamic_pod_strategy
        - resources
        - services
      required:
        - task_id
        - task_type
        - task_name
        - namespace
        - repository_username
        - repository_password
        - status
        - points
        - runing_points
        - billing_points
        - billing_value
        - forecast_value
        - scheduler_strategy
        - task_qos
        - load_balance
        - dynamic_pod_strategy
        - resources
        - services
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    IDeployService:
      type: object
      properties:
        service_id:
          type: number
          title: 服务id
          nullable: true
        service_name:
          type: string
          title: 服务名称
        service_image:
          type: string
          title: 服务镜像
        env:
          type: string
          title: 环境变量
          nullable: true
        shared_mem_size:
          type: number
          title: 共享内存
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
            x-apifox-orders:
              - storage_id
              - target_dir
            required:
              - storage_id
              - target_dir
            x-apifox-ignore-properties: []
          title: s3存储配置
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
            x-apifox-orders:
              - storage_id
              - target_dir
            required:
              - storage_id
              - target_dir
            x-apifox-ignore-properties: []
          title: NAS存储配置
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
                title: 服务端口暴露
            x-apifox-orders:
              - url
              - service_port
            required:
              - url
              - service_port
            x-apifox-ignore-properties: []
          title: 服务端口暴露列表
        health_checks:
          type: object
          properties:
            liveness_probe: &ref_0
              properties:
                switch:
                  type: boolean
                probe_type:
                  type: string
                path:
                  type: string
                port:
                  type: integer
                initial_delay_seconds:
                  type: integer
                period_seconds:
                  type: integer
                timeout_seconds:
                  type: integer
                failure_threshold:
                  type: integer
              required:
                - switch
                - probe_type
                - path
                - port
                - initial_delay_seconds
                - period_seconds
                - timeout_seconds
                - failure_threshold
              x-apifox-orders:
                - switch
                - probe_type
                - path
                - port
                - initial_delay_seconds
                - period_seconds
                - timeout_seconds
                - failure_threshold
              $ref: '#/components/schemas/IHealthCheck'
              title: 存活探针
            startup_probe: *ref_0
            readiness_probe: *ref_0
          x-apifox-orders:
            - liveness_probe
            - startup_probe
            - readiness_probe
          required:
            - liveness_probe
            - startup_probe
            - readiness_probe
          title: 健康检查
          x-apifox-ignore-properties: []
          nullable: true
        start_script_v2:
          type: object
          properties:
            command:
              type: string
              title: 命令
              nullable: true
            args:
              type: array
              items:
                type: string
              title: 参数列表
          x-apifox-orders:
            - command
            - args
          required:
            - command
            - args
          title: 启动命令
          x-apifox-ignore-properties: []
          nullable: true
      x-apifox-orders:
        - service_id
        - service_name
        - service_image
        - env
        - shared_mem_size
        - storage_config
        - share_storage_config
        - nas_storage_config
        - remote_ports
        - health_checks
        - start_script_v2
      required:
        - service_id
        - service_name
        - service_image
        - env
        - shared_mem_size
        - storage_config
        - share_storage_config
        - remote_ports
        - health_checks
        - start_script_v2
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    IHealthCheck:
      type: object
      properties:
        switch:
          type: boolean
          title: 开关
          x-apifox-mock: 'false'
        probe_type:
          type: string
          title: 检查类型
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
          x-apifox-mock: httpGet
        path:
          type: string
          title: 路径
          x-apifox-mock: /live
        port:
          type: integer
          title: 端口
          x-apifox-mock: '80'
        initial_delay_seconds:
          type: integer
          title: 初始延迟 (秒)
          x-apifox-mock: '0'
        period_seconds:
          type: integer
          title: 检查周期 (秒)
          x-apifox-mock: '10'
        timeout_seconds:
          type: integer
          title: 超时时间 (秒)
          x-apifox-mock: '1'
        failure_threshold:
          type: integer
          title: 失败阈值
          x-apifox-mock: '3'
      required:
        - switch
        - probe_type
        - path
        - port
        - initial_delay_seconds
        - period_seconds
        - timeout_seconds
        - failure_threshold
      x-apifox-orders:
        - switch
        - probe_type
        - path
        - port
        - initial_delay_seconds
        - period_seconds
        - timeout_seconds
        - failure_threshold
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    IDeployResource:
      type: object
      properties:
        resource:
          type: object
          properties:
            device_name:
              type: string
              title: 设备名称
            region:
              type: string
              title: 区域唯一标识
            gpu_name:
              type: string
              title: GPU名称
              nullable: true
            gpu_count:
              type: integer
              title: GPU数量
            gpu_memory:
              type: integer
              title: GPU显存
            memory:
              type: integer
              title: 内存
            cpu_cores:
              type: integer
              title: CPU核数
          x-apifox-orders:
            - device_name
            - region
            - gpu_name
            - gpu_count
            - gpu_memory
            - memory
            - cpu_cores
          title: 资源信息
          required:
            - device_name
            - region
            - gpu_name
            - gpu_count
            - gpu_memory
            - memory
            - cpu_cores
          x-apifox-ignore-properties: []
          nullable: true
        region_name:
          type: string
          title: 地区名称
          nullable: true
        mark:
          type: string
          title: 资源唯一标识
      required:
        - resource
        - region_name
        - mark
      x-apifox-orders:
        - resource
        - region_name
        - mark
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