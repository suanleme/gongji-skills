# 节点日志查询接口

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/deployment/task/point_log:
    get:
      summary: 节点日志查询接口
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        获取弹性部署任务节点的日志信息。
      tags:
        - 共绩算力 Open API/弹性部署服务节点
        - 共绩算力 Open API/任务
      parameters:
        - name: task_id
          in: query
          description: 任务ID
          required: true
          example: 1
          schema:
            type: number
        - name: point_id
          in: query
          description: 节点ID
          required: true
          example: 1
          schema:
            type: number
        - name: service_id
          in: query
          description: 服务ID，从任务详情中获取。
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
          x-apifox-name: 成功
          description: 查询成功
          content:
            application/json:
              schema:
                type: object
                x-apifox-refs:
                  01KFAGHFCS9AJATERRZ9V4YWB7:
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
                      logs:
                        type: string
                    x-apifox-orders:
                      - logs
                    required:
                      - logs
                    x-apifox-ignore-properties: []
                    nullable: true
                required:
                  - code
                  - message
                  - data
                x-apifox-orders:
                  - 01KFAGHFCS9AJATERRZ9V4YWB7
                  - data
                x-apifox-ignore-properties:
                  - code
                  - message
          headers: {}
      security: []
      x-apifox-folder: 共绩算力 Open API/弹性部署服务节点
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-335612564-run
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