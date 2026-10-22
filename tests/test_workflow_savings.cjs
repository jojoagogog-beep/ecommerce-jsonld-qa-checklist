const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {estimate}=require('../assets/workflow-savings.js');
const base={pages:20,checksPerWeek:4,manualMinutesPerPage:2,reviewMinutesPerRun:15,initialSetupMinutes:45,hourlyLaborCostUsd:20};
const r=estimate(base);
assert(r.valid);
assert(Math.abs(r.estimatedProductsMonthly-20*4*52/12)<1e-9);
assert(Math.abs(r.estimatedEventsUsd-(20*4*52/12*0.0035+4*52/12*0.00005))<0.0000001);
assert(r.potentialHoursMonthly>0);
assert(r.illustrativeLaborValue>0);
const none=estimate({...base,reviewMinutesPerRun:180});
assert(none.valid&&none.potentialHoursMonthly===0&&none.illustrativeLaborValue===0);
assert(estimate({...base,pages:1}).valid);
assert(estimate({...base,pages:50}).valid);
assert(estimate({...base,initialSetupMinutes:0}).valid);
for(const options of [{pages:0},{pages:51},{pages:1.5},{checksPerWeek:0},{checksPerWeek:22},
 {manualMinutesPerPage:0},{manualMinutesPerPage:-1},{hourlyLaborCostUsd:-1},{hourlyLaborCostUsd:2000},
 {reviewMinutesPerRun:-1},{initialSetupMinutes:-1},{pages:Infinity},{pages:'not-a-number'}]){
 assert.equal(estimate({...base,...options}).valid,false,JSON.stringify(options));
}
const root=path.join(__dirname,'..');
const page=fs.readFileSync(path.join(root,'workflow-time-savings.html'),'utf8');
const script=fs.readFileSync(path.join(root,'assets/workflow-savings.js'),'utf8');
assert(page.includes('src="assets/workflow-savings.js"'));
assert(page.includes('utm_campaign=workflow_time_savings'));
assert(page.includes('user-supplied')||page.includes('assumptions'));
assert(page.includes('before any proposed tier discount'));
assert(page.includes('Manual')&&page.includes('Apify'));
assert(!script.includes('fetch(')&&!script.includes('XMLHttpRequest')&&!script.includes('localStorage'));
for(const p of ['competitor-price-tracker.html','index.html','sitemap.xml','README.md']){
 assert(fs.readFileSync(path.join(root,p),'utf8').includes('workflow-time-savings.html'),p);
}
console.log('PASS time-savings numeric boundaries and local/no-network purchase-path checks');
