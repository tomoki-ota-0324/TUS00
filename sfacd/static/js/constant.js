//商圏分析側定数処理


//対象のレイヤーの標準偏差と平均を返す
function checkStdMeanNum(attrNum) {
  var mean_num;
  var std_num;
  //ここを修正するところから！！
  if (attrNum == "T000849001") { //市区町村年齢  ※　22/11/2 現在不使用
    mean_num = 892; //平均
    std_num = 1286; //標準偏差
  } else if (attrNum == "T000849002") {
    mean_num = 39;
    std_num = 61;
  } else if (attrNum == "T000849003") {
    mean_num = 42;
    std_num = 64;
  } else if (attrNum == "T000849004") {
    mean_num = 44;
    std_num = 66;
  } else if (attrNum == "T000849017") {
    mean_num = 120;
    std_num = 187;
  } else if (attrNum == "T000849018") {
    mean_num = 525;
    std_num = 772;
  } else if (attrNum == "T000849019") {
    mean_num = 245;
    std_num = 337;
  } else if (attrNum == "T000851001") { //市区町村世帯  ※　22/11/2 現在不使用
    mean_num = 344;
    std_num = 494;
  } else if (attrNum == "T000851002") {
    mean_num = 243;
    std_num = 350;
  } else if (attrNum == "T000851003") {
    mean_num = 196;
    std_num = 289;
  } else if (attrNum == "T000851004") {
    mean_num = 70;
    std_num = 103;
  } else if (attrNum == "T000851005") {
    mean_num = 96;
    std_num = 147;
  } else if (attrNum == "T000851006") {
    mean_num = 49;
    std_num = 66;
  } else if (attrNum == "T000851007") {
    mean_num = 35;
    std_num = 56;
  } else if (attrNum == "T000851008") {
    mean_num = 85;
    std_num = 132;
  } else if (attrNum == "T000851009") {
    mean_num = 157;
    std_num = 211;

    // 以下、H27年度国勢調査
  } else if (attrNum == "T000847001") { // メッシュ年齢
    mean_num = 381;
    std_num = 559;
  } else if (attrNum == "T000847004") {
    mean_num = 56;
    std_num = 82;
  } else if (attrNum == "T000847007") {
    mean_num = 330;
    std_num = 478;
  } else if (attrNum == "T000847010") {
    mean_num = 229;
    std_num = 346;
  } else if (attrNum == "T000847013") {
    mean_num = 311;
    std_num = 450;
  } else if (attrNum == "T000847016") {
    mean_num = 101;
    std_num = 143;
  } else if (attrNum == "T000847019") {
    mean_num = 49;
    std_num = 70;
  } else if (attrNum == "T000847026") { //メッシュ世帯
    mean_num = 150;
    std_num = 236;
  } else if (attrNum == "T000847034") {
    mean_num = 105;
    std_num = 156;
  } else if (attrNum == "T000847035") {
    mean_num = 88;
    std_num = 138;
  } else if (attrNum == "T000847037") {
    mean_num = 26;
    std_num = 18;
  } else if (attrNum == "T000847038") {
    mean_num = 65;
    std_num = 95;
  } else if (attrNum == "T000847039") {
    mean_num = 18;
    std_num = 38;
  } else if (attrNum == "T000847040") {
    mean_num = 17;
    std_num = 29;
  } else if (attrNum == "T000847041") {
    mean_num = 19;
    std_num = 29;

    // 以下、2020年度国勢調査
  } else if (attrNum == "T001101001") { // メッシュ年齢 人口総数
    mean_num = 378;
    std_num = 559;
  } else if (attrNum == "T001101004") { // 0～14歳
    mean_num = 54;
    std_num = 79;
  } else if (attrNum == "T001101007") { // 15歳以上総数
    mean_num = 338;
    std_num = 482;
  } else if (attrNum == "T001101010") { // 15～64歳
    mean_num = 227;
    std_num = 342;
  } else if (attrNum == "T001101016") { // 20歳以上総数
    mean_num = 320;
    std_num = 455;
  } else if (attrNum == "T001101019") { // 65歳以上総数
    mean_num = 112;
    std_num = 152;
  } else if (attrNum == "T001101022") { // 75歳以上総数
    mean_num = 58;
    std_num = 82;
  } else if (attrNum == "T001101035") { //メッシュ世帯 一般世帯総数
    mean_num = 156;
    std_num = 246;
  } else if (attrNum == "T001101043") { // 親族世帯数
    mean_num = 108;
    std_num = 157;
  } else if (attrNum == "T001101044") { // 核家族世帯数
    mean_num = 93;
    std_num = 142;
  } else if (attrNum == "T001101046") { // 6歳未満世帯員のいる一般世帯数
    mean_num = 17;
    std_num = 24;
  } else if (attrNum == "T001101047") { // 65歳以上の世帯員のいる一般世帯数
    mean_num = 71;
    std_num = 100;
  } else if (attrNum == "T001101048") { // 世帯主年齢が20～29歳の1人世帯一般世帯数
    mean_num = 19;
    std_num = 36;
  } else if (attrNum == "T001101049") { // 高齢単身一般世帯数
    mean_num = 20;
    std_num = 32;
  } else if (attrNum == "T001101050") { // 高齢夫婦のみの一般世帯数
    mean_num = 21;
    std_num = 31;
  } else {
    console.log("error in set mean_num n std_num");
  }
  return {
    std_num: std_num,
    mean_num: mean_num
  }
}

//テリトリーのカラー
function shopCodeList() {
  return {
    146010111: {
      code: 'hsl(0, 100%, 50%)',
      name: '静岡長沼店'
    },
    146010113: {
      code: 'hsl(280, 100%, 50%)',
      name: '静岡南店'
    },
    146010114: {
      code: 'hsl(200, 100%, 70%)',
      name: '清水東名店'
    },
    146010115: {
      code: 'hsl(60, 100%, 50%)',
      name: '藤枝店'
    },
    146010116: {
      code: 'hsl(50, 50%, 50%)',
      name: '焼津大富店'
    },
    146010117: {
      code: 'hsl(330, 100%, 70%)',
      name: '榛原静波店'
    },
    146010118: {
      code: 'hsl(90, 100%, 50%)',
      name: '清水桜橋店'
    },
    146010120: {
      code: 'hsl(180, 50%, 50%)',
      name: '藤枝築地店'
    },
    146010123: {
      code: 'hsl(310, 100%, 70%)',
      name: '静岡いろは店'
    },
    146010331: {
      code: 'hsl(340, 100%, 50%)',
      name: '沼津平町店'
    },
    146010332: {
      code: 'hsl(240, 100%, 40%)',
      name: '三島店'
    },
    146010333: {
      code: 'hsl(300, 100%, 50%)',
      name: '富士伝法店'
    },
    146010334: {
      code: 'hsl(30, 100%, 50%)',
      name: '富士店'
    },
    146010335: {
      code: 'hsl(80, 100%, 70%)',
      name: '伊東店'
    },
    146010336: {
      code: 'hsl(120, 50%, 50%)',
      name: '下田店'
    },
    146010337: {
      code: 'hsl(150, 100%, 50%)',
      name: '御殿場店'
    },
    146010338: {
      code: 'hsl(50, 100%, 70%)',
      name: '富士宮店'
    },
    146010339: {
      code: 'hsl(190, 100%, 70%)',
      name: '大仁店'
    },
    146010341: {
      code: 'hsl(90, 50%, 50%)',
      name: '裾野店'
    },
    146010342: {
      code: 'hsl(180, 100%, 50%)',
      name: '沼津バイパスみどりが丘店'
    },
    146010561: {
      code: 'hsl(40, 100%, 50%)',
      name: '浜松宮竹店'
    },
    146010562: {
      code: 'hsl(90, 100%, 70%)',
      name: '浜松有玉店'
    },
    146010563: {
      code: 'hsl(120, 100%, 30%)',
      name: '浜松東若林店'
    },
    146010564: {
      code: 'hsl(210, 100%, 50%)',
      name: '磐田店'
    },
    146010565: {
      code: 'hsl(30, 100%, 70%)',
      name: '掛川店'
    },
    146010566: {
      code: 'hsl(240, 100%, 70%)',
      name: '浜北店'
    },
    146010567: {
      code: 'hsl(320, 100%, 50%)',
      name: '浜松志都呂店'
    },
    146010568: {
      code: 'hsl(270, 100%, 50%)',
      name: '小笠店'
    },
    146010569: {
      code: 'hsl(0, 50%, 50%)',
      name: '浜松初生店'
    },
    146010570: {
      code: 'hsl(120, 100%, 30%)',
      name: '袋井店'
    },
    146999999: {
      code: 'hsl(0, 0%, 0%)',
      name: '不明'
    }
  }
}

//数字で帰ってくる凡例を文字に返る 不明と入力がNoneのものは全て不明として表示
function getLegendFromNum(legendName, marker_color) {
  var legend;
  if (marker_color == "sex") {
    if (legendName == "1") {
      legend = "男性";
    } else if (legendName == "2") {
      legend = "女性";
    } else if (legendName == "3") {
      legend = "法人";
    // } else if (legendName == "9") {
    //   legend = "不明";
    } else {
      legend = "不明"
    }
  } else if (marker_color == "sale_flg") {
    if (legendName == "1") {
      legend = "新車";
    } else if (legendName == "2") {
      legend = "中古車";
    } else {
      legend = "不明";
    }
  } else if (marker_color == "car_fixed_kind" || marker_color == "customer_fixed_kind") {
    if (legendName == "0") {
      legend = "一般客";
    } else if (legendName == "1") {
      legend = "新車客";
    } else if (legendName == "2") {
      legend = "準固定客";
    } else if (legendName == "3") {
      legend = "固定客";
    } else {
      legend = "不明";
    }
  }
  console.log(legend);
  return legend;
}

// 市区町村／町丁字等別, 行政区域別年齢統計の分類の基準値を辞書で返す
function getFeatureColorRange(attr_num) {
  var colorRange;
  if (currentLayer == ageLayer) { //市区町村町丁字別人口
    if (attr_num == "総数_s") {
      //自然なブレイク　閾値

      // H27国勢調査設定値
      // colorRange = {
      //   first: 726,
      //   second: 2101,
      //   third: 4594,
      //   fourth: 8769
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 696,
        second: 2057,
        third: 4399,
        fourth: 7770
      }
    } else if (attr_num == "0~9歳") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 59,
      //   second: 183,
      //   third: 442,
      //   fourth: 948
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 58,
        second: 185,
        third: 428,
        fourth: 805
      }
    } else if (attr_num == "10歳代") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 60,
      //   second: 179,
      //   third: 393,
      //   fourth: 769
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 59,
        second: 179,
        third: 399,
        fourth: 781
      }
    } else if (attr_num == "20歳代") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 66,
      //   second: 201,
      //   third: 466,
      //   fourth: 1068
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 63,
        second: 197,
        third: 443,
        fourth: 906
      }
    } else if (attr_num == "30歳代") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 86,
      //   second: 266,
      //   third: 601,
      //   fourth: 1149
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 80,
        second: 240,
        third: 491,
        fourth: 874
      }
    } else if (attr_num == "40歳代") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 104,
      //   second: 306,
      //   third: 629,
      //   fourth: 1185
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 102,
        second: 313,
        third: 685,
        fourth: 1306
      }
    } else if (attr_num == "50歳代") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 77,
      //   second: 206,
      //   third: 435,
      //   fourth: 820
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 91,
        second: 269,
        third: 561,
        fourth: 1018
      }
    } else if (attr_num == "60歳代") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 94,
      //   second: 248,
      //   third: 520,
      //   fourth: 1001
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 84,
        second: 226,
        third: 461,
        fourth: 837
      }
    } else if (attr_num == "15歳未満") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 90,
      //   second: 282,
      //   third: 659,
      //   fourth: 1318
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 90,
        second: 280,
        third: 624,
        fourth: 1242
      }
    } else if (attr_num == "15~64歳") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 402,
      //   second: 1156,
      //   third: 2459,
      //   fourth: 4362
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 405,
        second: 1208,
        third: 2554,
        fourth: 4451
      }
    } else if (attr_num == "65歳以上") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 194,
      //   second: 552,
      //   third: 1163,
      //   fourth: 2093
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 204,
        second: 571,
        third: 1222,
        fourth: 2245
      }
    }
  } else if (currentLayer == setaiLayer) { //市区町村別世帯
    if (attr_num == "一般世帯総数") {
      //自然なブレイク 閾値

      // H27国勢調査設定値
      // colorRange = {
      //   first: 272,
      //   second: 775,
      //   third: 1691,
      //   fourth: 3312
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 289,
        second: 831,
        third: 1720,
        fourth: 3116
      }
    } else if (attr_num == "親族世帯数") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 188,
      //   second: 569,
      //   third: 1210,
      //   fourth: 2164
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 184,
        second: 531,
        third: 1134,
        fourth: 2086
      }
    } else if (attr_num == "核家族世帯数") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 169,
      //   second: 487,
      //   third: 1088,
      //   fourth: 2020
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 160,
        second: 468,
        third: 1005,
        fourth: 1863
      }
    } else if (attr_num == "核家族の内夫婦のみ世帯数") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 54,
      //   second: 151,
      //   third: 341,
      //   fourth: 869
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 58,
        second: 167,
        third: 360,
        fourth: 754
      }
    } else if (attr_num == "核家族の内夫婦と子供世帯数") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 78,
      //   second: 232,
      //   third: 511,
      //   fourth: 984
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 75,
        second: 227,
        third: 498,
        fourth: 952
      }
    } else if (attr_num == "核家族以外の世帯数") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 32,
      //   second: 86,
      //   third: 182,
      //   fourth: 332
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 29,
        second: 82,
        third: 170,
        fourth: 311
      }
    } else if (attr_num == "6歳未満世帯員のいる一般世帯数") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 30,
      //   second: 97,
      //   third: 216,
      //   fourth: 406
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 26,
        second: 82,
        third: 189,
        fourth: 354
      }
    } else if (attr_num == "18歳未満世帯員のいる一般世帯数") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 65,
      //   second: 205,
      //   third: 463,
      //   fourth: 949
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 62,
        second: 193,
        third: 435,
        fourth: 899
      }
    } else if (attr_num == "65歳以上世帯員のいる一般世帯数") {
      // H27国勢調査設定値
      // colorRange = {
      //   first: 112,
      //   second: 315,
      //   third: 692,
      //   fourth: 1353
      // }

      // 2020年国勢調査設定値
      colorRange = {
        first: 123,
        second: 333,
        third: 688,
        fourth: 1256
      }
    }
  } else if (currentLayer == perAgeTotalLayer) { //9段階別年齢人口数
    if (attr_num == "総数_g") {
      //自然なブレイク 閾値

      // H30年度統計
      // colorRange = {
      //   first: 11930,
      //   second: 44392,
      //   third: 100538,
      //   fourth: 166504
      // }

      // R3年度統計
      colorRange = {
        first: 11306,
        second: 43241,
        third: 99451,
        fourth: 165743
      }
    } else if (attr_num == "0~6歳") {
      // H30年度統計
      // colorRange = {
      //   first: 326,
      //   second: 1038,
      //   third: 3338,
      //   fourth: 8378
      // }

      // R3年度統計
      colorRange = {
        first: 236,
        second: 916,
        third: 3052,
        fourth: 7637
      }
    } else if (attr_num == "7~12歳") {
      // H30年度統計
      // colorRange = {
      //   first: 399,
      //   second: 1822,
      //   third: 5186,
      //   fourth: 9350
      // }

      // R3年度統計
      colorRange = {
        first: 352,
        second: 1553,
        third: 4640,
        fourth: 7995
      }
    } else if (attr_num == "13~19歳") {
      // H30年度統計
      // colorRange = {
      //   first: 611,
      //   second: 2379,
      //   third: 6322,
      //   fourth: 9740
      // }

      // R3年度統計
      colorRange = {
        first: 483,
        second: 1976,
        third: 6093,
        fourth: 11082
      }
    } else if (attr_num == "20歳代") {
      // H30年度統計
      // colorRange = {
      //   first: 1308,
      //   second: 5064,
      //   third: 11682,
      //   fourth: 15005
      // }

      // R3年度統計
      colorRange = {
        first: 610,
        second: 2122,
        third: 7660,
        fourth: 14967
      }
    } else if (attr_num == "30歳代") {
      // H30年度統計
      // colorRange = {
      //   first: 766,
      //   second: 2408,
      //   third: 6632,
      //   fourth: 15915
      // }

      // R3年度統計
      colorRange = {
        first: 643,
        second: 2193,
        third: 6220,
        fourth: 15139
      }
    } else if (attr_num == "40歳代") {
      // H30年度統計
      // colorRange = {
      //   first: 1409,
      //   second: 5334,
      //   third: 13374,
      //   fourth: 23989
      // }

      // R3年度統計
      colorRange = {
        first: 1167,
        second: 4723,
        third: 20290,
        fourth: 34492
      }
    } else if (attr_num == "50歳代") {
      // H30年度統計
      // colorRange = {
      //   first: 1482,
      //   second: 5760,
      //   third: 12546,
      //   fourth: 19873
      // }

      // R3年度統計
      colorRange = {
        first: 1988,
        second: 5920,
        third: 13406,
        fourth: 20665
      }
    } else if (attr_num == "60歳代") {
      // H30年度統計
      // colorRange = {
      //   first: 2729,
      //   second: 7059,
      //   third: 14789,
      //   fourth: 23914
      // }

      // R3年度統計
      colorRange = {
        first: 2434,
        second: 6432,
        third: 13015,
        fourth: 21048
      }
    } else if (attr_num == "70歳~") {
      // H30年度統計
      // colorRange = {
      //   first: 4357,
      //   second: 9947,
      //   third: 18922,
      //   fourth: 33418
      // }

      // R3年度統計
      colorRange = {
        first: 4574,
        second: 13509,
        third: 26537,
        fourth: 36830
      }
    }
  } else if (currentLayer == perAgeDeviationLayer) { //特定年齢の全県民に対する地域内の特定年齢に対する偏差値  ※　22/11/2 現在不使用
    if (attr_num == "0-12歳") {
      //等間隔分類 基準値
      colorRange = {
        first: 36.478,
        second: 44.508,
        third: 52.538,
        fourth: 60.568
      }
    } else if (attr_num == "0歳") {
      colorRange = {
        first: 38.978,
        second: 48.684,
        third: 58.390,
        fourth: 68.096
      }
    } else if (attr_num == "1歳") {
      colorRange = {
        first: 35.334,
        second: 43.979,
        third: 52.625,
        fourth: 61.271
      }
    } else if (attr_num == "2歳") {
      colorRange = {
        first: 37.066,
        second: 45.711,
        third: 54.355,
        fourth: 63.000
      }
    } else if (attr_num == "3歳") {
      colorRange = {
        first: 35.156,
        second: 43.170,
        third: 51.185,
        fourth: 59.200
      }
    } else if (attr_num == "4歳") {
      colorRange = {
        first: 33.903,
        second: 42.183,
        third: 50.462,
        fourth: 58.742
      }
    } else if (attr_num == "5歳") {
      colorRange = {
        first: 36.575,
        second: 44.792,
        third: 53.010,
        fourth: 61.227
      }
    } else if (attr_num == "6歳") {
      colorRange = {
        first: 35.736,
        second: 43.613,
        third: 51.489,
        fourth: 59.365
      }
    } else if (attr_num == "7歳") {
      colorRange = {
        first: 36.764,
        second: 45.058,
        third: 53.352,
        fourth: 61.646
      }
    } else if (attr_num == "8歳") {
      colorRange = {
        first: 33.384,
        second: 41.347,
        third: 49.310,
        fourth: 57.273
      }
    } else if (attr_num == "9歳") {
      colorRange = {
        first: 33.654,
        second: 42.307,
        third: 50.961,
        fourth: 59.614
      }
    } else if (attr_num == "10歳") {
      colorRange = {
        first: 31.998,
        second: 40.023,
        third: 48.048,
        fourth: 56.073
      }
    } else if (attr_num == "11歳") {
      colorRange = {
        first: 31.998,
        second: 40.023,
        third: 48.048,
        fourth: 56.073
      }
    } else if (attr_num == "12歳") {
      colorRange = {
        first: 29.850,
        second: 38.615,
        third: 47.380,
        fourth: 56.145
      }
    }
  } else if (currentLayer == perAgeRatioLayer) { //地域内人口に対する選択年齢人口の割合  ※　22/11/2 現在不使用
    if (attr_num == "0-12歳") {
      //等間隔分類 基準値
      colorRange = {
        first: 7.057,
        second: 8.808,
        third: 10.560,
        fourth: 12.311
      }
    } else if (attr_num == "0歳") {
      colorRange = {
        first: 0.4211,
        second: 0.6141,
        third: 0.8072,
        fourth: 1.0003
      }
    } else if (attr_num == "1歳") {
      colorRange = {
        first: 0.3738,
        second: 0.5492,
        third: 0.7245,
        fourth: 0.8998
      }
    } else if (attr_num == "2歳") {
      colorRange = {
        first: 0.4623,
        second: 0.6335,
        third: 0.8046,
        fourth: 0.9758
      }
    } else if (attr_num == "3歳") {
      colorRange = {
        first: 0.4503,
        second: 0.5937,
        third: 0.7372,
        fourth: 0.8807
      }
    } else if (attr_num == "4歳") {
      colorRange = {
        first: 0.4300,
        second: 0.5820,
        third: 0.7340,
        fourth: 0.8860
      }
    } else if (attr_num == "5歳") {
      colorRange = {
        first: 0.5286,
        second: 0.6735,
        third: 0.8183,
        fourth: 0.9631
      }
    } else if (attr_num == "6歳") {
      colorRange = {
        first: 0.5448,
        second: 0.6814,
        third: 0.8181,
        fourth: 0.9547
      }
    } else if (attr_num == "7歳") {
      colorRange = {
        first: 0.5771,
        second: 0.7144,
        third: 0.8517,
        fourth: 0.9890
      }
    } else if (attr_num == "8歳") {
      colorRange = {
        first: 0.5276,
        second: 0.6599,
        third: 0.7923,
        fourth: 0.9247
      }
    } else if (attr_num == "9歳") {
      colorRange = {
        first: 0.5534,
        second: 0.6966,
        third: 0.8398,
        fourth: 0.9830
      }
    } else if (attr_num == "10歳") {
      colorRange = {
        first: 0.5848,
        second: 0.7039,
        third: 0.8230,
        fourth: 0.9421
      }
    } else if (attr_num == "11歳") {
      colorRange = {
        first: 0.5915,
        second: 0.7118,
        third: 0.8322,
        fourth: 0.9525
      }
    } else if (attr_num == "12歳") {
      colorRange = {
        first: 0.5857,
        second: 0.7030,
        third: 0.8203,
        fourth: 0.9377
      }
    }
  }
  return colorRange;
}

//ポリゴンの数値の表示の際の単位を取得
function getUnitPropertyNum(currentLayer) {
  var unit;
  if (currentLayer == ageLayer || currentLayer == meshAgeLayer || currentLayer == perAgeTotalLayer) {
    unit = "人";
  } else if (currentLayer == setaiLayer || currentLayer == meshSetaiLayer) {
    unit = "世帯";
  } else if (currentLayer == perAgeRatioLayer) {
    unit = "%";
  } else if (currentLayer == perAgeDeviationLayer) {
    unit = "偏差値";
  } else {
    unit = "";
  }
  return unit;
}

//テキストを渡すとテキストの入ったdiv要素として返す: tag string 要素名 例：div, h3、text string テキスト
function createDiv(tag, text) {
  var div = document.createElement(tag);
  div.innerText = text;
  return div;
}

