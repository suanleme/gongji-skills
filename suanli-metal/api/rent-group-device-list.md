# 已购组网设备列表

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/output/v2/device-output/list_rent_device_network_v2:
    post:
      summary: 已购组网设备列表
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        获取已购买且订单没有结束的组网设备列表
      tags:
        - 共绩算力 Open API/裸金属/已购列表
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties: {}
            examples: {}
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
                  message:
                    type: string
                  data:
                    type: array
                    items:
                      type: object
                      properties:
                        network_id:
                          type: integer
                          title: 网络ID
                        network_type:
                          type: string
                          title: 网络类型
                        network_name:
                          type: string
                          title: 网络名称
                        inner:
                          type: array
                          items:
                            type: object
                            properties:
                              billing_type:
                                type: string
                                title: 计费方式
                                enum:
                                  - Hour
                                  - Day
                                  - Week
                                  - Month
                                x-apifox-enum:
                                  - value: Hour
                                    name: 小时时长包
                                    description: ''
                                  - value: Day
                                    name: 24小时时长包
                                    description: ''
                                  - value: Week
                                    name: 7天时长包
                                    description: ''
                                  - value: Month
                                    name: 30天时长包
                                    description: ''
                              inner_ip:
                                type: string
                                title: 设备内网IP
                              pub_ip:
                                type: string
                                title: 设备公网IP
                              network_id:
                                type: integer
                                title: 网络ID
                              network_type:
                                type: string
                                title: 网路类型
                              cores:
                                type: integer
                                title: 设备核数
                              cpu_model:
                                type: string
                                title: 设备CPU型号
                              gpu_model:
                                type: string
                                title: 设备GPU型号
                              gpu_count:
                                type: integer
                                title: 设备GPU数量
                              gpu_memory:
                                type: integer
                                title: 设备GPU显存（单位MB）
                              memory_size:
                                type: integer
                                title: 设备内存（单位MB）
                              gpu_driver_version:
                                type: string
                                title: 设备GPU驱动版本
                              cuda_version:
                                type: string
                                title: 设备cuda版本
                              operating_system:
                                type: string
                                title: 设备操作系统
                              system_disk_size:
                                type: integer
                                title: 设备硬盘空间（单位MB）
                              system_disk_type:
                                type: string
                                title: 硬盘类型：NVMe,SSD,HDD,SCSI
                              use_end_time:
                                type: string
                                title: 订单结束时间
                                nullable: true
                              use_start_time:
                                type: string
                                title: 订单开始时间
                                nullable: true
                              idc_name:
                                type: string
                                title: 设备机房名称
                              order_details_id:
                                type: integer
                                title: 订单详情ID
                              zone_name:
                                type: string
                                title: 设备区域名称
                              device_id:
                                type: integer
                                title: 设备ID
                              order_detail_status:
                                type: string
                                title: 订单详情状态
                                enum:
                                  - Default
                                  - Waiting
                                  - Serving
                                  - Finished
                                  - Canceled
                                  - CanceledRefunded
                                x-apifox-enum:
                                  - value: Default
                                    name: 默认
                                    description: ''
                                  - value: Waiting
                                    name: 等待中
                                    description: ''
                                  - value: Serving
                                    name: 服务中
                                    description: ''
                                  - value: Finished
                                    name: 已结束
                                    description: ''
                                  - value: Canceled
                                    name: 已取消
                                    description: ''
                                  - value: CanceledRefunded
                                    name: 已取消并退款
                                    description: ''
                              create_channel:
                                type: string
                                title: 订单创建渠道
                                enum:
                                  - OutputPlatform
                                  - MiddlePlatform
                                x-apifox-enum:
                                  - value: OutputPlatform
                                    name: 裸金属输出端
                                    description: ''
                                  - value: MiddlePlatform
                                    name: 中台
                                    description: ''
                            required:
                              - billing_type
                              - inner_ip
                              - pub_ip
                              - network_id
                              - network_type
                              - cores
                              - cpu_model
                              - gpu_model
                              - gpu_count
                              - gpu_memory
                              - memory_size
                              - gpu_driver_version
                              - cuda_version
                              - operating_system
                              - system_disk_size
                              - system_disk_type
                              - use_end_time
                              - use_start_time
                              - idc_name
                              - order_details_id
                              - zone_name
                              - device_id
                              - order_detail_status
                              - create_channel
                            x-apifox-orders:
                              - billing_type
                              - inner_ip
                              - pub_ip
                              - network_id
                              - network_type
                              - cores
                              - cpu_model
                              - gpu_model
                              - gpu_count
                              - gpu_memory
                              - memory_size
                              - gpu_driver_version
                              - cuda_version
                              - operating_system
                              - system_disk_size
                              - system_disk_type
                              - use_end_time
                              - use_start_time
                              - idc_name
                              - order_details_id
                              - zone_name
                              - device_id
                              - order_detail_status
                              - create_channel
                      x-apifox-orders:
                        - network_id
                        - network_type
                        - network_name
                        - inner
                required:
                  - code
                  - message
                  - data
                x-apifox-orders:
                  - code
                  - message
                  - data
              example:
                code: '0000'
                message: success
                data:
                  - network_id: 1
                    network_type: NVLinkSwitch
                    network_name: NS-test
                    inner:
                      - billing_type: Hour
                        inner_ip: 172.1.1.1
                        pub_ip: 183.1.1.1
                        network_id: 1
                        network_type: NVLinkSwitch
                        cores: 80
                        cpu_model: Intel(R) Xeon(R) Gold 6133 CPU @ 2.50GHz
                        gpu_model: '3090'
                        gpu_count: 4
                        gpu_memory: 24576
                        memory_size: 515641
                        gpu_driver_version: 570.86.10
                        cuda_version: '12.8'
                        operating_system: ubuntu (5.15.0-161-generic)
                        system_disk_size: 4273819
                        system_disk_type: NVMe
                        use_end_time: '2026-08-04T12:20:17.872387+08:00'
                        use_start_time: '2026-08-04T11:20:17.872387+08:00'
                        idc_name: cn-region-test
                        order_details_id: 1
                        zone_name: 测试区域
                        device_id: 1
                        order_detail_status: Serving
                        create_channel: OutputPlatform
                      - billing_type: Hour
                        inner_ip: 172.1.1.1
                        pub_ip: 183.1.1.1
                        network_id: 1
                        network_type: NVLinkSwitch
                        cores: 80
                        cpu_model: Intel(R) Xeon(R) Gold 6133 CPU @ 2.50GHz
                        gpu_model: '3090'
                        gpu_count: 4
                        gpu_memory: 24576
                        memory_size: 515601
                        gpu_driver_version: 570.86.10
                        cuda_version: '12.8'
                        operating_system: ubuntu (5.15.0-161-generic)
                        system_disk_size: 4273818
                        system_disk_type: NVMe
                        use_end_time: null
                        use_start_time: null
                        idc_name: cn-region-test
                        order_details_id: 2
                        zone_name: 测试区域
                        device_id: 2
                        order_detail_status: Waiting
                        create_channel: OutputPlatform
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 共绩算力 Open API/裸金属/已购列表
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-496695377-run
components:
  schemas: {}
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