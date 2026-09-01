# 设备详情【开机信息】

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/output/v2/device_order/get_device_details_v2:
    post:
      summary: 设备详情【开机信息】
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        获取单个设备的设备详细信息
        注意：设备已处在服务中，才会有内网IP\服务暴露端口\SSH开放端口
      tags:
        - 共绩算力 Open API/裸金属/已购列表
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                device_id:
                  type: integer
                  title: 设备ID
              required:
                - device_id
              x-apifox-orders:
                - device_id
            example:
              device_id: 672
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
                      order_details_id:
                        type: integer
                        title: 订单详情ID
                      start_time:
                        type: 'null'
                        title: 服务开始时间
                      end_time:
                        type: 'null'
                        title: 服务结束时间
                      pub_ip:
                        type: string
                        title: 设备公网IP
                      inner_ip:
                        type: string
                        title: 设备内网IP
                      ssh_port:
                        type: 'null'
                        title: 设备ssh端口
                      device_username:
                        type: 'null'
                        title: 设备登录账号
                      device_passwd:
                        type: 'null'
                        title: 设备登录密码
                      billing_type:
                        type: string
                        title: 计费方式
                      network_type:
                        type: string
                        title: 网络类型
                      network_name:
                        type: string
                        title: 网络名称
                      operating_system:
                        type: string
                        title: 设备操作系统
                      cpu_model:
                        type: string
                        title: 设备CPU型号
                      memory_size:
                        type: integer
                        title: 设备内存（单位MB）
                      gpu_count:
                        type: integer
                        title: 设备GPU数量
                      gpu_model:
                        type: string
                        title: 设备GPU型号
                      gpu_driver_version:
                        type: string
                        title: 设备GPU驱动版本
                      cuda_version:
                        type: string
                        title: 设备cuda版本
                      system_disk_size:
                        type: integer
                        title: 设备硬盘空间（单位MB）
                      estimated_time:
                        type: string
                        title: 预计开机时间
                        description: 目前无实际参考意义
                      expose_ports:
                        type: array
                        items:
                          type: object
                          properties:
                            local_port:
                              type: integer
                              x-apifox-mock: 本机端口
                            mapping_port:
                              type: integer
                              x-apifox-mock: 外网端口
                          x-apifox-orders:
                            - local_port
                            - mapping_port
                        title: 服务暴露端口
                    required:
                      - order_details_id
                      - start_time
                      - end_time
                      - pub_ip
                      - inner_ip
                      - ssh_port
                      - device_username
                      - device_passwd
                      - billing_type
                      - network_type
                      - network_name
                      - operating_system
                      - cpu_model
                      - memory_size
                      - gpu_count
                      - gpu_model
                      - gpu_driver_version
                      - cuda_version
                      - system_disk_size
                      - estimated_time
                      - expose_ports
                    x-apifox-orders:
                      - order_details_id
                      - start_time
                      - end_time
                      - pub_ip
                      - inner_ip
                      - ssh_port
                      - device_username
                      - device_passwd
                      - billing_type
                      - network_type
                      - network_name
                      - operating_system
                      - cpu_model
                      - memory_size
                      - gpu_count
                      - gpu_model
                      - gpu_driver_version
                      - cuda_version
                      - system_disk_size
                      - estimated_time
                      - expose_ports
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
                  order_details_id: 1
                  start_time: null
                  end_time: null
                  pub_ip: 183.1.1.1
                  inner_ip: 172.1.1.1
                  ssh_port: null
                  device_username: null
                  device_passwd: null
                  billing_type: Hour
                  network_type: NVLinkSwitch
                  network_name: NS-test
                  operating_system: ubuntu (5.15.0-161-generic)
                  cpu_model: Intel(R) Xeon(R) Gold 6133 CPU @ 2.50GHz
                  memory_size: 515641
                  gpu_count: 4
                  gpu_model: '3090'
                  gpu_driver_version: 570.86.10
                  cuda_version: '12.8'
                  system_disk_size: 4273819
                  estimated_time: '2026-08-05T09:40:49.818142+08:00'
                  expose_ports:
                    - local_port: 5001
                      mapping_port: 50050
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 共绩算力 Open API/裸金属/已购列表
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-497148897-run
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