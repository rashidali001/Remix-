$('.carousel').carousel()

function DisplayForm(){
    let new_purchase = document.querySelector("div.new_purchase");
    new_purchase.style.display = "block";
}

function ClosePurchase(){
    let new_purchase = document.querySelector("div.new_purchase");
    new_purchase.style.display = "none";
}

let price = document.querySelector("#price");
let points = document.querySelector("#points");

price.addEventListener("keyup", ()=>{
    price_val = parseInt(price.value);
    points.value = (2 * price_val) / 100;
    if (points.value  == ""){
        points.value = 0;
    }
})

function CloseFlashedMessage(){
    let flashed = document.querySelector("#flashed_messages");
    flashed.style.display = none;
}

