# 任务暂停接口

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/deployment/task/pause:
    post:
      summary: 任务暂停接口
      deprecated: false
      description: |-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
        | --- | --- | --- | --- |
        | v1.0.0 | - | 否 | 是 |

        ### **描述**
        暂停运行中的弹性部署任务。

        ### **注意**
        暂停后资源将被释放。
      tags:
        - 共绩算力 Open API/弹性部署服务任务
        - 共绩算力 Open API/任务
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
                  type: integer
                  title: 任务id
              required:
                - task_id
              x-apifox-orders:
                - task_id
              x-apifox-ignore-properties: []
            example:
              task_id: 1
      responses:
        '200':
          x-apifox-name: 成功
          description: ''
          content:
            application/json:
              schema:
                type: object
                x-apifox-refs:
                  01KEC1JFZERRFHQZWWF0HCMD5G:
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
                    type: 'null'
                required:
                  - code
                  - message
                  - data
                x-apifox-orders:
                  - 01KEC1JFZERRFHQZWWF0HCMD5G
                  - data
                x-apifox-ignore-properties:
                  - code
                  - message
          headers: {}
      security: []
      x-apifox-folder: 共绩算力 Open API/弹性部署服务任务
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-296882601-run
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