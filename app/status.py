import const


class status:
    # リターン値の設定
    const.ok_json = {"isBase64Encoded": False,
                     "statusCode": 200}
    const.error_json = {"isBase64Encoded": False,
                        "statusCode": 500}
    const.forbidden_json = {"isBase64Encoded": False,
                            "statusCode": 403}
