# 单机设备可购列表

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/output/v2/device-output/page_list_product_single_v2:
    post:
      summary: 单机设备可购列表
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        获取单机裸金属可购买列表及裸金属基础信息。
      tags:
        - 共绩算力 Open API/裸金属/可购列表
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                page:
                  type: integer
                  title: 页码
                page_size:
                  type: integer
                  title: 每页数量
                conditional:
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
                    gpu_models:
                      type: array
                      items:
                        type: string
                      title: 卡型集合
                      description: 为空代表全部
                    zone_id:
                      type: integer
                      title: 区域ID
                    gpu_count:
                      type: integer
                      title: 单机 GPU 数量
                  required:
                    - billing_type
                    - gpu_models
                  x-apifox-orders:
                    - billing_type
                    - gpu_models
                    - zone_id
                    - gpu_count
              required:
                - conditional
                - page_size
                - page
              x-apifox-orders:
                - page
                - page_size
                - conditional
            example:
              page: 1
              page_size: 10
              conditional:
                billing_type: Day
                gpu_models:
                  - '4090'
                  - '5090'
                zone_id: 1
                gpu_count: 2
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
                    type: object
                    properties:
                      count:
                        type: integer
                      results:
                        type: array
                        items:
                          type: object
                          properties:
                            network_type:
                              type: string
                              title: 网络类型
                            network_id:
                              type: integer
                              title: 网络ID
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
                            idc_name:
                              type: string
                              title: 设备机房名称
                            idc_id:
                              type: integer
                              title: 设备机房ID
                            zone_name:
                              type: string
                              title: 设备区域名称
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
                            listing_mode:
                              type: string
                              title: 设备上架模式：Single-单机模式，Proxy-网关代理模式，Direct-网关直连模式
                            gateway_type:
                              type: string
                              title: 设备网关类型
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
                            - idc_name
                            - idc_id
                            - zone_name
                            - end_time
                            - start_time
                            - device_id
                            - hour_price
                            - day_price
                            - week_price
                            - month_price
                            - listing_mode
                            - gateway_type
                            - hour_price_discount
                            - day_price_discount
                            - week_price_discount
                            - month_price_discount
                            - migration_mode
                            - cooperation_mode
                            - allow_switch_to_elastic_full_rent
                            - max_buy_count
                            - network_type
                            - network_id
                            - cores
                          x-apifox-orders:
                            - network_type
                            - network_id
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
                            - idc_name
                            - idc_id
                            - zone_name
                            - end_time
                            - start_time
                            - device_id
                            - hour_price
                            - day_price
                            - week_price
                            - month_price
                            - listing_mode
                            - gateway_type
                            - hour_price_discount
                            - day_price_discount
                            - week_price_discount
                            - month_price_discount
                            - migration_mode
                            - cooperation_mode
                            - allow_switch_to_elastic_full_rent
                            - max_buy_count
                    required:
                      - count
                      - results
                    x-apifox-orders:
                      - count
                      - results
                required:
                  - code
                  - message
                  - data
                x-apifox-orders:
                  - code
                  - message
                  - data
              example:
                count: 13
                results:
                  - network_type: null
                    network_id: null
                    cores: 128
                    cpu_model: INTEL(R) XEON(R) GOLD 6530
                    gpu_model: '5090'
                    gpu_count: 8
                    gpu_memory: 32607
                    memory_size: 515610
                    gpu_driver_version: 580.105.08
                    cuda_version: '13.0'
                    operating_system: ubuntu (5.15.0-179-generic)
                    system_disk_size: 15566270
                    system_disk_type: NVMe
                    idc_name: 测试一区机房
                    idc_id: 1
                    zone_name: 测试一区
                    end_time: '2031-07-31T00:00:00+08:00'
                    start_time: '2026-07-17T00:00:00+08:00'
                    device_id: 1
                    hour_price: 28000000
                    day_price: 638000000
                    week_price: 4245000000
                    month_price: 17285000000
                    listing_mode: Direct
                    gateway_type: Direct
                    hour_price_discount: null
                    day_price_discount: null
                    week_price_discount: null
                    month_price_discount: null
                    migration_mode: null
                    cooperation_mode: IdleFullRent
                    allow_switch_to_elastic_full_rent: false
                    max_buy_count: 43717
                  - network_type: null
                    network_id: null
                    cores: 128
                    cpu_model: INTEL(R) XEON(R) GOLD 6530
                    gpu_model: '5090'
                    gpu_count: 8
                    gpu_memory: 32607
                    memory_size: 515610
                    gpu_driver_version: 580.82.07
                    cuda_version: '13.0'
                    operating_system: ubuntu (5.15.0-181-generic)
                    system_disk_size: 15566999
                    system_disk_type: NVMe
                    idc_name: 测试一区机房
                    idc_id: 1
                    zone_name: 测试一区
                    end_time: '2028-07-31T00:00:00+08:00'
                    start_time: '2026-07-17T00:00:00+08:00'
                    device_id: 1
                    hour_price: 28000000
                    day_price: 638000000
                    week_price: 4245000000
                    month_price: 17285000000
                    listing_mode: Direct
                    gateway_type: Direct
                    hour_price_discount: null
                    day_price_discount: null
                    week_price_discount: null
                    month_price_discount: null
                    migration_mode: null
                    cooperation_mode: IdleFullRent
                    allow_switch_to_elastic_full_rent: false
                    max_buy_count: 17437
                  - network_type: null
                    network_id: null
                    cores: 128
                    cpu_model: INTEL(R) XEON(R) GOLD 6530
                    gpu_model: '5090'
                    gpu_count: 8
                    gpu_memory: 32607
                    memory_size: 515610
                    gpu_driver_version: '580.142'
                    cuda_version: '13.0'
                    operating_system: ubuntu (5.15.0-94-generic)
                    system_disk_size: 15566065
                    system_disk_type: NVMe
                    idc_name: 测试一区机房
                    idc_id: 1
                    zone_name: 测试一区
                    end_time: '2028-07-31T00:00:00+08:00'
                    start_time: '2026-07-17T00:00:00+08:00'
                    device_id: 1
                    hour_price: 28000000
                    day_price: 638000000
                    week_price: 4245000000
                    month_price: 17285000000
                    listing_mode: Direct
                    gateway_type: Direct
                    hour_price_discount: null
                    day_price_discount: null
                    week_price_discount: null
                    month_price_discount: null
                    migration_mode: null
                    cooperation_mode: IdleFullRent
                    allow_switch_to_elastic_full_rent: false
                    max_buy_count: 17437
                  - network_type: null
                    network_id: null
                    cores: 128
                    cpu_model: INTEL(R) XEON(R) GOLD 6530
                    gpu_model: '5090'
                    gpu_count: 8
                    gpu_memory: 32607
                    memory_size: 515611
                    gpu_driver_version: 580.82.07
                    cuda_version: '13.0'
                    operating_system: ubuntu (5.15.0-94-generic)
                    system_disk_size: 15566931
                    system_disk_type: NVMe
                    idc_name: 测试一区机房
                    idc_id: 1
                    zone_name: 测试一区
                    end_time: '2028-07-31T00:00:00+08:00'
                    start_time: '2026-07-17T00:00:00+08:00'
                    device_id: 1
                    hour_price: 28000000
                    day_price: 638000000
                    week_price: 4245000000
                    month_price: 17285000000
                    listing_mode: Direct
                    gateway_type: Direct
                    hour_price_discount: null
                    day_price_discount: null
                    week_price_discount: null
                    month_price_discount: null
                    migration_mode: null
                    cooperation_mode: IdleFullRent
                    allow_switch_to_elastic_full_rent: false
                    max_buy_count: 17437
                  - network_type: null
                    network_id: null
                    cores: 128
                    cpu_model: INTEL(R) XEON(R) GOLD 6530
                    gpu_model: '5090'
                    gpu_count: 8
                    gpu_memory: 32607
                    memory_size: 515610
                    gpu_driver_version: 580.82.07
                    cuda_version: '13.0'
                    operating_system: ubuntu (5.15.0-181-generic)
                    system_disk_size: 15566897
                    system_disk_type: NVMe
                    idc_name: 测试一区机房
                    idc_id: 1
                    zone_name: 测试一区
                    end_time: '2028-07-31T00:00:00+08:00'
                    start_time: '2026-07-17T00:00:00+08:00'
                    device_id: 1
                    hour_price: 28000000
                    day_price: 638000000
                    week_price: 4245000000
                    month_price: 17285000000
                    listing_mode: Direct
                    gateway_type: Direct
                    hour_price_discount: null
                    day_price_discount: null
                    week_price_discount: null
                    month_price_discount: null
                    migration_mode: null
                    cooperation_mode: IdleFullRent
                    allow_switch_to_elastic_full_rent: false
                    max_buy_count: 17437
                  - network_type: null
                    network_id: null
                    cores: 128
                    cpu_model: INTEL(R) XEON(R) GOLD 6530
                    gpu_model: '5090'
                    gpu_count: 8
                    gpu_memory: 32607
                    memory_size: 515610
                    gpu_driver_version: 580.82.07
                    cuda_version: '13.0'
                    operating_system: ubuntu (5.15.0-181-generic)
                    system_disk_size: 15566897
                    system_disk_type: NVMe
                    idc_name: 测试一区机房
                    idc_id: 1
                    zone_name: 测试一区
                    end_time: '2028-07-31T00:00:00+08:00'
                    start_time: '2026-07-17T00:00:00+08:00'
                    device_id: 1
                    hour_price: 28000000
                    day_price: 638000000
                    week_price: 4245000000
                    month_price: 17285000000
                    listing_mode: Direct
                    gateway_type: Direct
                    hour_price_discount: null
                    day_price_discount: null
                    week_price_discount: null
                    month_price_discount: null
                    migration_mode: null
                    cooperation_mode: IdleFullRent
                    allow_switch_to_elastic_full_rent: false
                    max_buy_count: 17437
                  - network_type: null
                    network_id: null
                    cores: 128
                    cpu_model: INTEL(R) XEON(R) GOLD 6530
                    gpu_model: '5090'
                    gpu_count: 8
                    gpu_memory: 32607
                    memory_size: 515610
                    gpu_driver_version: 580.82.07
                    cuda_version: '13.0'
                    operating_system: ubuntu (5.15.0-181-generic)
                    system_disk_size: 15566950
                    system_disk_type: NVMe
                    idc_name: 测试一区机房
                    idc_id: 1
                    zone_name: 测试一区
                    end_time: '2028-07-31T00:00:00+08:00'
                    start_time: '2026-07-17T00:00:00+08:00'
                    device_id: 1
                    hour_price: 28000000
                    day_price: 638000000
                    week_price: 4245000000
                    month_price: 17285000000
                    listing_mode: Direct
                    gateway_type: Direct
                    hour_price_discount: null
                    day_price_discount: null
                    week_price_discount: null
                    month_price_discount: null
                    migration_mode: null
                    cooperation_mode: IdleFullRent
                    allow_switch_to_elastic_full_rent: false
                    max_buy_count: 17437
                  - network_type: null
                    network_id: null
                    cores: 128
                    cpu_model: INTEL(R) XEON(R) GOLD 6530
                    gpu_model: '5090'
                    gpu_count: 8
                    gpu_memory: 32607
                    memory_size: 515610
                    gpu_driver_version: 580.82.07
                    cuda_version: '13.0'
                    operating_system: ubuntu (5.15.0-181-generic)
                    system_disk_size: 15566950
                    system_disk_type: NVMe
                    idc_name: 测试一区机房
                    idc_id: 1
                    zone_name: 测试一区
                    end_time: '2028-07-31T00:00:00+08:00'
                    start_time: '2026-07-17T00:00:00+08:00'
                    device_id: 1
                    hour_price: 28000000
                    day_price: 638000000
                    week_price: 4245000000
                    month_price: 17285000000
                    listing_mode: Direct
                    gateway_type: Direct
                    hour_price_discount: null
                    day_price_discount: null
                    week_price_discount: null
                    month_price_discount: null
                    migration_mode: null
                    cooperation_mode: IdleFullRent
                    allow_switch_to_elastic_full_rent: false
                    max_buy_count: 17437
                  - network_type: null
                    network_id: null
                    cores: 128
                    cpu_model: INTEL(R) XEON(R) GOLD 6530
                    gpu_model: '5090'
                    gpu_count: 8
                    gpu_memory: 32607
                    memory_size: 515610
                    gpu_driver_version: 580.82.07
                    cuda_version: '13.0'
                    operating_system: ubuntu (5.15.0-181-generic)
                    system_disk_size: 15566897
                    system_disk_type: NVMe
                    idc_name: 测试一区机房
                    idc_id: 1
                    zone_name: 测试一区
                    end_time: '2028-07-31T00:00:00+08:00'
                    start_time: '2026-07-17T00:00:00+08:00'
                    device_id: 1
                    hour_price: 28000000
                    day_price: 638000000
                    week_price: 4245000000
                    month_price: 17285000000
                    listing_mode: Direct
                    gateway_type: Direct
                    hour_price_discount: null
                    day_price_discount: null
                    week_price_discount: null
                    month_price_discount: null
                    migration_mode: null
                    cooperation_mode: IdleFullRent
                    allow_switch_to_elastic_full_rent: false
                    max_buy_count: 17437
                  - network_type: null
                    network_id: null
                    cores: 128
                    cpu_model: INTEL(R) XEON(R) GOLD 6530
                    gpu_model: '5090'
                    gpu_count: 8
                    gpu_memory: 32607
                    memory_size: 515610
                    gpu_driver_version: 580.105.08
                    cuda_version: '13.0'
                    operating_system: ubuntu (5.15.0-181-generic)
                    system_disk_size: 15566382
                    system_disk_type: NVMe
                    idc_name: 测试一区机房
                    idc_id: 1
                    zone_name: 测试一区
                    end_time: '2027-06-07T00:00:00+08:00'
                    start_time: '2026-07-22T00:00:00+08:00'
                    device_id: 1
                    hour_price: 28000000
                    day_price: 638000000
                    week_price: 4245000000
                    month_price: 17285000000
                    listing_mode: Direct
                    gateway_type: Direct
                    hour_price_discount: null
                    day_price_discount: null
                    week_price_discount: null
                    month_price_discount: null
                    migration_mode: null
                    cooperation_mode: IdleFullRent
                    allow_switch_to_elastic_full_rent: false
                    max_buy_count: 7357
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 共绩算力 Open API/裸金属/可购列表
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-496591301-run
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