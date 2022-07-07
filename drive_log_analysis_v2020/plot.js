var map;
var marker;

function getCSV(){
  var req = new XMLHttpRequest(); // HTTPでファイルを読み込むためのXMLHttpRrequestオブジェクトを生成
  req.open("get", "coords.csv", true); // アクセスするファイルを指定
  req.send(null); // HTTPリクエストの発行

  // レスポンスが返ってきたらconvertCSVtoArray()を呼ぶ
  req.onload = function(){
	   var result = convertCSVtoArray(req.responseText); // 渡されるのは読み込んだCSVデータ
     return result;
  }

}

function convertCSVtoArray(str){ // 読み込んだCSVデータが文字列として渡される
  var result = []; // 最終的な二次元配列を入れるための配列
  var tmp = str.split("\n"); // 改行を区切り文字として行を要素とした配列を生成

  // 各行ごとにカンマで区切った文字列を要素とした二次元配列を生成
  for(var i=0;i<tmp.length;++i){
    result[i] = tmp[i].split(',');
  }

  return result;
}

function initMap() {

  var result = getCSV();

  var center = {
    lat: result[0][0], // 緯度
    lng: result[0][1] // 経度
  };

  map = new google.maps.Map(document.getElementById('map'), { // #mapに地図を埋め込む
    center: center,
    zoom: 19 // 地図のズームを指定
  });

  marker = new google.maps.Marker({ // マーカーの追加
    position: center, // マーカーを立てる位置を指定
    map: map // マーカーを立てる地図を指定
  });
}
