# 镜像预热任务可用集群列表

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  version: 1.0.0
paths:
  /api/task/image_preheat/get_regions:
    get:
      summary: 镜像预热任务可用集群列表
      deprecated: false
      description: >-
        | 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |

        | --- | --- | --- | --- |

        | v1.0.0 | - | 否 | 是 |


        ### **描述**

        获取镜像预热任务可预热集群列表

        加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)
      tags:
        - 共绩算力 Open API/镜像预热任务
        - 共绩算力 Open API/任务
      parameters:
        - name: token
          in: header
          description: 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。
          required: true
          example: a69abd35-1df0-4c21-9c2b-82a20a72d3b2-20260417200925
          schema:
            type: string
        - name: timestamp
          in: header
          description: 时间戳
          required: true
          example: '{{$date.millisecondsTimestamp}}'
          schema:
            type: integer
        - name: version
          in: header
          description: 固定值
          required: true
          example: 1.0.0
          schema:
            type: string
        - name: sign_str
          in: header
          description: 如果token为简易模式则无需填写此字段
          required: false
          example: ''
          schema:
            type: string
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: object
                    properties:
                      regions:
                        type: array
                        items:
                          type: object
                          properties:
                            region:
                              type: string
                            region_name:
                              type: string
                          required:
                            - region
                            - region_name
                          x-apifox-orders:
                            - region
                            - region_name
                    required:
                      - regions
                    x-apifox-orders:
                      - regions
                required:
                  - data
                x-apifox-orders:
                  - 01KV0A4T77BBWDRS8VG7SWKR70
                  - data
                x-apifox-refs:
                  01KV0A4T77BBWDRS8VG7SWKR70:
                    $ref: '#/components/schemas/IResponse'
              example:
                code: '0000'
                message: success
                data:
                  regions:
                    - region: bj-jxq-t1
                      region_name: 北京酒仙桥t1
                    - region: bj-jxq-t2
                      region_name: 北京酒仙桥t2
                    - region: tengxun-sheq-t1
                      region_name: 腾讯上海二区T1-测试
                    - region: warmup-test
                      region_name: 福建4
          headers: {}
          x-apifox-name: 成功
          x-apifox-ordering: 0
      security: []
      x-apifox-folder: 共绩算力 Open API/镜像预热任务
      x-apifox-status: developing
      x-run-in-apifox: https://app.apifox.com/web/project/3025695/apis/api-483003688-run
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
  responses: {}
  securitySchemes: {}
servers: []
security: []

```