'use strict';
const input=document.querySelector('#property-price');
if(input){
 const locale=document.body.dataset.locale;
 const fx=Number(document.body.dataset.aedUsd);
 const pct=Number(document.body.dataset.booking)/100;
 const error=document.querySelector('#calc-error');
 const format=new Intl.NumberFormat(locale,{maximumFractionDigits:0});
 input.addEventListener('input',()=>{
  const price=Number(input.value);
  const valid=input.value!==''&&input.validity.valid&&Number.isFinite(price);
  error.textContent=valid?'':error.dataset.message;
  input.setAttribute('aria-invalid',String(!valid));
  const booking=Math.round(price*pct);
  const amounts={booking,handover:price-booking,total:price,before:booking};
  document.querySelectorAll('[data-payment]').forEach(el=>el.textContent=valid?format.format(amounts[el.dataset.payment])+' AED':'—');
  document.querySelectorAll('[data-usd]').forEach(el=>el.textContent=valid?'≈ '+format.format(amounts[el.dataset.usd]/fx)+' USD':'—');
 });
}
