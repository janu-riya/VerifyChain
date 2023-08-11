import http.client

conn = http.client.HTTPSConnection("apisetu.gov.in")

payload = "{\"txnId\":\"f7f1469c-29b0-4325-9dfc-c567200a70f7\",\"format\":\"xml\",\"certificateParameters\":{\"dlno\":\"TN0119920009646. As per your Driving License.\",\"UID\":\"123412341234\",\"FullName\":\"Sunil Kumar\",\"DOB\":\"31-12-1980\"},\"consentArtifact\":{\"consent\":{\"consentId\":\"ea9c43aa-7f5a-4bf3-a0be-e1caa24737ba\",\"timestamp\":\"2019-08-24T14:15:22Z\",\"dataConsumer\":{\"id\":\"string\"},\"dataProvider\":{\"id\":\"string\"},\"purpose\":{\"description\":\"string\"},\"user\":{\"idType\":\"string\",\"idNumber\":\"string\",\"mobile\":\"string\",\"email\":\"string\"},\"data\":{\"id\":\"string\"},\"permission\":{\"access\":\"string\",\"dateRange\":{\"from\":\"2019-08-24T14:15:22Z\",\"to\":\"2019-08-24T14:15:22Z\"},\"frequency\":{\"unit\":\"string\",\"value\":0,\"repeats\":0}}},\"signature\":{\"signature\":\"string\"}}}"

headers = {
    'X-APISETU-CLIENTID': "com.securekloud",
    'content-type': "application/json"
    }

conn.request("POST", "/certificate/v3/transportkl/drvlc", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8")),
