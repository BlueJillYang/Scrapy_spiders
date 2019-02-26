function stringToHex(str) {
    var val = "";
    for (var i = 0; i < str.length; i++) {
        if (val == "") val = str.charCodeAt(i).toString(16);
        else val += str.charCodeAt(i).toString(16);
    }
    return val;
}
function YunSuoAutoJump(url) {
    var dict_info = {};
    var screen = {'width': 1200, 'height': 800};
    var width = screen.width;
    var height = screen.height;
    var screendate = width + "," + height;
    var curlocation = url;
    if ( - 1 == curlocation.indexOf("security_verify_")) {
        var str_cookie = stringToHex(url);
        dict_info['str_cookie'] = str_cookie;
    }
    var another_href = "/?security_verify_data=" + stringToHex(screendate);
    dict_info['another_href'] = another_href;
    return dict_info;
}

