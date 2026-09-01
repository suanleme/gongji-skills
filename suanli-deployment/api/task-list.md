# 任务列表查询接口

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/deployment/task/search:
    get:
      summary: 任务列表查询接口
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        获取弹性部署任务列表及其相关信息。
        支持按状态、任务名等条件查询。
      tags:
        - 共绩算力 Open API/弹性部署服务任务
        - 共绩算力 Open API/任务
      parameters:
        - name: type
          in: query
          description: 任务类型。如果有多个值，请使用英文逗号（,）分隔
          required: true
          example: Deployment
          schema:
            type: string
            enum:
              - Deployment
            x-apifox-enum:
              - value: Deployment
                name: ''
                description: 弹性部署服务
        - name: status
          in: query
          description: 任务状态。如果有多个值，请使用英文逗号（,）分隔
          required: true
          example: Running,Pending,Paused
          schema:
            type: string
            enum:
              - Running
              - Pending
              - Paused
              - End
            x-apifox-enum:
              - value: Running
                name: ''
                description: 运行中
              - value: Pending
                name: ''
                description: 等待中
              - value: Paused
                name: ''
                description: 已停止
              - value: End
                name: ''
                description: 已删除
        - name: search_value
          in: query
          description: 任务名
          required: false
          schema:
            type: string
        - name: page
          in: query
          description: 页码
          required: false
          example: 1
          schema:
            type: integer
            default: 1
        - name: page_size
          in: query
          description: 每页数量
          required: false
          example: 10
          schema:
            type: integer
            default: 10
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
          description: 请求成功
          content:
            application/json:
              schema:
                type: object
                x-apifox-refs:
                  01KEB4ZR0YXZG8P00Q95QJFFT8:
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
                        type: integer
                      results:
                        type: array
                        items:
                          type: object
                          properties:
                            task_id:
                              type: integer
                              title: 任务id
                              nullable: true
                            task_name:
                              type: string
                              title: 任务名称
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
                              type: integer
                              title: 节点数量
                              nullable: true
                            runing_points:
                              type: integer
                              title: 运行中节点数
                              nullable: true
                            billing_value:
                              type: integer
                              title: 累计花费金额
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
                                properties:
                                  service_id:
                                    type: integer
                                    title: 服务id
                                    nullable: true
                                  service_name:
                                    type: string
                                    title: 服务名称
                                  service_image:
                                    type: string
                                    title: 服务镜像
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
                                x-apifox-orders:
                                  - service_id
                                  - service_name
                                  - service_image
                                  - remote_ports
                                type: object
                                x-apifox-refs: {}
                                required:
                                  - service_id
                                  - service_name
                                  - service_image
                                  - remote_ports
                                x-apifox-ignore-properties: []
                              title: 服务列表
                          x-apifox-refs: {}
                          x-apifox-orders:
                            - task_id
                            - task_name
                            - status
                            - points
                            - runing_points
                            - billing_value
                            - resources
                            - services
                          required:
                            - task_id
                            - task_name
                            - status
                            - points
                            - runing_points
                            - billing_value
                            - resources
                            - services
                          x-apifox-ignore-properties: []
                    x-apifox-orders:
                      - count
                      - results
                    x-apifox-refs: {}
                    required:
                      - count
                      - results
                    x-apifox-ignore-properties: []
                    nullable: true
                x-apifox-orders:
                  - 01KEB4ZR0YXZG8P00Q95QJFFT8
                  - data
                required:
                  - code
                  - message
                  - data
                x-apifox-ignore-properties:
                  - code
                  - message
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 共绩算力 Open API/弹性部署服务任务
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-296881864-run
components:
  schemas:
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