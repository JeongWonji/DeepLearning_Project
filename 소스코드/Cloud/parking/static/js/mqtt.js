var host = "3.25.85.102";
var port = 9001;
var mqtt;
var dicSpace = {};
dicSpace['space1'];
dicSpace['space2'];
dicSpace['space3'];
dicSpace['space4'];
var empty = 0;
var dicCarInfo = {};
dicCarInfo['img'];
dicCarInfo['number'];
dicCarInfo['handicap'];
var state = 0;

function onConnect() {
    console.log("접속 성공");
    mqtt.subscribe("web/#");
}

function onFailure() {
    console.log("접속 실패");
}

function sendMsg(msg, topic) {
        message = new Paho.MQTT.Message(msg);
        message.destinationName = topic;
        mqtt.send(message);
};

function onMessageArrived(msg) {
    topic = msg.destinationName.split("/");
    message = msg.payloadString;

    if(topic[1] == "img") {
        document.getElementById("enterCar").src = "data:image/jpeg;base64,"+message;
    }
    else if(topic[1] == "space1") {

        spaceColor(topic[1], message);
        dicSpace['space1'] = parseInt(message);
        document.getElementById("disability").innerHTML = dicSpace['space1'] + "대";
        carSpace();
    }
    else if(topic[1] == "space2") {
        spaceColor(topic[1], message);
        dicSpace['space2'] = parseInt(message);
        carSpace();
    }
    else if(topic[1] == "space3") {
        spaceColor(topic[1], message);
        dicSpace['space3'] = parseInt(message);
        carSpace();
    }
    else if(topic[1] == "space4") {
        spaceColor(topic[1], message);
        dicSpace['space4'] = parseInt(message);
        carSpace();
    }

    else if(topic[1] == "carimg") {
        dicCarInfo['img'] = message;
        console.log("이미지 경로 왔음");
    }
    else if(topic[1] == "carnumber") {
        if (message == "NULL")
            pushNotify("error","차량번호 감지 Error",
                        "차량번호를 감지하지 못했습니다.", false);

        dicCarInfo['number'] = message;
        console.log("차 번호 왔음");

        if((dicCarInfo['img'] == undefined) && (dicCarInfo['handicap'] == undefined)) {
            $.ajax({
            type:"GET",
            url:"/numbercompare",
            data:{"number":dicCarInfo['number']},
            success: function(value) {
                if (value['result'] == "0") {// 불법차량인 경우
                    pushNotify("error","불법차량 감지","장애인 주차구역에 일반차량 진입 차량번호 : "+
                                dicCarInfo['number'], false);
                    sendMsg('fail','parking/fail');
                }else if(value['result'] == "1") {// 정상차량인 경우
                    sendMsg('ok', 'parking/ok');
                }
                dicCarInfo['number'] = undefined;
            }
            })
        }
    }
    else if(topic[1] == "carhandicap") {
        dicCarInfo['handicap'] = message;
        console.log("판별 유무 왔음");
    }

    if((dicCarInfo['img'] !== undefined) && (dicCarInfo['number'] !== undefined)
        && (dicCarInfo['handicap'] !== undefined)) {
        $.ajax({
            type:"GET",
            url:"/dataset",
            data:{"img":dicCarInfo['img'],
                "number":dicCarInfo['number'],
                "handicap":dicCarInfo['handicap']}
        })

        for (value in dicCarInfo) // 정보가 다 넘어 왔으면 초기화
            dicCarInfo[value] = undefined;
    }

    empty = 0;
    state = 0;
}

function carSpace() {
    for(value in dicSpace)
        empty += dicSpace[value];

    document.getElementById('allSpace').innerHTML = empty + "대";
}

function spaceColor(name, value) {
    if(value == "1")
        document.getElementById(name).style.backgroundColor = "Red";
    else
        document.getElementById(name).style.backgroundColor = "Blue";
}

function MQTTConnect() {
    console.log("mqtt접속"+host+"port");
    mqtt = new Paho.MQTT.Client(host,port,"javascript_client");
    var options = {
        timeout:3,
        onSuccess:onConnect,
        onFailure:onFailure,
    };
    mqtt.onMessageArrived = onMessageArrived;
    mqtt.connect(options);
};

MQTTConnect();