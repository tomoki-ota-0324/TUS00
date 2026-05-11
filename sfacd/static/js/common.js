//オブジェクト同士が同じかどうか比較し同じならtrueを返す 例: {aaa: "bbb"} == {aaa: "bbb"}　通常の比較であればfalse, 以下のfunctionではture
function checkObject(a, b) {
  if (JSON.stringify(a) == JSON.stringify(b)) {
    return true;
  } else {
    return false;
  }
}

//引数リストの中に引数文字列が存在するかチェック
function checkCurrent(list_box, layer) {
  if (list_box.indexOf(layer) >= 0) {
    return true;
  }
  if (list_box.indexOf(layer) == -1) {
    return false;
  }
}

//オブジェクトの中味が空か判別　空ならTrue
function isEmpty(obj){
  return !Object.keys(obj).length;
}

//緯度経度から対応するメッシュの算出
function calcMeshCode(lon, lat, resolution){
  var p = Math.floor((lat * 60) / 40);
  var a = (lat * 60) % 40;
  var q = Math.floor(a / 5);
  var b = a % 5;
  var r = Math.floor((b * 60) / 30);
  var c = (b * 60) % 30;
  var s = Math.floor(c / 15);
  var d = c % 15;
  var t = Math.floor(d / 7.5);

  var u = Math.floor(lon - 100);
  var f = lon - 100 - u;
  var v = Math.floor((f * 60) / 7.5);
  var g = (f * 60) % 7.5;
  var w = Math.floor((g * 60) / 45);
  var h = (g * 60) % 45;
  var x = Math.floor(h / 22.5);
  var i = h % 22.5;
  var y = Math.floor(i / 11.25);

  var m = (s * 2) + (x + 1);
  var n = (t * 2) + (y + 1);

  //1次メッシュ
  var mesh = "" + p + u;
  //2次メッシュ
  if(resolution >= 2){
    mesh = mesh + q + v;
    //3次メッシュ
    if(resolution >= 3){
      mesh = mesh + r + w;
      // 1/2メッシュ
      if(resolution >= 4){
        mesh = mesh + m;
        // 1/4メッシュ
        if(resolution >=5){
          mesh = mesh + n;
        }
      }
    }
  }
  return mesh;
}

//マーカー色ごとのカウントCKにて使用 デバックにて使用
function checkMarkerCount(c_markers, path) {
  var count = 0;
  $.each(c_markers, function(index) {
    if (this.icon.url == path) {
      count = count + 1;
    } else {
      return true; //次へ継続 continue
    }
  });
  console.log("カウント:" + path + " 数：" + count);
}

// 指定された秒数だけ待つ deferred
function wait(sec) {
  var d = $.Deferred();
  setTimeout(function() {
      d.resolve();
  }, sec * 1000);
  return d.promise();
}

