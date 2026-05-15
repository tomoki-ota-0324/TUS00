//以下作成HTML内の処理 -------------------------------------------------------------

//顧客マーカーメニューの商圏エリアを切り替えた時
var circleArea =
  '<div class="row" id="select_area">' +
    '<label class="col-sm-3 col-form-label">同心円距離範囲</label>' +
    '<div class="col-sm-9">' +
      '<div class="form-check form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="checkbox" name="areaBox" value="3000" checked>' +
          '<span class="form-check-sign"></span>' +
          '半径3Km' +
        ' </label>' +
      '</div>' +
      '<div class="form-check form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="checkbox" name="areaBox" value="6000">' +
          '<span class="form-check-sign"></span>' +
          '半径6Km' +
        '</label>' +
      '</div>' +
      '<div class="form-check form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="checkbox" name="areaBox" value="10000">' +
          '<span class="form-check-sign"></span>' +
          '半径10Km' +
        '</label>' +
      '</div>' +
    '</div>' +
  '</div>'
;

var driveArea =
  '<div class="row" id="select_area">' +
    '<label class="col-sm-3 col-form-label">車両運転時到達圏</label>' +
    '<div class="col-sm-9">' +
      '<div class="form-check form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="checkbox" name="driveTimeArea" value="15min" checked>' +
          '<span class="form-check-sign"></span>' +
          '15分' +
        '</label>' +
      '</div>' +
      '<div class="form-check form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="checkbox" name="driveTimeArea" value="30min">' +
          '<span class="form-check-sign"></span>' +
          '30分' +
        '</label>' +
      '</div>' +
    '</div>' +
  '</div>'
;

//レイヤーの選択を切り替えた時
var dataSelect =
  '<div class="row">' +
    '<label class="col-sm-3 col-form-label">統計データの選択</label>' +
    '<div class="col-sm-9 checkbox-radios">' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="dataRadioz" id="dataRadios1" value="1"> 年齢別' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="dataRadioz" id="dataRadios2" value="2"> 世帯別' +
          '<span class="form-check-sign"></span></label>' +
      '</div>' +
    '</div>' +
  '</div>'
;

var hideSelect =
  '<div class="row">' +
    '<input type="checkbox" name="dataRadioz" value="1" style="display: none;" checked>' +
  '</div>'
;

var ageSelect =
  '<div class="row">' +
    '<label class="col-sm-3 col-form-label">統計データの選択</label>' +
    '<div class="col-sm-9 checkbox-radios">' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="dataRadioz" id="dataRadios1" value="1"> 9段階別年齢人口総数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
    '</div>' +
  '</div>'
;

//統計の選択を切り替えた時
var cityAgeSelect =
  '<div class="row">' +
    '<label class="col-sm-3 col-form-label">属性の選択</label>' +
    '<div class="col-sm-9 checkbox-radios">' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios1" value="総数_s"> 人口総数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios2" value="0~9歳"> 0~9歳' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios3" value="10歳代"> 10歳代' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios4" value="20歳代"> 20歳代' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios5" value="30歳代"> 30歳代' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios6" value="40歳代"> 40歳代' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios7" value="50歳代"> 50歳代' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios8" value="60歳代"> 60歳代' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios9" value="15歳未満"> 15歳未満' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios10" value="15~64歳"> 15~64歳' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios11" value="65歳以上"> 65歳以上' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
    '</div>' +
  '</div>'
;

var citySetaiSelect =
  '<div class="row">' +
    '<label class="col-sm-3 col-form-label">属性の選択</label>' +
    '<div class="col-sm-9 checkbox-radios">' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios1" value="一般世帯総数"> 一般世帯総数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios2" value="親族世帯数"> 親族世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios3" value="核家族世帯数"> 核家族世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios4" value="核家族の内夫婦のみ世帯数"> 核家族の内夫婦のみ世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios5" value="核家族の内夫婦と子供世帯数"> 核家族の内夫婦と子供世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios6" value="核家族以外の世帯数"> 核家族以外の世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios7" value="6歳未満世帯員のいる一般世帯数"> 6歳未満世帯員のいる一般世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios8" value="18歳未満世帯員のいる一般世帯数"> 18歳未満世帯員のいる一般世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios9" value="65歳以上世帯員のいる一般世帯数"> 65歳以上世帯員のいる一般世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
    '</div>' +
  '</div>'
;

// H27年度国勢調査選択肢
// var meshAgeSelect =
//   '<div class="row">' +
//     '<label class="col-sm-3 col-form-label">属性の選択</label>' +
//     '<div class="col-sm-9 checkbox-radios">' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios1" value="T000847001"> 人口総数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios2" value="T000847004"> 0～14歳' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios3" value="T000847007"> 15歳以上総数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios4" value="T000847010"> 15～64歳' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios5" value="T000847013"> 20歳以上総数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios6" value="T000847016"> 65歳以上総数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios7" value="T000847019"> 75歳以上総数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//     '</div>' +
//   '</div>'
// ;

// var meshSetaiSelect =
//   '<div class="row">' +
//     '<label class="col-sm-3 col-form-label">属性の選択</label>' +
//     '<div class="col-sm-9 checkbox-radios">' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios1" value="T000847026"> 一般世帯総数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios2" value="T000847034"> 親族世帯数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios3" value="T000847035"> 核家族世帯数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios4" value="T000847037"> 6歳未満世帯員のいる一般世帯数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios5" value="T000847038"> 65歳以上の世帯員のいる一般世帯数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios6" value="T000847039"> 世帯主年齢が20～29歳の1人世帯一般世帯数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios7" value="T000847040"> 高齢単身一般世帯数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//       '<div class="form-check-radio form-check-inline">' +
//         '<label class="form-check-label">' +
//           '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios8" value="T000847041"> 高齢夫婦のみの一般世帯数' +
//           '<span class="form-check-sign"></span>' +
//         '</label>' +
//       '</div>' +
//     '</div>' +
//   '</div>'
// ;

// 2020年国勢調査選択肢
var meshAgeSelect =
  '<div class="row">' +
    '<label class="col-sm-3 col-form-label">属性の選択</label>' +
    '<div class="col-sm-9 checkbox-radios">' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios1" value="T001101001"> 人口総数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios2" value="T001101004"> 0～14歳' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios3" value="T001101007"> 15歳以上総数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios4" value="T001101010"> 15～64歳' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios5" value="T001101016"> 20歳以上総数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios6" value="T001101019"> 65歳以上総数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="ageRadios7" value="T001101022"> 75歳以上総数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
    '</div>' +
  '</div>'
;

var meshSetaiSelect =
  '<div class="row">' +
    '<label class="col-sm-3 col-form-label">属性の選択</label>' +
    '<div class="col-sm-9 checkbox-radios">' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios1" value="T001101035"> 一般世帯総数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios2" value="T001101043"> 親族世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios3" value="T001101044"> 核家族世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios4" value="T001101046"> 6歳未満世帯員のいる一般世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios5" value="T001101047"> 65歳以上の世帯員のいる一般世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios6" value="T001101048"> 世帯主年齢が20～29歳の1人世帯一般世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios7" value="T001101049"> 高齢単身一般世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="setaiRadios8" value="T001101050"> 高齢夫婦のみの一般世帯数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
    '</div>' +
  '</div>'
;

var perAgeSelect =
  '<div class="row">' +
    '<label class="col-sm-3 col-form-label">属性の選択</label>' +
    '<div class="col-sm-9 checkbox-radios">' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="perAgeRadios1" value="総数_g"> 総数' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="perAgeRadios2" value="0~6歳"> 0~6歳' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="perAgeRadios3" value="7~12歳"> 7~12歳' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="perAgeRadios4" value="13~19歳"> 13~19歳' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="perAgeRadios5" value="20歳代"> 20歳代' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="perAgeRadios6" value="30歳代"> 30歳代' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="perAgeRadios7" value="40歳代"> 40歳代' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="perAgeRadios8" value="50歳代"> 50歳代' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="perAgeRadios9" value="60歳代"> 60歳代' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
      '<div class="form-check-radio form-check-inline">' +
        '<label class="form-check-label">' +
          '<input class="form-check-input" type="radio" name="attrRadioz" id="perAgeRadios10" value="70歳~"> 70歳~' +
          '<span class="form-check-sign"></span>' +
        '</label>' +
      '</div>' +
    '</div>' +
  '</div>'
;

var cardOfCustomerDistribution =
  '<div class="card-header h6"> 商圏別顧客分布 </div>' +
  '<div class="card-body">' +
    '<div class="card-title">' +
      '総入庫台数：<div id="legend_tempo_cust_total">9999</div>' +
    '</div>' +
    '<div class="card-title">' +
      '対象商圏内入庫台数：<div id="legend_tempo_cust_area_total">9999</div>' +
    '</div>' +
    '<div class="card-text">' +
      '<div class="">' +
        '<table class="table" id="legendCustMatrixtable">' +
          '<thead class="">' +
            '<th align="center" id="legend_1_tempo_matrix_name">' +
              '商圏' +
            '</th>' +
            '<th align="center" id="legend_1_tempo_area_name_r_x">' +
              '商圏内総数<br /><small>上段&nbsp;入庫台数</small><br /><small>下段&nbsp;重複率</small>' +
            '</th>' +
            '<th align="center" id="legend_1_tempo_area_name_r_0">' +
              'x商圏名0(店舗名）' +
            '</th>' +
            '<th align="center" id="legend_1_tempo_area_name_r_1">' +
              'x商圏名1(店舗名）' +
            '</th>' +
            '<th align="center" id="legend_1_tempo_area_name_r_2">' +
              'x商圏名2(店舗名）' +
            '</th>' +
            '<th align="center" id="legend_1_tempo_area_name_r_3">' +
              'x商圏名3(店舗名）' +
            '</th>' +
            '<th align="center" id="legend_1_tempo_area_name_r_4">' +
              'x商圏名4(店舗名）' +
            '</th>' +
          '</thead>' +
          '<tbody>' +
            '<tr id="tempo_r0">' +
              '<th align="left" scope="row" id="legend_1_tempo_area_name_c_0">' +
                'y商圏名0(店舗名）' +
              '</th>' +
              '<td align="right" id="legend_1_cust_total_r0_x">' +
                '999' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r0_0">' +
                '１×１' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r0_1">' +
                '１×２' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r0_2">' +
                '１×３' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r0_3">' +
                '１×４' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r0_4">' +
                '１×５' +
              '</td>' +
            '</tr>' +
            '<tr id="tempo_r1">' +
              '<th align="left" scope="row" id="legend_1_tempo_area_name_c_1">' +
                'y商圏名1(店舗名）' +
              '</th>' +
              '<td align="right" id="legend_1_cust_total_r1_x">' +
                '999' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r1_0">' +
                '２×１' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r1_1">' +
                '２×２' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r1_2">' +
                '２×３' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r1_3">' +
                '２×４' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r1_4">' +
                '２×５' +
              '</td>' +
            '</tr>' +
            '<tr id="tempo_r2">' +
              '<th align="left" scope="row" id="legend_1_tempo_area_name_c_2">' +
                'y商圏名2(店舗名）' +
              '</th>' +
              '<td align="right" id="legend_1_cust_total_r2_x">' +
                '999' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r2_0">' +
                '３×１' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r2_1">' +
                '３×２' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r2_2">' +
                '３×３' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r2_3">' +
                '３×４' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r2_4">' +
                '３×５' +
              '</td>' +
            '</tr>' +
            '<tr id="tempo_r3">' +
              '<th align="left" scope="row" id="legend_1_tempo_area_name_c_3">' +
                'y商圏名3(店舗名）' +
              '</th>' +
              '<td align="right" id="legend_1_cust_total_r3_x">' +
                '999' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r3_0">' +
                '４×１' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r3_1">' +
                '４×２' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r3_2">' +
                '４×３' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r3_3">' +
                '４×４' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r3_4">' +
                '４×５' +
              '</td>' +
            '</tr>' +
            '<tr id="tempo_r4">' +
              '<th align="left" scope="row" id="legend_1_tempo_area_name_c_4">' +
                'y商圏名4(店舗名）' +
              '</th>' +
              '<td align="right" id="legend_1_cust_total_r4_x">' +
                '999' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r4_0">' +
                '５×１' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r4_1">' +
                '５×２' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r4_2">' +
                '５×３' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r4_3">' +
                '５×４' +
              '</td>' +
              '<td align="right" id="legend_1_cust_total_r4_4">' +
                '５×５' +
              '</td>' +
            '</tr>' +
          '</tbody>' +
        '</table>' +
      '</div>' +
    '</div>' +
    '<div class="card-subtitle">' +
      '<small>※同一商圏同士の重複セルの値は、その商圏のみでカバーしている入庫数</small>' +
    '</div>' +
  '</div>';

//以下Google Map内の処理-------------------------------------------------------------------------------

//グローバル変数
var map; //地図
var trafficLayer; //交通情報レイヤー
var currentLayer = []; //現在のレイヤーを入れる箱
var features_dict = {}; //geojsonのレイヤー情報をLayerPathをキーの元、辞書に入れる {layerPath: features, layerPath: features, ...}
var c_markers = []; //顧客マーカー入れ
var s_markers = []; //店舗マーカー入れ
var circles = []; //商圏入れ
var parks = []; //集客施設入れ
var current_icon = []; //表示中のアイコン種類
var polygon = []; //到達圏ポリゴンなど入れる箱

//道路のみの地図スタイル
var onlyRoad = new google.maps.StyledMapType(
  [
    {
      "featureType": "landscape.man_made",
      "elementType": "labels.icon",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "landscape.natural",
      "elementType": "geometry.fill",
      "stylers": [
        {
          "color": "#dfdfdf"
        }
      ]
    },
    {
      "featureType": "landscape.natural",
      "elementType": "labels.icon",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "poi",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    }
  ],
  {name: '道路のみ'}
);

//道路、学校、公園、アトラクション施設、スポーツ施設のマーカーのみのマップ
var placeOfChild = new google.maps.StyledMapType(
  [
    {
      "featureType": "landscape.natural",
      "elementType": "geometry.fill",
      "stylers": [
        {
          "color": "#dfdfdf"
        }
      ]
    },
    {
      "elementType": "labels",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    },
    {
      "elementType": "labels.icon",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "poi.attraction",
      "elementType": "labels",
      "stylers": [
        {
          "visibility": "on"
        }
      ]
    },
    {
      "featureType": "poi.attraction",
      "elementType": "labels.icon",
      "stylers": [
        {
          "visibility": "on"
        }
      ]
    },
    {
      "featureType": "poi.park",
      "elementType": "labels",
      "stylers": [
        {
          "visibility": "on"
        }
      ]
    },
    {
      "featureType": "poi.park",
      "elementType": "labels.icon",
      "stylers": [
        {
          "visibility": "on"
        }
      ]
    },
    {
      "featureType": "poi.school",
      "elementType": "labels",
      "stylers": [
        {
          "visibility": "on"
        }
      ]
    },
    {
      "featureType": "poi.school",
      "elementType": "labels.icon",
      "stylers": [
        {
          "visibility": "on"
        }
      ]
    },
    {
      "featureType": "poi.sports_complex",
      "elementType": "labels.icon",
      "stylers": [
        {
          "visibility": "on"
        }
      ]
    },
    {
      "featureType": "poi.sports_complex",
      "elementType": "labels.text",
      "stylers": [
        {
          "visibility": "on"
        }
      ]
    },
    {
      "featureType": "road",
      "elementType": "labels",
      "stylers": [
        {
          "visibility": "on"
        }
      ]
    },
    {
      "featureType": "road",
      "elementType": "labels.icon",
      "stylers": [
        {
          "visibility": "on"
        }
      ]
    }
  ],
  {name: '学校公園施設'}
);

//デフォルトマップをレトロ色に設定
var defaultMap = new google.maps.StyledMapType(
  [
    {
      "featureType": "landscape.natural",
      "elementType": "geometry.fill",
      "stylers": [
        {
          "color": "#dfdfdf"
        }
      ]
    }
  ],
  {name: '地図'}
);

//各店舗の基本情報モーダルの中身をデータより変更する
function inputShopDetailData(data) {
  $('input[name="shop_name"]').val([data.name]);
  $('input[name="open_year_month"]').val([data.open_year_month]);
  $('input[name="build_year"]').val([data.build_passed_year]);
  $('input[name="tel_num"]').val([data.tel]);
  $('input[name="post_code"]').val([data.post_code]);
  $('input[name="address"]').val([data.address]);
  $('textarea[name="notices"]').val([data.notices]);
  $('input[name="shop_area_square_meter"]').val([data.shop_area_square_meter]);
  $('input[name="shop_area_tsubo"]').val([data.shop_area_tsubo]);
  $('input[name="chinshaku_area_square_meter"]').val([data.chinshaku_area_square_meter]);
  $('input[name="chinshaku_area_tsubo"]').val([data.chinshaku_area_tsubo]);
  $('input[name="place_rent"]').val([data.place_rent]);
  $('input[name="building_area_square_meter"]').val([data.building_area_square_meter]);
  $('input[name="building_area_tsubo"]').val([data.building_area_tsubo]);
  $('input[name="total_floor_area_square_meter"]').val([data.total_floor_area_square_meter]);
  $('input[name="total_floor_area_tsubo"]').val([data.total_floor_area_tsubo]);
  $('input[name="building_rent"]').val([data.building_rent]);
  $('input[name="youto_chiiki"]').val([data.youto_chiiki]);
  $('input[name="factory_area_square_meter"]').val([data.factory_area]);
  $('input[name="factory_auth"]').val([data.factory_auth]);
  $('input[name="stalls"]').val([data.stalls]);
  $('input[name="total_shop_menber"]').val([data.total_shop_menber]);
  $('input[name="store_manager"]').val([data.store_manager]);
  $('input[name="vice_store_manager"]').val([data.vice_store_manager]);
  $('input[name="TM"]').val([data.TM]);
  $('input[name="QA_SC"]').val([data.QA_SC]);
  $('input[name="STM"]').val([data.STM]);
  $('input[name="SAD_TM"]').val([data.SAD_TM]);
  $('input[name="EL_WSL"]').val([data.EL_WSL]);
  $('input[name="SE_TS"]').val([data.SE_TS]);
  $('input[name="FC_RS"]').val([data.FC_RS]);
  $('input[name="others"]').val([data.others]);
  $('textarea[name="close_store_P"]').val([data.close_store_P]);
  $('textarea[name="close_store_C"]').val([data.close_store_C]);
  $('textarea[name="close_store_N"]').val([data.close_store_N]);
  $('textarea[name="remarks"]').val([data.remarks]);
  $('textarea[name="feature_store"]').val([data.feature_store]);
}

//店舗基本情報の表の部分の書き込みをデータより行う
function inputSalesResultData(data) {
  y_1_list = data.Y_1.split(','); //Y-1年のリスト
  y_2_list = data.Y_2.split(','); //Y-2年のリスト
  y_3_list = data.Y_3.split(','); //Y-3年のリスト
  y_list = ['y_3','y_2', 'y_1'];
  id_list = ['_customer', '_sa', '_new_car', '_u_car', '_fix_car', '_inspection']
  for (var i = 0; i < y_list.length; i++) {
    if (y_list[i] == 'y_3') {
      for (var n = 0; n < id_list.length; n++) {
        $('#' + y_list[i] + id_list[n]).text(y_3_list[n]);
      }
    } else if (y_list[i] == 'y_2') {
      for (var n = 0; n < id_list.length; n++) {
        $('#' + y_list[i] + id_list[n]).text(y_2_list[n]);
      }
    } else {
      for (var n = 0; n < id_list.length; n++) {
        $('#' + y_list[i] + id_list[n]).text(y_1_list[n]);
      }
    }
  }
}
