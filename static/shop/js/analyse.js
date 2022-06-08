window.addEventListener("load" , function (){
    draw_monthly_graph();
});


function draw_monthly_graph(){

    //テーブルから月ごとのデータを取る
    let month_elem      = $(".month");
    let amount_elem     = $(".amount");
    let monthly_data    = [];

    //1月から12月までの初期化したデータ(辞書型のリスト)を作る。
    for (let i=1;i<13;i++){
        let obj         = {};
        obj["label"]    = String(i) + "月";
        obj["amount"]   = 0;

        monthly_data.push(obj);
    }


    /*
    for (let m of monthly_data){
        console.log(m); //←このmはjQueryのオブジェクトではないので、jQueryのメソッドは使えない。
    }
    */

    //テーブルから抜き取ったデータからmonthly_dataへ格納
    for (let i=0;i<month_elem.length;i++){

        let target_index    = Number(month_elem.eq(i).text().replace("月","")) - 1;
        let target_amount   = Number(amount_elem.eq(i).text().replace("円",""));

        monthly_data[target_index]["amount"]    = target_amount
    }

    //月ごとのラベルとデータが作られた。
    console.log(monthly_data);


    let labels      = [];
    let datasets    = [];

    for (let m of monthly_data){

        labels.push(m["label"]);
        datasets.push(m["amount"]);

    }

    const ctx       = document.getElementById('monthly_graph').getContext('2d');
    const myChart   = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels, 
            datasets: [{
                label: "売上金額",
                data: datasets,
                backgroundColor: "rgb(100,200,100)",
            }]
        },
        //y軸は0から始める
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });





}

