window.addEventListener("load" , function (){


    //order_byの指定があれば、同様にurl_replace_sendに送信。
    $("[name='order_by']").on("input",function(){ url_replace_send(this); });

    $("[name='min_price']").on("keydown", function(e) { if( e.keyCode === 13 ){ url_replace_send(this); } });
    $("[name='max_price']").on("keydown", function(e) { if( e.keyCode === 13 ){ url_replace_send(this); } });
    $("[name='search']").on("keydown", function(e)    { if( e.keyCode === 13 ){ url_replace_send(this); } });
    



});
function url_replace_send(elem){

    let key     = $(elem).prop("name");
    let value   = $(elem).val();

    //TODO:ここでクエリストリングを書き換える。
    // https://maku77.github.io/js/web/search-params.html

    param   = new URLSearchParams(window.location.search);

    //valueが空欄であれば、キーを削除
    if (value === "" ){
        param.delete(key);
    }
    else{
        param.set(key, value);
    }

    //書き換えたクエリストリングへ移動する
    // https://qiita.com/shuntaro_tamura/items/99adbe51132e0fb3c9e9
    
    if (param.toString() === ""){
        window.location.href = window.location.origin + window.location.pathname;
    }
    else{
        //search=test&page=2
        window.location.href = "?" + param.toString();
    }

}

