# 节点列表查询接口

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/deployment/task/points:
    get:
      summary: 节点列表查询接口
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        查询任务节点列表信息。
      tags:
        - 共绩算力 Open API/弹性部署服务节点
        - 共绩算力 Open API/节点
      parameters:
        - name: task_id
          in: query
          description: 任务id
          required: true
          example: 1
          schema:
            type: number
        - name: status
          in: query
          description: 节点状态。如果有多个值，请使用英文逗号（,）分隔
          required: false
          example: Running,Pendi,End,Failed
          schema:
            type: string
            enum:
              - Running
              - Pending
              - Succeeded
              - Failed
              - End
              - Unknown
            x-apifox-enum:
              - value: Running
                name: 运行中
                description: ''
              - value: Pending
                name: 等待中
                description: ''
              - value: Succeeded
                name: 成功
                description: ''
              - value: Failed
                name: 失败
                description: 异常
              - value: End
                name: 结束
                description: ''
              - value: Unknown
                name: 未知
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
          description: 每页数量
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
                  01KFAGEADQS1M8ERBRNMX48VWR:
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
                          $ref: '#/components/schemas/IDeployPoint'
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
                  - 01KFAGEADQS1M8ERBRNMX48VWR
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
                    - point_id: 1
                      name: deployment-5-8vxr7frs-5f876c5fc-8gz8b
                      status: Running
                      region: guangdong-t-01
                      region_name: 广东-T1
                      resource:
                        gpu_name: '4090'
                        gpu_count: 1
                        cpu_cores: 16
                      containers:
                        - service_name: null
                          name: d1768790900909-38167100-container
                          image: idc.suanleme.cn/public-hub/test:latest
                          gpu_limit: 1
                          reason: null
                          message: null
                          exit_code: null
                      runing_time: 14593
                      billing_value: 6710400
                      port_mappings: null
                      describe_dto:
                        restart_count: 2
                        last_restart_time: null
          headers: {}
      security: []
      x-apifox-folder: 共绩算力 Open API/弹性部署服务节点
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-296885186-run
components:
  schemas:
    IDeployPoint:
      type: object
      properties:
        point_id:
          type: number
          description: 节点id
        name:
          type: string
          description: 节点名称
        status:
          type: string
          description: 节点状态
          enum:
            - Pending
            - Running
            - Succeeded
            - Failed
            - End
            - Unknown
          x-apifox-enum:
            - value: Pending
              name: 等待中
              description: ''
            - value: Running
              name: 运行中
              description: ''
            - value: Succeeded
              name: 成功
              description: ''
            - value: Failed
              name: 失败
              description: ''
            - value: End
              name: 结束
              description: ''
            - value: Unknown
              name: 未知
              description: ''
        region:
          type: string
          description: 区域tag
        region_name:
          type: string
          description: 区域名称
        resource:
          type: object
          properties:
            gpu_name:
              type: string
              description: gpu名称
              nullable: true
            gpu_count:
              type: string
              description: gpu卡数
            cpu_cores:
              type: string
              description: cpu核数
          x-apifox-orders:
            - gpu_name
            - gpu_count
            - cpu_cores
          required:
            - gpu_name
            - gpu_count
            - cpu_cores
          description: 资源
          x-apifox-ignore-properties: []
        containers:
          type: array
          items:
            type: object
            properties:
              service_name:
                type: string
                nullable: true
              name:
                type: string
              image:
                type: string
              gpu_limit:
                type: number
              reason:
                type: string
                description: 重启原因
                nullable: true
              message:
                type: string
                description: 重启信息
                nullable: true
              exit_code:
                type: string
                description: 退出码
            x-apifox-orders:
              - service_name
              - name
              - image
              - gpu_limit
              - reason
              - message
              - exit_code
            required:
              - service_name
              - name
              - image
              - gpu_limit
              - reason
              - message
              - exit_code
            x-apifox-ignore-properties: []
          description: 容器列表
        runing_time:
          type: number
          description: 运行时间
        billing_value:
          type: number
          description: 费用
        describe_dto:
          type: object
          properties:
            last_restart_time:
              type: string
              description: 上次重启时间（RFC3339格式）
              nullable: true
            restart_count:
              type: number
              description: 重启次数
          x-apifox-orders:
            - last_restart_time
            - restart_count
          required:
            - last_restart_time
            - restart_count
          x-apifox-ignore-properties: []
      x-apifox-orders:
        - point_id
        - name
        - status
        - region
        - region_name
        - resource
        - containers
        - runing_time
        - billing_value
        - describe_dto
      required:
        - point_id
        - name
        - status
        - region
        - region_name
        - resource
        - containers
        - runing_time
        - billing_value
        - describe_dto
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