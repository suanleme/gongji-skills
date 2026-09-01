# 组网设备可购列表

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/output/v2/device-output/page_list_product_network_v2:
    post:
      summary: 组网设备可购列表
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        获取组网裸金属可购买列表及裸金属基础信息。
      tags:
        - 共绩算力 Open API/裸金属/可购列表
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                billing_type:
                  type: string
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
                  title: 计费方式
                zone_id:
                  type: integer
                  title: 区域ID
                gpu_count:
                  type: integer
                  title: 单机 GPU 数量
                gpu_models:
                  type: array
                  items:
                    type: string
                  title: 卡型集合
                device_count:
                  type: integer
                  title: 设备数量
                network_type:
                  type: string
                  title: 网络类型
                  enum:
                    - Ib
                    - Roce
                    - NVLinkSwitch
                    - EthernetFast
                  x-apifox-enum:
                    - value: Ib
                      name: IB网络
                      description: ''
                    - value: Roce
                      name: RoCE网络
                      description: ''
                    - value: NVLinkSwitch
                      name: NVLink-Switch网络
                      description: ''
                    - value: EthernetFast
                      name: 高速以太网
                      description: ''
              required:
                - billing_type
                - device_count
                - network_type
              x-apifox-orders:
                - billing_type
                - zone_id
                - gpu_count
                - gpu_models
                - device_count
                - network_type
            example:
              billing_type: Hour
              zone_id: 1
              gpu_count: 4
              gpu_models:
                - '4090'
                - '5090'
              device_count: 2
              network_type: EthernetFast
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
                        network_type:
                          type: string
                          title: 网络类型
                        zone_name:
                          type: string
                          title: 设备区域名称
                        idc_name:
                          type: string
                          title: 设备机房名称
                        network_id:
                          type: integer
                          title: 网络ID
                        inner:
                          type: array
                          items:
                            type: object
                            properties:
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
                              end_time:
                                type: string
                                title: 设备结束时间
                              start_time:
                                type: string
                                title: 设备开始时间
                              device_id:
                                type: integer
                                title: 设备ID
                              hour_price:
                                type: integer
                                title: 小时时长包价格
                                description: 1000000=1元
                              day_price:
                                type: integer
                                title: 24小时时长包价格
                                description: 1000000=1元
                              week_price:
                                type: integer
                                title: 7天时长包价格
                                description: 1000000=1元
                              month_price:
                                type: integer
                                title: 30天时长包价格
                                description: 1000000=1元
                              idc_id:
                                type: integer
                                title: 设备机房ID
                              hour_price_discount:
                                type: 'null'
                                title: 租户折扣 - 小时时长包价格
                                description: 1000000=1元
                              day_price_discount:
                                type: 'null'
                                title: 租户折扣 - 24小时时长包价格
                                description: 1000000=1元
                              week_price_discount:
                                type: 'null'
                                title: 租户折扣 - 7天时长包价格
                                description: 1000000=1元
                              month_price_discount:
                                type: 'null'
                                title: 租户折扣 - 30天时长包价格
                                description: 1000000=1元
                              migration_mode:
                                type: 'null'
                                title: 设备迁移类型：Flexible-灵活迁移，Fast-快速迁移
                              cooperation_mode:
                                type: string
                                title: 设备合作模式：IdleElastic-闲时弹性，IdleFullRent-闲时整租
                              allow_switch_to_elastic_full_rent:
                                type: boolean
                                title: 设备允许切换至弹性整租
                              max_buy_count:
                                type: integer
                                title: 最多购买数
                            required:
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
                              - end_time
                              - start_time
                              - device_id
                              - hour_price
                              - day_price
                              - week_price
                              - month_price
                              - idc_id
                              - hour_price_discount
                              - day_price_discount
                              - week_price_discount
                              - month_price_discount
                              - migration_mode
                              - cooperation_mode
                              - allow_switch_to_elastic_full_rent
                              - max_buy_count
                            x-apifox-orders:
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
                              - end_time
                              - start_time
                              - device_id
                              - hour_price
                              - day_price
                              - week_price
                              - month_price
                              - idc_id
                              - hour_price_discount
                              - day_price_discount
                              - week_price_discount
                              - month_price_discount
                              - migration_mode
                              - cooperation_mode
                              - allow_switch_to_elastic_full_rent
                              - max_buy_count
                      x-apifox-orders:
                        - network_type
                        - zone_name
                        - idc_name
                        - network_id
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
                  - network_type: NVLinkSwitch
                    zone_name: 测试区域
                    idc_name: cn-region-test
                    network_id: 1
                    inner:
                      - cores: 80
                        cpu_model: Intel(R) Xeon(R) Gold 6133 CPU @ 2.50GHz
                        gpu_model: '3090'
                        gpu_count: 4
                        gpu_memory: 24576
                        memory_size: 515641
                        gpu_driver_version: 580.173.02
                        cuda_version: '13.0'
                        operating_system: ubuntu (5.15.0-161-generic)
                        system_disk_size: 4273755
                        system_disk_type: NVMe
                        end_time: '2026-10-31T00:00:00+08:00'
                        start_time: '2026-08-03T00:00:00+08:00'
                        device_id: 1
                        hour_price: 15000000
                        day_price: 166000000
                        week_price: 666000000
                        month_price: 1888000000
                        idc_id: 1
                        hour_price_discount: null
                        day_price_discount: null
                        week_price_discount: null
                        month_price_discount: null
                        migration_mode: null
                        cooperation_mode: IdleFullRent
                        allow_switch_to_elastic_full_rent: false
                        max_buy_count: 2096
                      - cores: 80
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
                        end_time: '2026-10-28T00:00:00+08:00'
                        start_time: '2026-08-03T00:00:00+08:00'
                        device_id: 2
                        hour_price: 15000000
                        day_price: 166000000
                        week_price: 666000000
                        month_price: 1888000000
                        idc_id: 1
                        hour_price_discount: null
                        day_price_discount: null
                        week_price_discount: null
                        month_price_discount: null
                        migration_mode: null
                        cooperation_mode: IdleFullRent
                        allow_switch_to_elastic_full_rent: false
                        max_buy_count: 2024
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 共绩算力 Open API/裸金属/可购列表
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-496652989-run
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