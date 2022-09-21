function moterUpDown(msg, topic) {
    sendMsg(msg, topic);
    if (msg == 'servo_on')
        pushNotify("success","바리게이트 제어","바리게이트 올리기 완료", true);
    else if(msg == 'servo_off')
        pushNotify("success","바리게이트 제어","바리게이트 내리기 완료", true);
}