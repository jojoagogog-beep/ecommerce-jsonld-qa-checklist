"use strict";
(function(root){
  const MAX=512*1024;
  function str(x){return x===null||x===undefined?"":String(x);}
  function cleanPrice(x){
    const s=str(x).trim();
    if(!/^\d{1,12}(?:\.\d{1,6})?$/.test(s))return "";
    const n=Number(s);
    return Number.isFinite(n)?s:"";
  }
  function currency(x){
    const s=str(x).trim().toUpperCase();
    return /^[A-Z]{3}$/.test(s)?s:"";
  }
  function typ(v,t){
    if(Array.isArray(v))return v.some(x=>typ(x,t));
    return typeof v==="string"&&v.replace(/\/$/,"").split("/").pop().toLowerCase()===t.toLowerCase();
  }
  function parseTags(html,kind){
    const out=[]; const rx=new RegExp("<"+kind+"\\b[^>]*>","gi");
    const matches=html.match(rx)||[];
    for(const tag of matches.slice(0,80)){
      const attrs={};
      const attrRe=/([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/g;
      let m;
      while((m=attrRe.exec(tag)))attrs[m[1].toLowerCase()]=m[2]??m[3]??m[4]??"";
      out.push(attrs);
    }
    return out;
  }
  function rootsFrom(input){
    const s=input.trim();
    if(s.charAt(0)!=="<"){return [JSON.parse(s)];}
    const matches=s.match(/<script\b[^>]*>[\s\S]*?<\/script\s*>/gi)||[];
    if(matches.length>30)throw Error("More than 30 script blocks.");
    return matches.filter(x=>/\btype\s*=\s*(?:"application\/ld\+json"|'application\/ld\+json'|application\/ld\+json)/i.test(x))
      .map((x,i)=>{
        const a=x.indexOf(">"),b=x.search(/<\/script\s*>/i);
        try{return JSON.parse(x.slice(a+1,b));}
        catch(e){throw Error("Invalid JSON-LD script #"+(i+1)+".");}
      });
  }
  function collect(obj,out,depth){
    if(depth>8||out.length>=30||!obj||typeof obj!=="object")return;
    if(Array.isArray(obj)){obj.slice(0,80).forEach(x=>collect(x,out,depth+1));return;}
    if(typ(obj["@type"],"Product"))out.push(obj);
    if(obj["@graph"])collect(obj["@graph"],out,depth+1);
    if(obj.mainEntity)collect(obj.mainEntity,out,depth+1);
  }
  function inspect(input){
    if(typeof input!=="string"||!input.trim())throw Error("Paste a static HTML page or Product JSON-LD first.");
    if(input.length>MAX)throw Error("Pasted content exceeds 512 KB.");
    const roots=rootsFrom(input),products=[];
    roots.forEach(x=>collect(x,products,0));
    let data=null,model="",warning="";
    if(products.length){
      if(products.length!==1)return {status:"Needs review",details:"Multiple Product records found. This basic check cannot choose a single offer reliably."};
      const p=products[0];
      const offers=p.offers;
      if(Array.isArray(offers)||!offers||typeof offers!=="object")
        return {status:"Needs review",details:"Product JSON-LD exists, but a single direct offers object was not found. Multi-offer pages need manual review."};
      const price=cleanPrice(offers.price??offers.lowPrice??"");
      const cur=currency(offers.priceCurrency||"");
      data={name:str(p.name).slice(0,110),price,currency:cur,
        availability:str(offers.availability||"").slice(0,160)};
      model="Product/Offer JSON-LD";
      if(!data.price||!data.currency)warning="A valid price and ISO currency must both be explicitly declared.";
    }else if(input.trim().charAt(0)==="<"){
      const metas=parseTags(input,"meta");
      const find=k=>{const row=metas.find(a=>(a.property||a.name||"").toLowerCase()===k);return row?str(row.content):"";};
      const type=find("og:type").toLowerCase().trim();
      if(type!=="product"&&!type.startsWith("product."))return {status:"Not confirmed",details:"No Product JSON-LD or explicitly product-typed Open Graph metadata was found."};
      data={name:find("og:title").slice(0,110),
        price:cleanPrice(find("product:price:amount")),
        currency:currency(find("product:price:currency")),
        availability:find("product:availability").slice(0,160)};
      model="Product-typed Open Graph";
      if(!data.price||!data.currency)warning="Product-typed Open Graph requires valid product:price:amount and product:price:currency.";
    }else return {status:"Not confirmed",details:"The JSON does not contain one supported Product with a single Offer."};
    return {status:warning?"Needs review":"Static metadata looks compatible",
      details:model+"\nProduct: "+(data.name||"Not declared")+
       "\nPublished price: "+(data.price||"Not declared")+
       "\nCurrency: "+(data.currency||"Not declared")+
       "\nAvailability label: "+(data.availability||"Not declared")+
       "\n"+(warning||"Basic fields detected. This does not guarantee a successful live run.")};
  }
  if(typeof module!=="undefined"&&module.exports)module.exports={inspect};
  if(root&&root.document){
    const d=root.document,src=d.getElementById("source"),status=d.getElementById("status"),detail=d.getElementById("details");
    if(src&&status&&detail){
      const example=src.value;
      function render(){
        try{const r=inspect(src.value);status.textContent=r.status;detail.textContent=r.details;}
        catch(err){status.textContent="Cannot inspect source";detail.textContent=err.message;}
      }
      d.getElementById("check").addEventListener("click",render);
      d.getElementById("reset").addEventListener("click",function(){src.value=example;render();});
      render();
    }
  }
})(typeof window!=="undefined"?window:null);
