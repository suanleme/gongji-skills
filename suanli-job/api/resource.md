# 获取设备资源列表

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/deployment/resource/search:
    get:
      summary: 获取设备资源列表
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        获取设备资源列表及其相关信息。
      tags:
        - 共绩算力 Open API/资源
        - 共绩算力 Open API/任务
      parameters:
        - name: task_type
          in: query
          description: 如果有多个值，请使用英文逗号（,）分隔
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
        - name: device_type
          in: query
          description: 如果有多个值，请使用英文逗号（,）分隔
          required: true
          example: GpuDevice
          schema:
            type: string
            enum:
              - GpuDevice
              - CpuDevice
            x-apifox-enum:
              - value: GpuDevice
                name: GPU设备
                description: GPU资源
              - value: CpuDevice
                name: CPU设备
                description: Cpu资源
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
            type: number
      responses:
        '200':
          x-apifox-name: 成功
          description: ''
          content:
            application/json:
              schema:
                type: object
                x-apifox-refs:
                  01KE9D5NK4XX01VN43XC0BDHAQ:
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
                          properties:
                            device_name:
                              type: string
                              title: 设备名称
                            regions:
                              type: array
                              items:
                                type: object
                                properties:
                                  region:
                                    type: string
                                    title: 区域唯一标识
                                  region_name:
                                    type: string
                                    title: 区域名称
                                  mark:
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
                                            title: 区域tag
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
                                        x-apifox-ignore-properties: []
                                      mark:
                                        type: string
                                        title: 设备唯一标识
                                    required:
                                      - resource
                                      - mark
                                    x-apifox-orders:
                                      - resource
                                      - mark
                                    x-apifox-ignore-properties: []
                                  price:
                                    type: integer
                                    title: 设备价格
                                    nullable: true
                                  discount_price:
                                    type: integer
                                    title: 折扣价格
                                    nullable: true
                                  inventory:
                                    type: integer
                                    title: 库存数
                                required:
                                  - region
                                  - region_name
                                  - mark
                                  - price
                                  - discount_price
                                  - inventory
                                x-apifox-orders:
                                  - region
                                  - region_name
                                  - mark
                                  - price
                                  - discount_price
                                  - inventory
                                x-apifox-ignore-properties: []
                              title: 资源所属区域列表
                            gpu_name:
                              type: string
                              title: GPU名称
                            gpu_memory:
                              type: integer
                              title: GPU显存
                            gpu_count:
                              type: integer
                              title: GPU数量
                            memory:
                              type: integer
                              title: 内存
                            cpu_cores:
                              type: integer
                              title: CPU核数
                            disk_size:
                              type: integer
                              title: 硬盘类型
                            disk_type:
                              type: string
                              title: 硬盘大小
                          x-apifox-refs: {}
                          x-apifox-orders:
                            - device_name
                            - regions
                            - gpu_name
                            - gpu_memory
                            - gpu_count
                            - memory
                            - cpu_cores
                            - disk_size
                            - disk_type
                          required:
                            - device_name
                            - regions
                            - gpu_name
                            - gpu_memory
                            - gpu_count
                            - memory
                            - cpu_cores
                            - disk_size
                            - disk_type
                          x-apifox-ignore-properties: []
                    x-apifox-orders:
                      - count
                      - results
                    required:
                      - count
                      - results
                    x-apifox-ignore-properties: []
                    nullable: true
                x-apifox-orders:
                  - 01KE9D5NK4XX01VN43XC0BDHAQ
                  - data
                required:
                  - code
                  - message
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
                    - device_name: H20 x 8
                      regions:
                        - region: hebeif-1
                          region_name: 河北一区
                          mark:
                            resource:
                              device_name: H20 x 8
                              region: hebeif-1
                              gpu_name: H20
                              gpu_count: 8
                              gpu_memory: 786432
                              memory: 1572864
                              cpu_cores: 192
                            region_name: null
                            mark: >-
                              ha8GDGEAORN3a9Hhu7X+W4Vtce8YV33R2cqzDf1CeFte7rPSMOMpgrHAlL3THz4zxz17CQ2xan6Q2UrnIQ6pUPcLqpoLUCh5MaAY9kIet8llTG2oulHTzTR0DoTuhhQcWfNOpn3zHQbZ3F73AivgnZVpBnOidOQtK7OFQF2etyubD5p/9khWFNjEhW7QZGN49g==
                          price: 16416
                          discount_price: 16416
                          inventory: 0
                        - region: xingjiangf-1
                          region_name: 新疆一区
                          mark:
                            resource:
                              device_name: H20 x 8
                              region: xingjiangf-1
                              gpu_name: H20
                              gpu_count: 8
                              gpu_memory: 786432
                              memory: 1572864
                              cpu_cores: 192
                            mark: >-
                              ha8GDGEAORN3a9Hhu7X+W4Vtce8YV33R2cqzDf1CeFte7rPCPO8rgb6My/iZEGhhnkByGBWLJiXf9FrtIWq5B6VS154UUBlufO9OrkJD/5AYRniwik7PgmExT5Dggh4GT60Z5zDsAUmMnxLiCiLjnotzUzf7CeQyLImVDRXK/TvcZdwJCgWWDknwrBCDIAAVli9FdX8=
                          price: 16416
                          discount_price: 16416
                          inventory: 0
                      gpu_name: H20
                      gpu_memory: 786432
                      gpu_count: 8
                      memory: 1572864
                      cpu_cores: 192
                      disk_size: 81920
                      disk_type: HDD
          headers: {}
      security: []
      x-apifox-folder: 共绩算力 Open API/资源
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-296881020-run
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