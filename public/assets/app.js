'use strict';
const languagePicker=document.querySelector('.language-picker');
if(languagePicker){
 const trigger=languagePicker.querySelector('summary');
 document.addEventListener('pointerdown',event=>{if(!languagePicker.contains(event.target))languagePicker.open=false});
 document.addEventListener('keydown',event=>{if(event.key==='Escape'&&languagePicker.open){languagePicker.open=false;trigger.focus()}});
 languagePicker.addEventListener('focusout',()=>{requestAnimationFrame(()=>{if(!languagePicker.contains(document.activeElement))languagePicker.open=false})});
}
const sticky=document.querySelector('.sticky');
let heroVisible=true,formVisible=false;
const syncSticky=()=>sticky?.classList.toggle('visible',!heroVisible&&!formVisible);
if('IntersectionObserver' in window){
 new IntersectionObserver(entries=>{heroVisible=entries[0].isIntersecting;syncSticky()}).observe(document.querySelector('.hero'));
 new IntersectionObserver(entries=>{formVisible=entries[0].isIntersecting;syncSticky()}).observe(document.querySelector('#enquire'));
}
const frame=document.querySelector('iframe[data-tally-src]');
if(frame){
 const src=new URL(frame.dataset.tallySrc);
 const params=new URLSearchParams(location.search);
 ['utm_source','utm_medium','utm_campaign','utm_content','utm_term'].forEach(key=>{if(params.has(key))src.searchParams.set(key,params.get(key))});
 src.searchParams.set('page_language',document.documentElement.lang);
 frame.dataset.tallySrc=src.href;
 frame.src=src.href;
 const script=document.createElement('script');script.src='https://tally.so/widgets/embed.js';script.async=true;script.onload=()=>window.Tally?.loadEmbeds();document.body.appendChild(script);
}

// Progressive motion: content remains visible without JS or animation support.
const motionPreference=window.matchMedia('(prefers-reduced-motion: reduce)');
const runningReveals=new Set();
let revealObserver;
if(!motionPreference.matches && 'IntersectionObserver' in window && Element.prototype.animate){
 const revealTargets=document.querySelectorAll('.wrap h2,.wrap .lead,.stats>div,.island-section figure,.island-section .copy,.simple-residence,.post-handover,.total-plan,.milestone,.benefits article,.visa,.faq-grid>div,.contact .split>div');
 revealObserver=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{
   if(!entry.isIntersecting)return;
   revealObserver.unobserve(entry.target);
   if(motionPreference.matches)return;
   const anim=entry.target.animate([{opacity:.25,transform:'translateY(20px)'},{opacity:1,transform:'translateY(0)'}],{duration:680,easing:'cubic-bezier(.22,1,.36,1)',fill:'none'});
   runningReveals.add(anim);
   anim.finished.catch(()=>{}).finally(()=>runningReveals.delete(anim));
  });
 },{threshold:.08});
 revealTargets.forEach(el=>{if(el.getBoundingClientRect().top>=window.innerHeight)revealObserver.observe(el)});
}
motionPreference.addEventListener('change',event=>{
 if(event.matches){revealObserver?.disconnect();runningReveals.forEach(anim=>anim.cancel());runningReveals.clear()}
});

