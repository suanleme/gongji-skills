# 节点数量修改接口

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/deployment/task/change_points:
    post:
      summary: 节点数量修改接口
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        修改任务节点数量
      tags:
        - 共绩算力 Open API/弹性部署服务节点
        - 共绩算力 Open API/节点
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
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                task_id:
                  type: number
                  title: 任务id
                points:
                  type: number
                  title: 修改的任务点数
              required:
                - task_id
                - points
              x-apifox-orders:
                - task_id
                - points
              x-apifox-ignore-properties: []
            example:
              task_id: 388
              points: 1
      responses:
        '200':
          x-apifox-name: 成功
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
                    type: 'null'
                x-apifox-orders:
                  - 01KV0B7RZPGB3AYBWN33XM0JV4
                  - data
                required:
                  - code
                  - message
                  - data
                x-apifox-refs:
                  01KV0B7RZPGB3AYBWN33XM0JV4:
                    $ref: '#/components/schemas/IResponse'
                x-apifox-ignore-properties:
                  - code
                  - message
              example:
                code: '0000'
                message: success
          headers: {}
      security: []
      x-apifox-folder: 共绩算力 Open API/弹性部署服务节点
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-296883326-run
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