a = 'eJxdjk1vgjAYx79LryPQqoCQ7CAvE8rQiYCaZQdEsAgtKp0Ol333dZm7LHmS/9vv8HyCs78DJoLQgFACl+IMTIBkKGtAArwTiwZHuirGoQFVCeT/Ok2XwPacOsB8HY2gpA7R208RifyKBmMo6QP4Jv1azRB2MBL3w/gCAYTzY2cqStbJtKj4e8bkvKWK8B2pFPECECiNBSq0vmt2V/6XQ/GzYLtqz4Qr8LU5bOHsepgsyLog+Zxt7E3t13vukk3cTkPHtdTe1wsyjqjvp9T2HHdtPTVkcUmMF32wI3Zxm0+XybRXJp4allZxsEukhMZtjIntOls6mV1o0NQRvm7KRN9qodXi5TOx8nkUsVnDeKCdaL/0jvbNWQf+pTrl56bCfaoG7YJ80Hip6d0Crg6qN+4SGj/nxnDqdswOPtyYWXpvsN08q28seVGSFrV45zhZuZqleJhxisrsAaInjHm5t9tY9dDk8RF8fQMGRInC'
# a = 'eJxNjl1vqkAYhP/L3pbALvK1Jr2QjwpL0YpgNY0XiOAiLLSy1eLJ%KdiDMYIQQyiBc3ECY4BkKBtAArwXjQE1U8d4pMoqNg3DsCSQ/y2w9lvsTisXjF9eNArfVkDC6tq4m5MIBBAOX/tx4qS9TIrKv6etXLeMUX4nlaKmAMEyhKBCq2/NftW/wdnlOFnQdUHzebtxNnVQH7hHN0k3jVzP1ofALKgVsyBYMcd3vbX90NDFOcVPprqnTnGdGoR6njujk1mZxY2dUwumzI1d0Zkd2T5SO18HsftrGl5aLyxYem/Old3HQbn6i0/NH3rT5lyWOOR1Ovb53ww0ta2xxwu59n9bVNn5S0Qx3Zu25WPs9WZJRxhsrsDqIHQnh5cL==='
b = b'{"rId":100900,"ver":"1.0.6","ts":1604759003905,"cts":1604759003967,"brVD":[440,531],"brR":[[1280,720],[1280,690],24,24],"bI":["https://as.meituan.com/meishi/",""],"mT":[],"kT":[],"aT":[],"tT":[],"aM":"","sign":"eJwljb0NwjAQhXehcOnYCYkIkgtEhYToGMDEB5yI7eh8RmIIVmCHDEXBFlhQvU9P72dhCezOGSUGy/AH5MfBejCf1/M9z8JhCEDbmANvmKlkRJwYfU7b6MBoJSLhBcORRnNlntK6qmySHpCzDXKIviqcrliJyV5KoQhxmTS67sQ0Wj5H8sUmTLc93GEsnCKxETnB7y9ndOakznUP/Uo1oJdDDafWNVJ3atm1fa+01FJJtfgCoT5H1A=="}'


d = 'eJxdj11vgjAUhv9Lb2ekVQFZsgv5mFCGTgSnES8QwSK0bNLpcNl/X2HJliw5F895zvsmLfiMwNk5ROAeQahB2IvAJT2LNQKoD/tKBIThdXtX4EiVRWSoQVnI5L9VVGH355Up9HY0gj15iHad8luzRYMx7KkDuOv9oKIJHIzEdCmnDUWAcP5a30tSXPdpmvP3mPWTikqCa5JL3XMi0BZo0BZaKn4p/iX+57zuN12zzo+s21J8LU97OLueJguyTkkyZxtjUzjFkVtkE1RTz7R0uXHUlIx96jgratimtdYfS7K4hNqzOjgQI73Np8tw2kgTW/YyPT0ZGZI87TbGxLDMPZ3MLtQtCx9fN1mo7hVPr/DyiejJ3PfZrGTcVd5os7RfjZu5dp1L/pacyxw3K9mtFuSDBktFrRfw5STb4zqkwVOiDadWzQz3wwqYrjYaO8zj4sbCZymsUIUPphlnL7MVHsacoiy+g+gRY54djSqQbTR5eIjAF/gGQBCW9g=='
import zlib, base64, time, json

def decode_token(token):
    # base64解码
    token_decode = base64.b64decode(token.encode())
    # 二进制解压
    token_string = zlib.decompress(token_decode)
    return token_string

def encode_token(token):
    # base64解码
    # token_decode = zlib.compress(
    #         bytes(json.dumps(token, separators=(',', ':'), ensure_ascii=False), encoding="utf8"))
    # token_string = str(base64.b64encode(token_decode), encoding="utf8")
    # 二进制解压
    
    token_decode = zlib.compress(token)
    token_string = str(base64.b64encode(token_decode))
    return token_string


def join_sign():
    # 参数
    # b'"areaId=0&cateId=0&cityName=\xe9\x9e\x8d\xe5\xb1\xb1&
    # dinnerCountAttrId=&optimusCode=10&originUrl=https:/
    # /as.meituan.com/meishi/&page=1&partner=126&platform=1&r
    # iskLevel=1&sort=&userId=&uuid=b0f29e9803e14c2eb5d3.1604659901.1.0.0"'
    areaId = str(0)
    # cityName = '\xe9\x9e\x8d\xe5\xb1\xb1'
    cityName = '鞍山'
    originUrl = 'https://as.meituan.com/meishi/'
    page = str(1)
    uuid = 'b0f29e9803e14c2eb5d3.1604659901.1.0.0'
    sign = 'areaId=' + areaId + '&cateId=0&cityName=' + cityName + '&dinnerCountAttrId=&optimusCode=10&originUrl=' + originUrl + '&page=' + page + '&partner=126&platform=1&riskLevel=1&sort=&userId=&uuid=' + uuid
    # _str = sign.format(areaId=areaId, cityName=cityName, originUrl=originUrl, page=page,
    #                     uuid=uuid)
    sign = base64.b64encode(zlib.compress(bytes(json.dumps(sign, ensure_ascii=False), encoding="utf8")))
    sign = str(sign, encoding="utf8")
    return sign
    
def test():
    a = 'eJwljb0NwjAQhXehcOnYCYkIkgtEhYToGMDEB5yI7eh8RmIIVmCHDEXBFlhQvU9P72dhCezOGSUGy/AH5MfBejCf1/M9z8JhCEDbmANvmKlkRJwYfU7b6MBoJSLhBcORRnNlntK6qmySHpCzDXKIviqcrliJyV5KoQhxmTS67sQ0Wj5H8sUmTLc93GEsnCKxETnB7y9ndOakznUP/Uo1oJdDDafWNVJ3atm1fa+01FJJtfgCoT5H1A=='
    token_decode = decode_token(a)
    print(token_decode)
# print(decode_token(a))
# print(encode_token(b))
test()
# eJwljb0NwjAQhXehcOnYASKC5AJRISE6BjDxASdiOzqfkRiCFegoKFkhLIYF1fv09H4mlsBunFGiswx/QL7trAfzeY2P8f55ju/xLRyGALSOOfCKmUpSxIHR57SODoxWIhKeMOypN2fmIS2ryibpATnbILvoq8LpjJUY7KkUihCXSaPrRgy95WMkX2zCdNnCFfrCKRIbkRP8/nJGZw7qWLfQLtQU9Kyr4TB3U6kbNWvmbau01FJJNfkCxepL4g==
# print(join_sign())