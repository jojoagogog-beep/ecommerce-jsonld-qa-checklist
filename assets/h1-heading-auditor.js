/* PAL local static HTML H1 check: no networking, no image loading, no eval. */
(function(root){
  "use strict";
  function clean(source) {
    return String(source || "")
      .replace(/<!--[\s\S]*?-->/g, "")
      .replace(/<script\b[^>]*>[\s\S]*?<\/script\s*>/gi, "")
      .replace(/<style\b[^>]*>[\s\S]*?<\/style\s*>/gi, "")
      .replace(/<textarea\b[^>]*>[\s\S]*?<\/textarea\s*>/gi, "");
  }
  function check(source) {
    const html = clean(source);
    const starts = Array.from(html.matchAll(/<h1\b[^>]*>/gi));
    const complete = Array.from(html.matchAll(/<h1\b[^>]*>([\s\S]*?)<\/h1\s*>/gi));
    const headings = complete.map((m,idx) => ({
      index:idx+1,
      text:m[1].replace(/<[^>]*>/g," ").replace(/\s+/g," ").trim()
    }));
    const empty = headings.filter(h => !h.text).length;
    const issues = [];
    if (!starts.length) issues.push("No H1 found in supplied static HTML. Review the page structure manually.");
    if (starts.length>1) issues.push("Multiple H1 headings found. This is not always invalid; check page purpose and hierarchy.");
    if (starts.length>complete.length) issues.push("One or more H1 start tags lack a matching closing tag in this basic scanner.");
    if (empty) issues.push(empty+" empty H1 heading(s) detected.");
    return {total:starts.length, matched:complete.length, empty, headings, issues};
  }
  const api = {check};
  if (typeof module !== "undefined" && module.exports) module.exports=api;
  if(root) root.PALH1HeadingAuditor=api;
})(typeof window !== "undefined" ? window : null);
