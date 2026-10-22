/* PAL buyer education: hypothetical manual labor vs a static-page monitoring workflow.
   Pure arithmetic, no network requests, no storage, no personalized tracking. */
(function(root){
"use strict";
function finite(n,min,max){const v=Number(n);return Number.isFinite(v)&&v>=min&&v<=max;}
function estimate(values){
  const n=Number(values.pages), frequency=Number(values.checksPerWeek),
        manual=Number(values.manualMinutesPerPage), review=Number(values.reviewMinutesPerRun),
        setup=Number(values.initialSetupMinutes), hourly=Number(values.hourlyLaborCostUsd);
  if(!finite(n,1,50)||!Number.isInteger(n)||!finite(frequency,1,21)||!Number.isInteger(frequency)||
     !finite(manual,0.1,120)||!finite(review,0,180)||!finite(setup,0,480)||
     !finite(hourly,0,1000)){
    return {valid:false,error:"Enter a valid number: 1–50 URLs, 1–21 checks per week, and nonnegative labor costs."};
  }
  const weeksPerMonth=52/12,initialAmortizationWeeks=4;
  const manualMinutesWeekly=n*frequency*manual;
  const reviewMinutesWeekly=frequency*review;
  const setupPerWeek=setup/initialAmortizationWeeks;
  const modelMinutesWeekly=reviewMinutesWeekly+setupPerWeek;
  const potentialMinutesWeekly=Math.max(0,manualMinutesWeekly-modelMinutesWeekly);
  const potentialHoursMonthly=potentialMinutesWeekly*weeksPerMonth/60;
  const illustrativeLaborValue=potentialHoursMonthly*hourly;
  // One successfully processed product-priced offer per URL, plus a start event.
  const estimatedProductsMonthly=n*frequency*weeksPerMonth;
  const estimatedRunsMonthly=frequency*weeksPerMonth;
  const productRate=0.0035,runRate=0.00005; // Free-tier rates observed Oct 22, 2026.
  const estimatedEventsUsd=estimatedProductsMonthly*productRate+estimatedRunsMonthly*runRate;
  return {valid:true,pages:n,checksPerWeek:frequency,
          manualHoursMonthly:manualMinutesWeekly*weeksPerMonth/60,
          afterHoursMonthly:modelMinutesWeekly*weeksPerMonth/60,
          potentialHoursMonthly,illustrativeLaborValue,
          estimatedProductsMonthly,estimatedRunsMonthly,estimatedEventsUsd,
          note:"This is a user-supplied scenario, not actual time saved or a guaranteed ROI."};
}
const api={estimate};
if(typeof module!=="undefined"&&module.exports)module.exports=api;
if(root)root.PALWorkflowSavings=api;
})(typeof window!=="undefined"?window:null);
